from os import listdir
from django.http import HttpResponse
import os
import json
from authentication import is_authorized
from authentication import http_method_list


@http_method_list(["GET"])
@is_authorized
def get(request):

    apis = []
    for file in listdir('./apis/'):
        apis.append(os.path.splitext(file)[0])

    return HttpResponse(json.dumps(apis))



