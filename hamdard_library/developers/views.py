from django.shortcuts import render

# Create your views here.


def api_docs(request):
    return render(request, 'developers/api_docs.html')

def developers(request):
    return render(request, 'developers/for-developers.html')