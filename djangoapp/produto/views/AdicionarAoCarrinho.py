from typing import Any
from django.shortcuts import render, redirect, reverse, get_object_or_404  # type: ignore
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto import models # type: ignore

#TODO remover
from pprint import pprint


# Create your views here.
class AdicionarAoCarrinho(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.carrinho = {}
        self.variacao_id = ''

    def get_variacao_id(self):
        '''Coletar id da variacao do produto'''
        self.variacao_id = self.request.GET.get('vid')
    
    def load_or_create_carrinho(self):
        '''
        Verifica se existe uma seção aberta do carrinho. 
        Se existir, carrega, se nao existir cria.
        O carrinho é armazenado dentro da variável _`self.carrinho`_'''

        #verificando se já há uma seção com nome carrinho
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        self.carrinho = self.request.session['carrinho']
    
    def add_item_carrinho(self, variacao_produto):
        '''Adiciona um item ao carrinho e salva.'''

        produto = variacao_produto.produto

        chaves = {
            'produto_id' : produto.id,
            'produto_nome' : produto.nome,
            'variacao_nome': variacao_produto.nome or '',
            'variacao_id' : variacao_produto.id,
            'preco_unitario' : variacao_produto.preco,
            'preco_unitario_promocional' : variacao_produto.preco_promocional,
            'preco_quantitativo' : variacao_produto.preco,
            'preco_quantitativo_promocional' : variacao_produto.preco_promocional ,
            'quantidade' : 1,
            'slug' : produto.slug,
            'imagem' : produto.imagem.name if produto.imagem else '',
            }

        if self.variacao_id in self.carrinho:

            qtd_carrinho = self.carrinho[self.variacao_id]['quantidade']
            qtd_carrinho += 1

            if variacao_produto.estoque < qtd_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque do {variacao_produto.produto.nome} Insuficiente'
                )
                qtd_carrinho = variacao_produto.estoque
            
            self.carrinho[self.variacao_id]['quantidade'] = qtd_carrinho
            self.carrinho[self.variacao_id]\
                ['preco_quantitativo'] = qtd_carrinho * self.carrinho[self.variacao_id]\
                ['preco_unitario']
            
            self.carrinho[self.variacao_id]\
                ['preco_quantitativo_promocional'] = qtd_carrinho * self.carrinho[self.variacao_id]\
                ['preco_unitario_promocional']
        else:
            self.carrinho[self.variacao_id] = chaves


    def salvar_carrinho(self):
        '''Salva o carrinho'''
        self.request.session.save()

    def deletar_carrinho(self):
        if self.request.session.get('carrinho'):
            del self.request.session['carrinho']
            self.salvar_carrinho()

    def get(self, *args, **kwargs):
        
        #TODO remover
        # self.deletar_carrinho()
        
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
            )
        
        self.get_variacao_id()
        
        #TODO esse if é descessessario uma vez que na 
        # funcao get_object_or_404 é emitido um ERRO 
        # caso o id n seja encontrado
        # if not self.variacao_id:
        #     messages.error(
        #         self.request,
        #         'Produto Inexistente.'
        #     )
        # #####

        variacao_produto = get_object_or_404(
            models.Variacao,
            id=self.variacao_id
        )

        #TODO - adicionar essa condição no view da pagina
        if variacao_produto.estoque < 1:
            messages.error(
                self.request,
                'Estoque do Produto Insuficiente'
            )
            return redirect(http_referer)

        self.load_or_create_carrinho()

        self.add_item_carrinho(variacao_produto=variacao_produto)

        self.salvar_carrinho()

        messages.success(
            self.request,
            f'{self.carrinho[self.variacao_id]["quantidade"]} Produto(s)'
            f' {variacao_produto.produto.nome} - {variacao_produto.nome}'
            f' adicionado(a) ao carrinho.',
            )

        #redireciona a pagina anterior
        return redirect(http_referer)

        
