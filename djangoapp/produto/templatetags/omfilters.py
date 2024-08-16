from django.template import Library
from utils import utils # type: ignore

register = Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)