import flask
import hashlib as hl
from repository import user
from ..Errors.erros import NonExistentEmail, DifferentPasswords, EmptyRegistrationFields, EmailAlreadyUsed
import re

"""
Sistema de Cadastro
    """
class Sistema_Cadastro(object):
    def __init__(self) -> None:
        """
        Inputs
            """
        # input nome
        self.nome_cadastro = flask.request.form["cadastro_user"]

        # input emali
        self.email_cadastro =  flask.request.form.get("cadastro_email")

        # input senha
        self.senha_cadastro = flask.request.form.get("cadastro_senha")

        # input confirmar senha
        self.confirmar_senha = flask.request.form.get("confirmar_senha")

        """
        Transformar variavel em código hash
            """
        self.senha_hash = (lambda senha: hl.md5(b'%s' %bytes(senha.encode())).hexdigest())
        
    """
    verificar cadastro do usuário
        """
    def Verificar_Cadastro(self):
        try:
            # verificar se algumk campo está vazio
            if self.nome_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirmar_senha == "":
                raise EmptyRegistrationFields
            # verificar se o que foi escrito no input email é mesmo um email
            elif not re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", self.email_cadastro):
                raise NonExistentEmail
            # verificar se já existe uma conta utilizando o email
            elif not user.banco_nosql.Pegar_Informações_Usuario(self.email_cadastro) == []:
                raise EmailAlreadyUsed
            # verificar se o input confirmar senha tem o mesmo valor do que o input senha
            elif not self.confirmar_senha == self.senha_cadastro:
                raise DifferentPasswords
                        
        except NonExistentEmail:
            return flask.render_template("PaginaCadastro.html", error="Email não existente")
        except DifferentPasswords:
            return flask.render_template("PaginaCadastro.html", error="Os campos de senhas estão diferentes")
        except EmptyRegistrationFields:
            return flask.render_template("PaginaCadastro.html", error="Algum campo não foi preencido")
        except EmailAlreadyUsed:
            return flask.render_template("PaginaCadastro.html", error="Email já está sendo utilizado")
        else:
            """
            Adicionar no bancos
                """
            user.banco_nosql.Adicionar_Usuario(email_user=self.email_cadastro,                       ####
                                               nome_user=self.nome_cadastro,                         #### Informações de cadastro do usuário
                                               senha_user=self.senha_hash(self.senha_cadastro),      ####
                                               
                                               cep_user=None,                                        ####
                                               rua_user=None,                                        ####
                                               bairro_user=None,                                     #### Informações de endereço do usuário
                                               numero_residencia_user=None,                          #### 
                                               complemento_user=None,                                ####
                                                                                                              
                                               produtos_carrinho_user=[],                            #### Informações do carrinho do usuário
                                               
                                               codigo_esqueci_senha=None                             #### Informações do código(esqueci senha)
                                               )

            """
            Criar cookies
                """
            self.criação_de_cookies = flask.make_response(flask.redirect("/emporio")) 

            self.criação_de_cookies.set_cookie("email user", self.email_cadastro)
            
            return self.criação_de_cookies
