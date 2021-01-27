from django.http import HttpResponse
from authentication import http_method_list
import json
from authentication import is_authorized
from database import read_queries


@is_authorized
@http_method_list(["GET"])
def get(request):

    rows = read_queries(request.headers.get("Authorization"))
    response = {"history": []}

    for row in rows:
        response["history"].append({})
        history_dict = response["history"][len(response["history"]) - 1]
        history_dict["user"] = row[1]
        history_dict["api"] = row[2]
        history_dict["result"] = row[3]
        history_dict["sentence"] = row[4]

    return HttpResponse(json.dumps(response))


