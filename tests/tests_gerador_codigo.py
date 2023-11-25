import pytest

def tests_type_codigo():
    import string
    import random

    codigo = ""
    tamanho = 5

    
    for _ in range(tamanho):
        codigo += str(random.randint(0, 9))
        codigo += string.ascii_uppercase[random.randint(1, 25)]
    
    assert type(codigo) == str