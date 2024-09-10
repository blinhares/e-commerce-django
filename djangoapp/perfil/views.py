from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse
from . import models
from . import forms

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)

        if self.request.user.is_authenticated:

            self.contexto = {
                'userform':forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance = self.request.user 
                    ),
                'perfilform':forms.PerfilForm(
                    data=self.request.POST or None
                    ),
            }

        else:

            self.contexto = {
                'userform':forms.UserForm(
                    data=self.request.POST or None
                    ),
                'perfilform':forms.PerfilForm(
                    data=self.request.POST or None
                    ),
            }

        

        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto)
    
    def get(self, *args, **kwargs):
        return self.renderizar
    
class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar

        

class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse(self.__class__.__name__)

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse(self.__class__.__name__)

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse(self.__class__.__name__)