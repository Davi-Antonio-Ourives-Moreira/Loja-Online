import mercadopago
import logging
from .produtos import Produtos

"""
Classe de pagamentos
    """
class Pagamentos(Produtos):
    def __init__(self) -> None:
        """
        Configurar logging
            """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

        """
        TOKENS
            """
        # ler o arquivo com o token
        with open("informações_mercadopago.txt", "r", encoding="utf-8") as file:
            self.token = file.read()
            
    """
    Pagamentos
        """ 
    def Pagamentos(self, **kwargs):
        # informações dos produtos
        produtos = Produtos(kwargs["produto"],
                            kwargs["preco"]) 
        """
        Configurações do SDK
            """
        # Configure as credenciais
        sdk = mercadopago.SDK(self.token)

        # Crie um item na preferência
        preference_data = {
            "items": [
                {
                    "title": produtos.produto,
                    "quantity": 1,
                    "unit_price": produtos.preco
                }
            ]
        }

        """
        Gerar a url
            """
        preference_response = sdk.preference().create(preference_data)
        url_pagamento = preference_response["response"]["init_point"]

        """
        Informar que o link foi criado
            """
        logging.info("Link criado com sucesso!")

        return url_pagamento