from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


# Create your views here.
class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse(self.__class__.__name__)
