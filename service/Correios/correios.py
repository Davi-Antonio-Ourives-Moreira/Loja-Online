import flask
from repository import user_admin

"""
Correios
    """
class Correios(object):
    def __init__(self) -> None:
        """
        Todos os pedidos
            """
        self.todos_pedidos = user_admin.banco_nosql_admin.Pegar_Informacoes_Todos_Pedidos() 

    def Pagina_Correios(self):
        return flask.render_template("PaginaCorreios.html", todos_pedidos=self.todos_pedidos)

    def Adicionar_Produto_Pagina(self, _email, _produto, _cep, _rua, _bairro, _n_residencia, _complemento):
        user_admin.banco_nosql_admin.Adicionar_Pedidos(email=_email,
                                                       produto=_produto,
                                                       cep=_cep,
                                                       rua=_rua,
                                                       bairro=_bairro,
                                                       numero_residencia=_n_residencia,
                                                       complemento=_complemento)
    
    def Remover_Produto_Pagina(self, email, produto):
        user_admin.banco_nosql_admin.Remover_Pedidos(email, produto)

        return flask.redirect("/correios")