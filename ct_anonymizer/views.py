from django.shortcuts import render

__author__ = 'dipap'


def index(request):
    return render(request, 'index.html')
