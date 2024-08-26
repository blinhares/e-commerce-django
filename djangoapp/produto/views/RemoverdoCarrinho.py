from typing import Any
from django.shortcuts import render, redirect, reverse, get_object_or_404  # type: ignore
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages



# Create your views here.
class RemoverDoCarrinho(View):
    variacao_id = ''
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.carrinho = {}

    def retornar_a_pagina_origen(self):
        '''Retorna a pagina de origem '''
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
            )
        return redirect(http_referer)

    def carrinho_existe(self):
        '''
        Verifica se existe uma seção aberta do carrinho. 
        Se existir, carrega, se nao existir cria.
        O carrinho é armazenado dentro da variável _`self.carrinho`_'''

        #verificando se já há uma seção com nome carrinho
        if not self.request.session.get('carrinho'):
            self.retornar_a_pagina_origen()
        
    def get_variacao_id(self):
        '''Coletar id da variação do produto e caso n 
        haja retorna a pagina de origem'''
        self.variacao_id = self.request.GET.get('vid')

        if self.variacao_id == '':
            self.retornar_a_pagina_origen()
    
    def remover_item_carrinho(self):
        '''Verifica se a variação do item esta no carrinho e o remove.'''
        if self.variacao_id not in (carrinho:=self.request.session['carrinho']):
            self.retornar_a_pagina_origen()
        
        messages.success(
            self.request,
            f'Produto {carrinho[self.variacao_id]["produto_nome"]} - '\
            f'{carrinho[self.variacao_id]["variacao_nome"]}'
            ' removido do carrinho'
        )

        del carrinho[self.variacao_id]

        self.request.session.save() 


    def get(self, *args, **kwargs):

        self.carrinho_existe()

        self.get_variacao_id()        

        self.remover_item_carrinho()      

        return self.retornar_a_pagina_origen()
