from django.http import HttpResponse
from authentication import http_method_list

@http_method_list(["GET"])
def get(request):

    return HttpResponse("[ {\"query\": \"give me something\", \"api\": \"json\", \"response\": \"here is a response\"}, {\"content\": 24}]")


