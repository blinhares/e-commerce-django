def formata_preco(val): # type: ignore
    return f'R$ {val:.2f}'.replace('.', ',')


def cart_total_qtd(carrinho):# type: ignore
    return sum([item['quantidade'] for item in carrinho.values()])# type: ignore


def cart_totals(carrinho):# type: ignore
    return sum(
        [
            (item.get('preco_quantitativo_promocional') 
             if item.get('preco_quantitativo_promocional') 
             else item.get('preco_quantitativo') 
             for item in carrinho.values())
        ] # type: ignore
    )

def cart_totals(carrinho):
    return sum(
        [
            p_promo
            if (p_promo:= item.get('preco_quantitativo_promocional'))
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )