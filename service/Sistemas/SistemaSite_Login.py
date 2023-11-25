import flask
from repository import user
from ..Errors.erros import EmailNotFound, WrongPassword, EmptyLoginFields
import hashlib as hl

"""
Sistema de Login
    """
class Sistema_Login(object):
    def __init__(self) -> None:
        """
        Inputs da página de login
            """
        # input email
        self.email_login = flask.request.form.get("login_email")

        # input senha
        self.senha_login =  flask.request.form.get("login_senha")

        """
        Transformar variavel em código hash
            """
        self.senha_hash = (lambda senha: hl.md5(b'%s' %bytes(senha.encode())).hexdigest())
    
    """
    Verificação login do usuário
        """
    def Verificar_Login(self):
        try:
            if self.email_login == "admin@gmail.com":
                if not self.senha_login == "admin1234":
                    return flask.render_template("PaginaLogin.html", error="Senha de usuário errada")
                else:
                    self.criar_cookies_admin = flask.make_response(flask.redirect("/correios"))

                    self.criar_cookies_admin.set_cookie("email admin", self.email_login)

                    return self.criar_cookies_admin
            # verificar se algum campo está vazio
            elif self.email_login == "" or self.senha_login == "":
                raise EmptyLoginFields
            # verificar se a conta existe
            elif user.banco_nosql.Pegar_Informações_Usuario(self.email_login) == []:
                raise EmailNotFound
            # verificar se a senha está certa
            elif not self.senha_hash(self.senha_login) == user.banco_nosql.Pegar_Informações_Usuario(self.email_login)[0]["Senha-user"]:
                raise WrongPassword
            
        except EmailNotFound:
            return flask.render_template("PaginaLogin.html", error="Email não existente")
        except WrongPassword:
            return flask.render_template("PaginaLogin.html", error="Senha de usuário errada")
        except EmptyLoginFields:
            return flask.render_template("PaginaLogin.html", error="Algum campo não foi preencido")
        else:
            """
            criar cookies
                """
            self.criação_de_cookies = flask.make_response(flask.redirect("/emporio")) 

            self.criação_de_cookies.set_cookie("email user", self.email_login)
            
            return self.criação_de_cookies