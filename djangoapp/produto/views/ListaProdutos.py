from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


# Create your views here.
class ListaProdutos(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse(f'{self.__class__.__name__}')
