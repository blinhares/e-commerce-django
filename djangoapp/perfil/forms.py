from typing import Any, Mapping
from django import forms
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    #transformar o campo de senha em um dado não exigido
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        label='Senha'
    )
    #confimacao de senha
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        label='Confirmação Senha'
    )
    def __init__(self, usuario=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 
                  'last_name', 
                  'username', 
                  'password', 
                  'password2', 
                  'email')
    def esta_logado(self):
        return self.usuario.is_authenticated # type: ignore

    def dados_ja_existe(self,dado)-> bool:
        """ Verifica se um dado especifico ja existe no banco de dados"""
        data_form = self.cleaned_data.get(dado)
        dicio = dict([(dado,data_form)])  
        data_db =  User.objects.filter(**dicio).first()
        return bool(data_db)

    
    def usuario_ja_existe(self):
        '''Verifica se usuário enviado no formulário existe'''

        if self.dados_ja_existe('username'):
            self.validation_erro_msgs['username'] = "Usuário já existe!"
            return True

        return False
    
    def email_ja_existe(self):
        '''Verifica se email enviado no formulário existe'''
        
        if self.dados_ja_existe('email'):
            self.validation_erro_msgs['email'] = "E-mail já existe!"
            return True

        return False
    
    def senhas_validas(self):
        '''Verifica se as senhas enviadas no formulário são iguais'''
        senha_form = self.cleaned_data.get('password')
        senha_form2 = self.cleaned_data.get('password2')

        if senha_form and senha_form2 and senha_form == senha_form2:
            if len(str(senha_form))< 6:
                self.validation_erro_msgs['password'] = "Senha deve ter no mínimo 6 caracteres!"
                return False
            return True
        
        self.validation_erro_msgs['password'] = "As senhas devem ser iguais!"
        return False

             

    def clean(self, *args, **kwargs): # type: ignore
        data = self.data
        cleaned = self.cleaned_data
        self.validation_erro_msgs = {}


        self.usuario_ja_existe()
        self.senhas_validas()
        self.email_ja_existe()
            

        if self.validation_erro_msgs:
                raise forms.ValidationError(self.validation_erro_msgs)

        # return super().clean()#TODO remover?