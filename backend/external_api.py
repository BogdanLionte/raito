from django.http import HttpResponse

def query(request, api):
    return HttpResponse('{\"sal\": \"pa\"}')
