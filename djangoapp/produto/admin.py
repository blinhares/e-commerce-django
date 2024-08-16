from django.contrib import admin
from .models import Produto, Variacao

class VariacaoInLIne(admin.TabularInline):
    """Criar In Line com o model de Variação"""
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    """Classe de Produto Para mostrar o Inline"""
    list_display = [
        'nome',
        'tipo',
        'descricao_curta',
        'get_preco_formatado',
        'get_preco_promocional_formatado'
                    ]
    inlines = [
        VariacaoInLIne
    ]

# Register your models here.
admin.site.register(
    Produto, 
    ProdutoAdmin#classe a ser utilizada no model produtos
    ) 
admin.site.register(Variacao)
