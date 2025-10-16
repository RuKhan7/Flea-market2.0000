from django.shortcuts import HttpResponse

# Create your views here.

def root(request):
    first_compoud = request.GET['a']
    second_compoud = request.GET['b']
    result = first_compoud + second_compoud

    return HttpResponse(str(result))




