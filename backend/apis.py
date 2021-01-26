from os import listdir
from django.http import HttpResponse
import os
import json

def get(request):

    apis = []
    for file in listdir('./apis/'):
        apis.append(os.path.splitext(file)[0])

    return HttpResponse(json.dumps(apis))



