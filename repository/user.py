from pymongo import MongoClient

"""
Banco de dados
    """
class Banco(object):
    def __init__(self) -> None:
        """
        conectar banco nosql
            """
        # uri do banco
        self.uri = "mongodb://localhost:27017"

        # cliente
        self.cliente = MongoClient(self.uri)

        # entrar no banco
        self.db = self.cliente["Clientes"]

        # entrar coluna
        self.collections = self.db.get_collection("Informações-clientes")

    """
    Criar meu banco nosql
        """
    def Criar_Banco(self):
        self.db = self.cliente.get_database("Clientes")

        print("Database criada")

    """
    criar minha tabela no banco
        """
    def Criação_Tabela(self):
        self.coluna = self.db.create_collection("Informações-clientes")

        print("Coluna criada")
    
    """
    Adicionar informações de usuário no banco
        """    
    def Adicionar_Usuario(self, **kwargs):
        """
        Informações dos clientes
            """
        data_dict = {
            
            # email do usuario
            "email": kwargs["email_user"], ### informações email

            # nome do usuario
            "Nome-user": kwargs["nome_user"],   ###
                                                ### informações do usuario - nome e senha
            # senha do usuario                  ###
            "Senha-user": kwargs["senha_user"], ###

            # endereço do usuario
            "Cep-user": kwargs["cep_user"],                                             ###
            "Rua-user": kwargs["rua_user"],                                             ###            
            "Bairro-user": kwargs["bairro_user"],                                       ### informações do usuario - endereço
            "Numero-de-residencia-user": kwargs["numero_residencia_user"],              ###
            "Complemento-user": kwargs["complemento_user"],                             ###

            # informações carrinho do usuario
            "Produtos-carrinho-user": kwargs["produtos_carrinho_user"],                 ###  informações do usuario - carrinho de compras
        
            # Código
            "Code-esqueci-senha": kwargs["codigo_esqueci_senha"]                        ### informações de código - esqueci senha 
        }
        """
        Adicionar no banco
            """
        self.collections.insert_one(data_dict)


    """
    Atualizar informações do usuário
        """
    def Atualizar_Informações_Do_Usuario(self, email, valor_selecionado, valor_novo):
        """
        Valores da mudança
            """
        # achar pessoa
        self.achar_pessoa_mudança = {"email": email}

        # valor da mudança
        self.novas_informações = {"$set": {valor_selecionado: valor_novo}}
    
        """
        Atualizar valores
            """
        self.collections.update_one(self.achar_pessoa_mudança, self.novas_informações)

    def Atualizar_Carrinho_De_Compras_Usuario(self, email, adicionar):
        """
        Valores da atualização
            """
        # achar pessoa
        self.achar_pessoa_atualização = {"email": email}

        # valor da mudança
        self.novas_informações_atualização = {"$addToSet": {"Produtos-carrinho-user": adicionar}}

        """
        Atualizar valores
            """
        self.collections.update_one(self.achar_pessoa_atualização, self.novas_informações_atualização)

    def Deletar_Produtos_Carrinho_De_Compras_Usuario(self, email, lista):
        # achar a pessoa
        self.achar_pessoa_deletar = {"email": email}

        # deletar o alimento da lista
        self.deletar_informações = {"$set": {"Produtos-carrinho-user": lista}}

        """
        Deletar 
            """
        self.collections.update_one(self.achar_pessoa_deletar, self.deletar_informações)

    """
    pegar as informações do usuário
        """
    def Pegar_Informações_Usuario(self, email):
        """
        Achar usuario
            """
        # informações do usuário
        self.info = self.collections.find({"email": email})

        self.info = list(self.info)

        return self.info
    
"""
Rodar banco nosql
    """
banco_nosql = Banco()

"""
Criações da database
    """
# criação database
##banco_nosql.Criar_Banco()

# criação de coluna
##banco_nosql.Criação_Tabela()