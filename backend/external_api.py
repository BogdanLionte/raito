from django.http import HttpResponse

import pathlib
import re
from authentication import is_authorized
print(pathlib.Path(__file__).parent.absolute())

import json

verb_synonyms = {
    'get': ['get', 'fetch', 'retrieve', 'give', 'bring'],
    'put': [],
    'post': [],
    'delete': ['delete', 'remove', 'erase'],
    'patch': [],
    'options': []
}

class Path:
    def __init__(self, name, verbs=None, path_params=None, query_params=None):
        self.name = name
        self.verbs = verbs
        self.path_params = path_params
        self.query_params = query_params

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name \
               and self.verbs == other.verbs \
               and self.path_params == other.path_params \
               and self.query_params == other.query_params


class HTTP_verb:
    def __init__(self, name):
        self.name = name


def get_predicted_paths(sentence, available_paths):
    predicted_paths = []

    for path in available_paths:
        for word in sentence.split():
            if word in path and Path(name=path) not in predicted_paths:
                predicted_paths.append(Path(name=path))

    return predicted_paths

def get_predicted_verbs(sentence, available_verbs):
    print('available verbs', available_verbs)
    predicted_verbs = []

    for available_verb in available_verbs:
        for word in sentence.split():
            if available_verb in verb_synonyms.keys() and word in verb_synonyms[available_verb]:
                predicted_verbs.append(available_verb)

    print('predicted verbs?', predicted_verbs)
    return predicted_verbs


def predict_path_param(sentence, predicted_path, predicted_paths):
    path_params = re.findall("\/.*\/\{.*\}", predicted_path.name)
    print('path paramzz')
    print(path_params)

    for path_param in path_params:
        path_param_name = path_param.split("/")[1]
        path_param_position_in_sentence = sentence.find(path_param_name)
        print("aaaa")
        print(sentence[path_param_position_in_sentence:])
        possible_path_param_values = re.findall("\d+", sentence[path_param_position_in_sentence:])
        if len(possible_path_param_values) > 0:
            path_param_value = re.findall("\d+", sentence[path_param_position_in_sentence:])[0]
        else:
            possible_path_param_values = re.findall("\d+", sentence)
            if len(possible_path_param_values) <= 0:
                print('could not determine path param value for path param ' + path_param_name + ' in predicted path ' + str(predicted_path))
                predicted_paths.remove(predicted_path)
                return
            else:
                path_param_value = re.findall("\d+", sentence)[0]

        print('replacing path param ' + path_param_name + ' with value ' + path_param_value)
        predicted_path.name = predicted_path.name.replace(path_param.split("/")[2], path_param_value)


@is_authorized
def query(request, api):

    # http://localhost:8000/query/api?sentence=sall
    print(request.GET.get('sentence'))
    print('api', api)
    sentence = request.GET.get('sentence')

    api_information = get_api_information_from_database(api)

    json_api_description = get_json_description_for_api(api)
    predicted_paths = get_predicted_paths(sentence, get_available_paths(json_api_description))


    for predicted_path in predicted_paths:
        predicted_path.verbs = get_predicted_verbs(sentence, get_available_verbs(json_api_description, predicted_path.name))
        predict_path_param(sentence, predicted_path, predicted_paths)


    print('predicted paths', predicted_paths)


    # if not api_information:
    #     api_information = extract_information(api)
    #     save_api_information_to_database(api_information)

    return HttpResponse('{\"sal\": \"pa\"}')


def get_available_HTTP_methods_for_path(param):
    pass

def get_api_information_from_database(api):
    return None

def save_api_information_to_database(api_information):
    pass

def get_available_paths(json_api_description):
    return json_api_description['paths']

def get_available_verbs(json_api_description, path):
    return json_api_description['paths'][path].keys()

def get_json_description_for_api(api):
    if api == 'json':
        print('ciaoo')
        return json.load(open('./json_storage_openAPI.json'))

