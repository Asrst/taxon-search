from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Tax on search index.")
