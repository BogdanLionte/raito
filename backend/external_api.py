import re
import json
from django.http import HttpResponse
from difflib import get_close_matches
import requests
from authentication import is_authorized
from authentication import http_method_list
import database

verb_synonyms = {
    'get': ['get', 'fetch', 'retrieve', 'give', 'bring'],
    'put': ['replace'],
    'post': ['create'],
    'delete': ['delete', 'remove', 'erase'],
    'patch': ['update'],
    'options': []
}


class Path:
    def __init__(self, name, verbs=None, path_params=None, query_params=None, request_body='', initial_path=None):
        self.name = name
        self.initial_path = initial_path
        self.verbs = verbs
        self.path_params = path_params
        self.query_params = query_params
        self.request_body = request_body

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name \
               and self.verbs == other.verbs \
               and self.path_params == other.path_params \
               and self.query_params == other.query_params \
               and self.request_body == other.request_body \
               and self.initial_path == other.initial_path \



@http_method_list(["GET"])
@is_authorized
def query(request, api):
    sentence = request.GET.get('sentence')

    json_api_description = get_json_description_for_api(api)
    predicted_paths = get_predicted_paths(sentence, get_available_paths(json_api_description))
    api_base_path = json_api_description['servers'][0]['url']

    for predicted_path in predicted_paths:
        predicted_path.verbs = get_predicted_verbs(sentence,
                                                   get_available_verbs(json_api_description, predicted_path.name))
        predict_path_param(sentence, predicted_path)

    # remove paths with no predicted verbs
    predicted_paths = [path for path in predicted_paths if path.verbs]

    set_request_body(predicted_paths, json_api_description, sentence)

    response = {}
    response['predicted_requests'] = build_requests(api_base_path, predicted_paths)

    if not response['predicted_requests']:
        response['api_response'] = []
    else:
        response['api_response'] = send_request_and_get_response(response['predicted_requests'][0])

    response = json.dumps(response)
    access_token = request.headers.get("Authorization")
    database.write_query(access_token, api, response)
    return HttpResponse(response)


def get_predicted_paths(sentence, available_paths):
    predicted_paths = []

    for path in available_paths:
        for word in sentence.split():
            if get_close_matches(word, [path], cutoff=0.5) and Path(name=path) not in predicted_paths:
                predicted_paths.append(Path(name=path, initial_path=path))

    return predicted_paths


def get_predicted_verbs(sentence, available_verbs):
    predicted_verbs = []

    for available_verb in available_verbs:
        for word in sentence.split():
            if available_verb in verb_synonyms.keys() and word in verb_synonyms[available_verb]:
                predicted_verbs.append(available_verb)

    return predicted_verbs


def predict_path_param(sentence, predicted_path):
    path_params = re.findall("\/.*\/\{.*\}", predicted_path.name)

    for path_param in path_params:
        path_param_name = path_param.split("/")[2]
        path_param_value = get_value_for_key_in_sentence(path_param_name, sentence)
        if path_param_value:
            predicted_path.name = predicted_path.name.replace(path_param.split("/")[2], path_param_value)


def create_json_request_body(request_body_content, sentence):
    properties = request_body_content['properties']
    request_body = {}

    for property in properties:
        request_body[property] = get_value_for_key_in_sentence(property, sentence)

    return request_body


def set_request_body(predicted_paths, json_api_description, sentence):
    for predicted_path in predicted_paths:
        for verb in predicted_path.verbs:
            if 'requestBody' in json_api_description['paths'][predicted_path.initial_path][verb].keys():
                request_body_content = json_api_description['paths'][predicted_path.name][verb]['requestBody'][
                    'content']

                if 'application/json' in request_body_content.keys():
                    predicted_path.request_body = create_json_request_body(
                        request_body_content['application/json']['schema'], sentence)


def send_request_and_get_response(request):
    verb = request.split()[0]
    url = request.split()[1]
    if len(request.split()) > 2:
        params = request.split()[2]

    if verb == 'GET':
        response = requests.get(url = url)

    if verb == 'POST':
        response = requests.post(url = url, params = params)

    if verb == 'DELETE':
        response = requests.delete(url = url)

    if verb == 'PUT':
        response = requests.put(url = url, params = params)

    if verb == 'PATCH':
        response = requests.patch(url = url, params = params)

    return response.json()


def build_requests(api_base_path, predicted_paths):
    predicted_requests = []
    for predicted_path in predicted_paths:
        for verb in predicted_path.verbs:
            predicted_requests.append(
                verb.upper() + ' ' + api_base_path + predicted_path.name + ' ' + str(predicted_path.request_body))
    return predicted_requests


def get_available_paths(json_api_description):
    return json_api_description['paths']

def get_available_verbs(json_api_description, path):
    return json_api_description['paths'][path].keys()

def get_value_for_key_in_sentence(key, sentence):
    words = sentence.split()
    for i in range(len(words)):
        if get_close_matches(key, [words[i]], cutoff=0.5):
            return words[i + 1]


def get_json_description_for_api(api):
    return json.load(open('./apis/' + api + '.json'))
