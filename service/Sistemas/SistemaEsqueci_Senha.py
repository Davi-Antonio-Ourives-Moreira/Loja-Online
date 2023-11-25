import flask
from repository import user
import hashlib as hl
import re
from service.Errors.erros import NonExistentEmail, EmptyEmailFields, EmailNotRegistered, EmptyCodeFields, WrongCode, EmptyPasswordFields, DifferentPasswords, ThePasswordCannotBeTheSameAsThePreviousOne
from random import randint
import string
from email.message import Message
import smtplib
import logging

"""
Sistema esqueci senha
    """
class Sistema_EsqueciSenha(object):
    def __init__(self) -> None:
        """
        Configurar logging
            """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

        """
        Inputs
            """
        # inputs email
        self.input_email =  flask.request.form.get("input_email_esquecisenha")

        # inputs codigo
        self.input_codigo = flask.request.form.get("input_codigo")

        # input nova senha
        self.input_nova_senha = flask.request.form.get("input_mudar_senha")

        # input confirmação da nova senha
        self.input_confirmacao_nova_senha = flask.request.form.get("input_confirmar_mudar_senha")

        """
        Transformar em código hash
            """
        self.senha_hash = (lambda senha: hl.md5(b'%s' %bytes(senha.encode())).hexdigest())

    """
    Verificar email 
        """
    def Verificar_Email(self):
        try:
            if self.input_email == "":
                raise EmptyEmailFields
            elif not re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", self.input_email):
                raise NonExistentEmail
            elif user.banco_nosql.Pegar_Informações_Usuario(self.input_email) == []:
                raise EmailNotRegistered
            
        except EmptyEmailFields:
            return flask.render_template("EsqueciSenha.html", error="O campo não foi preencido")
        except NonExistentEmail:
            return flask.render_template("EsqueciSenha.html", error="Email não existente")
        except EmailNotRegistered:
            return flask.render_template("EsqueciSenha.html", error="Email não foi cadastrado")
        else:
            """
            Informar que o codigo foi adicionado no banco de dados
                """
            logging.info("Codigo adicionado com sucesso!")

            """
            Gerar codigo
                """
            self.code_use = self.Gerar_Código()

            """
            Gravar o código no banco de dados
                """
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.input_email, "Code-esqueci-senha", self.code_use)
            
            """
            Criar cookies
                """
            self.criação_de_cookies = flask.make_response(flask.redirect("/esqueci_senha/codigo")) 

            self.criação_de_cookies.set_cookie("email user", self.input_email)
            
            """
            Mandar email para o email que o usuário selecionou
                """
            self.Mandar_Email(self.input_email,  
                                f"""
                                <p>Use esse código:{self.code_use} de verificação para poder mudar sua senha de usuário!</p>
                                """)

            return self.criação_de_cookies
              
    """
    Gerar código de verificação
        """
    def Gerar_Código(self):
        # codigo ainda vazio
        self.codigo = ""

        # tamanho do codigo
        self.tamanho = 5

        """
        gerar o codigo aleatoriamente
            """
        for _ in range(self.tamanho):
            self.codigo += str(randint(0, 9))
            self.codigo += string.ascii_uppercase[randint(1, 25)]
        
        return self.codigo
       
    """
    Mandar o código para o email 
        """
    def Mandar_Email(self, email_usuario, mensagem):
        # corpo da mensagem do meu email
        corpo_mensagem = mensagem

        # email message
        msg_email = Message()

        # assunto do email
        msg_email["Subject"] = "Código de verificação"

        # de - quem mandou a mensagem
        msg_email["From"] = "daviantoniomoreira4@gmail.com"

        # para - quem receber o email
        msg_email["To"] = email_usuario

        # senha do email de quem vai enviar a mensagem
        password = "maqc mjvq hbed wwbd"

        # header
        msg_email.add_header("Content-Type", "text/html")

        # selecionar mensagem
        msg_email.set_payload(corpo_mensagem)

        # smtplib informações
        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()

        # fazer login na conta que for enviar o email
        s.login(msg_email["From"], password)

        # enviar o email
        s.sendmail(msg_email["From"], # de
                   msg_email["To"],   # para
                   msg_email.as_string().encode("utf-8"), # formato da mensagem
                   )
        
        """
        Informar que o email foi enviado com sucesso
            """
        logging.info(f"Email foi enviado para {email_usuario} com sucesso!")

    """
    Verificação do código
        """
    def Verificar_Código(self):
        # cookies
        COOKIES = flask.request.cookies.get("email user")

        # pegar código
        code_leitura = user.banco_nosql.Pegar_Informações_Usuario(COOKIES)

        code = code_leitura[0]["Code-esqueci-senha"]

        try:
            if self.input_codigo == "":
                raise EmptyCodeFields
            elif not self.input_codigo == code:
                raise WrongCode

        except EmptyCodeFields:
            return flask.render_template("ColocarCodigo.html", error="O campo está vazio")
        except WrongCode:
            return flask.render_template("ColocarCodigo.html", error="O código está errado")
        else:
            """
            Informar que o código está correto
                """
            logging.info("código correto")

            """
            Resetar  código 
                """
            user.banco_nosql.Atualizar_Informações_Do_Usuario(COOKIES, "Code-esqueci-senha", None)

            return flask.redirect("/mudar-senha")

    """
    Verificar a mudança de senha
        """
    def Verificar_Mudança_De_senha(self):
        # Cookies
        COOKIES = flask.request.cookies.get("email user")

        try:
            if self.input_nova_senha == "" or self.input_confirmacao_nova_senha == "":
                raise EmptyPasswordFields
            elif self.input_nova_senha != self.input_confirmacao_nova_senha:
                raise DifferentPasswords
            elif self.senha_hash(self.input_confirmacao_nova_senha) == user.banco_nosql.Pegar_Informações_Usuario(COOKIES)[0]["Senha-user"]:
                raise ThePasswordCannotBeTheSameAsThePreviousOne
            
        except EmptyPasswordFields:
            return flask.render_template("MudarSenha.html", error="Algum campo não foi preencido")
        except DifferentPasswords:
            return flask.render_template("MudarSenha.html", error="O campo de confirmar senha está diferente do campo da senha")
        except ThePasswordCannotBeTheSameAsThePreviousOne:
            return flask.render_template("MudarSenha.html", error="O campo de confirmar senha está diferente do campo da senha")
        else:
            """
            Trocar senha
                """
            user.banco_nosql.Atualizar_Informações_Do_Usuario(COOKIES, "Senha-user", self.senha_hash(self.input_confirmacao_nova_senha))

            """
            Informar que senha foi mudada
                """
            logging.info("Senha foi mudada com sucesso!")

            return flask.redirect("/logar")