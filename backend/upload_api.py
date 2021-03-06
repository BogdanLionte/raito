from django.http import HttpResponse
from authentication import is_authorized
from authentication import http_method_list


@http_method_list(["POST"])
@is_authorized
def upload(request):
    print(request)
    print(request.FILES.keys())
    print(request.FILES['file'])

    file = request.FILES['file']
    fileName = request.FILES['file'].name

    fileContent = ''
    for line in file:
        fileContent = fileContent + line.decode()

    file = open('./apis/' + fileName, "w")
    file.write(fileContent)

    return HttpResponse('')
