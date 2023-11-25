from pymongo import MongoClient

"""
Banco de dados para admin
    """
class Banco_Admin(object):
    def __init__(self) -> None:
        """
        Conectar banco nosql
            """
        # uri do banco
        self.uri = "mongodb://localhost:27017"

        # cliente
        self.admin = MongoClient(self.uri)

        # entrar no banco
        self.db = self.admin["admin"]

        # entrar na coluna
        self.collections = self.db.get_collection("informações-pedidos")

    """
    Adicionar pedidos no site admin
        """
    def Adicionar_Pedidos(self, **kwargs):
        data_dict_pedidos = {
            "Email": kwargs["email"],
            "Produto": kwargs["produto"],
            "Cep": kwargs["cep"],
            "Rua": kwargs["rua"],
            "Bairro": kwargs["bairro"],
            "Numero de residencia": kwargs["numero_residencia"],
            "Complemento": kwargs["complemento"]
        }

        """
        Adicionar
            """
        self.collections.insert_one(data_dict_pedidos)
    
    """
    Remover pedidos entregues
        """
    def Remover_Pedidos(self, email, produto):
        """
        Filtro de remoção
            """
        self.filtro_pedido = {
            "Email": email, 
            "Produto": produto
        }
        
        """
        Remover
            """
        self.collections.delete_one(self.filtro_pedido)
    
        
    """
    Coletar as informações dos pedidos
        """
    def Pegar_Informacoes_Todos_Pedidos(self):
        self.pedidos = self.collections.find()

        self.pedidos = list(self.pedidos)

        return self.pedidos
    
"""
Rodar banco nosql
    """
banco_nosql_admin = Banco_Admin()