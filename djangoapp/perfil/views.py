from typing import Any
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import forms, models
import copy

class BasePerfil(View):
    template_name = 'perfil/criar.html'


    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.perfil = None

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))

        if self.request.user.is_authenticated:

            self.template_name = 'perfil/atualizar.html'

            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user).first()
            
            self.contexto = {'userform':forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance = self.request.user 
                    ),
                    'perfilform':forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                    )
                    }
        
        else:

            self.contexto = {'userform':forms.UserForm(
                    data=self.request.POST or None
                    ),
                    'perfilform':forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                    )
                    }
            
        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto)
    
    def get(self, *args, **kwargs):
        return self.renderizar
    
class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            print('INVALIDO')
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')

        #usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)
                
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfilform.cleaned_data['usuario']=usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
        #nao logado
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=username, 
                password=password)
            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        messages.success(
            self.request,
            'Cadastro Criado/Atualizado com sucesso!'
        )
        return redirect('perfil:criar')
        return self.renderizar

        

class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse(self.__class__.__name__)

class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if not username or not password:
            messages.error(self.request,
                           'Usuario e/ou senha invalido')
            return redirect('perfil:criar')
        usuario = authenticate(self.request, username=username, password= password)
        if not usuario:
            messages.error(self.request,
                           'Usuario e/ou senha invalido')
            return redirect('perfil:criar')

        login(self.request, user=usuario)

        messages.success(
            self.request,
            'Login realizado com sucesso!'
        )
        return redirect('produto:carrinho')


class Logout(View):
    def get(self, *args, **kwargs):
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))
        logout(self.request)
        self.request.session['carrinho'] = self.carrinho 
        self.request.session.save()
        return redirect('produto:lista')