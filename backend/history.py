from django.http import HttpResponse
from authentication import http_method_list
import json

@http_method_list(["GET"])
def get(request):

    rows = read_queries()
    response = {}

    for row in rows:
        response["user"] = row[0]
        response["api"] = row[1]
        response["result"] = row[2]
        response["sentence"] = row[3]

    return HttpResponse(json.dumps(response))


