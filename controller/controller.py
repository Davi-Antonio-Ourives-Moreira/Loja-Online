import flask
from service.Sistemas.SistemaSite_Cadastro import Sistema_Cadastro
from service.Sistemas.SistemaSite import Sistema_Site
from service.Sistemas.SistemaSite_Login import Sistema_Login
from service.Sistemas.SistemaEsqueci_Senha import Sistema_EsqueciSenha
from service.Correios.correios import Correios
from repository import user

app =  flask.Flask(__name__)

app.config["SECRET_KEY"] = "minha-palavra-secreta"

"""
Página home
    """
@app.get("/")
def homepage():
    return flask.redirect("/cadastrar")

"""
Página de cadastro
    """
# página de cadastro - get
@app.get("/cadastrar")
def cadastrar():
    return flask.render_template("PaginaCadastro.html")

# sistema de cadastrar usuario - post
@app.post("/cadastrando")
def cadastrando():
    sistema_cadastro = Sistema_Cadastro()

    return sistema_cadastro.Verificar_Cadastro()

"""
Página de login
    """
# página de login - get
@app.get("/logar")
def logar():
    return flask.render_template("PaginaLogin.html")

# sistema de logar na conta do usuário - post
@app.post("/logando")
def logando():
    sistema_login =  Sistema_Login()

    return sistema_login.Verificar_Login()

"""
Página esqueci senha
    """
# pagina esqueci senha - get
@app.get("/esqueci_senha/email")
def pagina_esqueci_senha():
    return flask.render_template("EsqueciSenha.html")

# sistema de verificar email - post
@app.post("/verification-authentiom-email")
def autenticacao_email():
    sistema_esqueci_senha_email = Sistema_EsqueciSenha()

    return sistema_esqueci_senha_email.Verificar_Email()

# pagina colocar codigo - get
@app.get("/esqueci_senha/codigo")
def pagina_codigo():
    return flask.render_template("ColocarCodigo.html")

# sistema de verificar codigo - post
@app.post("/verificando-atheunt-code")
def autenticacao_codigo():
    sistema_esqueci_senha_codigo = Sistema_EsqueciSenha()

    return sistema_esqueci_senha_codigo.Verificar_Código()

# pagina mudar senha - get
@app.get("/mudar-senha")
def pagina_mudarsenha():
    return flask.render_template("MudarSenha.html")

# sistema de mudar senha - post
@app.post("/verification-mudantion-senha")
def verificacao_mudar_senha():
    sistema_mudar_senha = Sistema_EsqueciSenha()

    return sistema_mudar_senha.Verificar_Mudança_De_senha()

"""
Página do site
    """
# página do site - get
@app.get("/emporio")
def site():
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    
    sistema_site = Sistema_Site(COOKIES)
        
    return sistema_site.Pagina_Inicial()


"""
Adicionar produto no carrinho
    """
# sistema de adicionar produtos no carrinho - post
@app.get("/carrinho/<produto_carrinho>/<preco>/<peso>/<image>")
def carrinho_produto(produto_carrinho, preco, peso, image):
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_adicionar_produto_carrinho = Sistema_Site(COOKIES)

        return sistema_adicionar_produto_carrinho.Adicionar_Produtos_Carrinho(produto_carrinho, preco, peso, image)
    
"""
Remover produto do carrinho
    """
# sistema de remover produto no carrinho - post
@app.post("/remover/<remove_produto>/<remove_preco>/<remove_peso>/<remove_image>")
def remover_carrinho(remove_produto, remove_preco, remove_peso, remove_image):
    """
    Pegar cookies
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_remover_produtos_carrinho = Sistema_Site(COOKIES)

        return sistema_remover_produtos_carrinho.Remover_Produtos_Carrinho(remove_produto, remove_preco, remove_peso, remove_image)

"""
Apagar todos os produtos do carrinho
    """
# sistema de apagar todo o carrinho - post
@app.post("/apagar-carrinho")
def apagar_carrinho():
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        """
        Deletar todos os produtos do carrinho
            """
        user.banco_nosql.Deletar_Produtos_Carrinho_De_Compras_Usuario(COOKIES, [])
        
        return flask.redirect("/emporio")

"""
Pagar pelos produtos
    """
# página pagar pelo produto - get
@app.get("/prod/<produto>/<preco>/<quantidade>")
def prod_produto(produto, preco, quantidade):
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_pagamento = Sistema_Site(COOKIES)

        return sistema_pagamento.Pagar_Produto_Separado([produto, float(preco), quantidade])

# sistema de pagamento de todos os produtos do carrinho produtos - post
@app.post("/comprar-carrinho")
def comprar_carrinho():
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_pagamento = Sistema_Site(COOKIES)

        return sistema_pagamento.Pagar_Produto_Carrinho()


"""
Filtro de seleção de produtos
    """
# pagina queijos
@app.get("/queijos")
def queijos():
    filtro = "Queijos"

    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_filtro = Sistema_Site(COOKIES)

        return sistema_filtro.Filtro_Pesquisa(filtro)


# pagina temperos
@app.get("/temperos")
def temperos():
    filtro = "Temperos"

    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_filtro = Sistema_Site(COOKIES)

        return sistema_filtro.Filtro_Pesquisa(filtro)
    

# pagina graos
@app.get("/graos")
def graos():
    filtro = "Grãos"

    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_filtro = Sistema_Site(COOKIES)

        return sistema_filtro.Filtro_Pesquisa(filtro)
    

# pagina ervas
@app.get("/ervas")
def ervas():
    filtro = "Ervas"

    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_filtro = Sistema_Site(COOKIES)

        return sistema_filtro.Filtro_Pesquisa(filtro)
    
"""
Sistema de cadastrar endereço do usuario
    """
# sistema de cadastrar endereço
@app.post("/cadastrar-endereco")
def cadastrar_endereco():
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_cadastrar_cep = Sistema_Site(COOKIES)

        return sistema_cadastrar_cep.Cadastrar_Endereco()

# sistema de trocar endereço
@app.post("/trocar-endereco")
def trocar_endereco():
    """
    Verificar se o usuario está logado
        """
    # cookies
    COOKIES = flask.request.cookies.get("email user")

    # verificar
    if COOKIES == None:
        return flask.redirect("/logar")
    else:
        sistema_de_trocar_cep = Sistema_Site(COOKIES)

        return sistema_de_trocar_cep.Trocar_Endereco()

"""
Página correios
    """
# pagina correios - get
@app.get("/correios")
def page_correios():
    COOKIES_ADMIN = flask.request.cookies.get("email admin")

    if COOKIES_ADMIN == None:
        return flask.redirect("/logar")

    sistema_correios = Correios()

    return sistema_correios.Pagina_Correios()

# remover produto correios - post
@app.post("/remove-pedido/<email>/<produto>")
def remover_pedido(email, produto):
    sistema_remover_pedido = Correios()

    return sistema_remover_pedido.Remover_Produto_Pagina(email, produto)
