from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def test(request):

    import pdb;pdb.set_trace()
    return HttpResponse('ok')