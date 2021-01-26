from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
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
