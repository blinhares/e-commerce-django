from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse



# Create your views here.
class Carrinho(View):
    template_name = 'produto/carrinho.html'
    context_object_name = 'carrinho'

    def get(self, *args, **kwargs):
        #TODO verfificar se enviar o contexto por aqui reduz o 
        # numero de requisições ao banco de dados
        # contexto = {
        #     'carrinho': self.request.session.get('carrinho',{})
        # }
        return render(
            self.request,
            self.template_name,
            # contexto
            )
        
