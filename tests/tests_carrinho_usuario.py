

def test_carrinho():
    """
    Verificar como fica varis listas vazias no zip
        """
    lista1 = []
    lista2 = []
    lista3 = []

    lista_total = list(zip(lista1, lista2, lista3))

    assert lista_total == [] 

def test_zip_carrinho():
    """
    Verificar como fica varias listas vazias no zip no for
        """
    lista1 = []
    lista2 = []
    lista3 = []

    lista_total = list(zip(lista1, lista2, lista3))

    for a, _, _ in lista_total:
        assert a == ""

def test_soma_lista():
    lista_soma = []

    assert float(sum(lista_soma)) == 0.00

    


