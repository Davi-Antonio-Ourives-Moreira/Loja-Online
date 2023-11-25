import flask
from repository import user
import requests
import logging
from service.Pagamentos.pagamento import Pagamentos
from ..Errors.erros import UnregisteredAddress, EmptyZipCode, EmptyStreet, EmptyNeighborhood, EmptyResidenceNumber, SmallZipCode
from ..Correios.correios import Correios

"""
Sistema Site
    """
class Sistema_Site(object):
    def __init__(self, cookies) -> None:
        """
        Configurar logging
            """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

        """
        INPUTS CADASTRAR ENDEREÇO
            """
        # input cep
        self.input_cep = flask.request.form.get("input_cep")

        # input rua
        self.input_rua = flask.request.form.get("input_rua")

        # input bairro
        self.input_bairro = flask.request.form.get("input_bairro")

        # input numero de residencia
        self.input_numero_de_residencia = flask.request.form.get("input_numero_residencia")

        # input complemento
        self.input_complemento = flask.request.form.get("input_complemento")

        """
        INPUTS TROCAR ENDEREÇO
            """
        # input trocar cep
        self.input_cep_trocar = flask.request.form.get("input_cep_novo")

        # input trocarrua
        self.input_rua_trocar = flask.request.form.get("input_rua_novo")

        # input trocar bairro
        self.input_bairro_trocar = flask.request.form.get("input_bairro_novo")

        # input trocar numero de residencia
        self.input_numero_de_residencia_trocar = flask.request.form.get("input_numero_residencia_novo")

        # input trocar complemento
        self.input_complemento_trocar = flask.request.form.get("input_complemento_novo")

        """
        Pegar os cookies do usuário
            """
        self.pegar_cookies = cookies

        """
        Lista de todos os produtos do meu site
            """
        # lista de todos os meus produtos - (nome do produto, preço do produto, peso do produto, imagem do produto)
        self.todos_os_produtos = [
            
        ]

        """
        Informações adicionais do usuário
            """
        self.informações = user.banco_nosql.Pegar_Informações_Usuario(self.pegar_cookies)

        """
        Informações da conta do usuário
            """
        # email conta
        self.email_conta = self.informações[0]["email"]

        # nome da conta do usuário
        self.nome_conta = self.informações[0]["Nome-user"]

        """
        Informações de endereço da conta do usuário
            """
        # cep da conta
        self.cep_conta = self.informações[0]["Cep-user"]

        # endereço da conta
        self.endereço_conta = self.informações[0]["Rua-user"]

        # bairro
        self.bairro_conta = self.informações[0]["Bairro-user"]

        # número de residência
        self.numero_residencia_conta = self.informações[0]["Numero-de-residencia-user"]

        # complemento
        self.complemento_conta = self.informações[0]["Complemento-user"]

        """
        Informações do carrinho
            """
        # produtos no carrinho
        self.produtos_carrinho = self.informações[0]["Produtos-carrinho-user"]

        """ 
        Executar a leitura da api da loja
            """
        self.Ler_APi_Produtos()

    """
    Página inicial da loja-online
        """
    def Pagina_Inicial(self):
        """
        Informar os produtos do meu carrinho
            """        
        logging.info(self.produtos_carrinho)

        """
        Verificar se o cmapo de endereço ja foi preencido
            """
        if self.cep_conta != None:
            """
            Avisos
                """
            flask.flash(self.cep_conta)
            flask.flash(self.endereço_conta)
            flask.flash(self.bairro_conta)
            flask.flash(self.numero_residencia_conta)
            flask.flash(self.complemento_conta)

        return flask.render_template("PaginaSite.html", email=self.email_conta, # pegar o  email da conta
                                     
                                                        nome_conta=self.nome_conta, # pegar o nome da conta

                                                        endereco_conta=self.endereço_conta, # pegar o  endereço da conta

                                                        total_produtos_carrinho_conta=len(self.produtos_carrinho),  # pegar total produtos no carrinho - número,

                                                        produtos_carrinho_conta=self.produtos_carrinho, # pegar todos produtos no carrinho da conta

                                                        soma_preco_produtos_carrinho_conta=str(sum([float(x[0][1]) for x in list(self.produtos_carrinho)])).replace(".", ","), # pegar soma dos preços de todos os produtos da minha lista 

                                                        todos_os_produtos_site=self.todos_os_produtos, # todos os produtos do site
                                                        )
    
    """
    Leitura da api da loja-online
        """
    def Ler_APi_Produtos(self):
        # pegar a url da api
        self.url_api_loja = requests.get(url="http://127.0.0.1:5000/produtos-loja")

        # converter a url em json
        self.url_json = self.url_api_loja.json()

        """
        Adicionar os produtos na lista
            """
        # adicionar os produtos da categoria queijo
        for categoria_queijo in self.url_json["Queijos"]:
            try:
                self.todos_os_produtos.append((categoria_queijo["Produto"], categoria_queijo["Preço"], categoria_queijo["Peso"], categoria_queijo["Imagem"]))
            except KeyError:
                self.todos_os_produtos.append((categoria_queijo["Produto"], categoria_queijo["Preço"], categoria_queijo["Quantidade"], categoria_queijo["Imagem"]))

        # adicionar produtos da categoria temperos
        for categoria_tempero in self.url_json["Temperos"]:
            self.todos_os_produtos.append((categoria_tempero["Produto"], categoria_tempero["Preço"], categoria_tempero["Peso"], categoria_tempero["Imagem"]))
            
        # adicionar produtos da categoria ervas
        for categoria_erva in self.url_json["Ervas"]:
            self.todos_os_produtos.append((categoria_erva["Produto"], categoria_erva["Preço"], categoria_erva["Peso"], categoria_erva["Imagem"]))
        
        # adicionar produtos da categoria grãos
        for categoria_graos in self.url_json["Grãos"]:
            self.todos_os_produtos.append((categoria_graos["Produto"], categoria_graos["Preço"], categoria_graos["Peso"], categoria_graos["Imagem"]))
    
    """
    Filtro de pesquisa
        """
    def Filtro_Pesquisa(self, filtro):
        """
        Verificar se o campo de endereço ja foi preencido
            """
        if self.cep_conta != None:
            """
            Avisos
                """
            flask.flash(self.cep_conta)
            flask.flash(self.endereço_conta)
            flask.flash(self.bairro_conta)
            flask.flash(self.numero_residencia_conta)
            flask.flash(self.complemento_conta)
            
        # lista das informações filtradas
        lista_filtrada =  [

        ]

        """
        Fazer o filtramento
            """
        for categoria_filtro in self.url_json[filtro]:
            try:
                lista_filtrada.append((categoria_filtro["Produto"], categoria_filtro["Preço"], categoria_filtro["Peso"], categoria_filtro["Imagem"]))
            except KeyError:
                lista_filtrada.append((categoria_filtro["Produto"], categoria_filtro["Preço"], categoria_filtro["Quantidade"], categoria_filtro["Imagem"]))

        return flask.render_template(f"Pagina{filtro}.html", produtos_filtrados=lista_filtrada,
                                                            
                                                             email=self.email_conta, # pegar o  email da conta
                                     
                                                             nome_conta=self.nome_conta, # pegar o nome da conta

                                                             endereco_conta=self.endereço_conta, # pegar o  endereço da conta

                                                             total_produtos_carrinho_conta=len(self.produtos_carrinho),  # pegar total produtos no carrinho - número,

                                                             produtos_carrinho_conta=self.produtos_carrinho, # pegar todos produtos no carrinho da conta

                                                             soma_preco_produtos_carrinho_conta=str(sum([float(x[0][1]) for x in list(self.produtos_carrinho)])).replace(".", ",") # pegar soma dos preços de todos os produtos da minha lista
                                                             ) 
    
    """
    Adicionar produtos no carrinho do usuário
        """
    def Adicionar_Produtos_Carrinho(self, new_produto, new_preco, new_peso, new_image):
        """ 
        Adicionar produtos no carrinho
            """
        user.banco_nosql.Atualizar_Carrinho_De_Compras_Usuario(self.pegar_cookies, [(new_produto, new_preco, new_peso, new_image)])

        return flask.redirect("/emporio")

    """
    Remover produtos no carrinho do usuário
        """
    def Remover_Produtos_Carrinho(self, remove_produto, remove_preco, remove_peso, remove_image):
        """
        Remover produto
            """
        # pegar as informações da pessoa
        pegar_informacoes = user.banco_nosql.Pegar_Informações_Usuario(self.pegar_cookies)
        
        # lista dos produtos do carrinho da pessoa
        lista_produtos_carrinho = list(pegar_informacoes[0]["Produtos-carrinho-user"])
        
        # remover produtos do carrinho
        lista_produtos_carrinho.pop(lista_produtos_carrinho.index([[remove_produto, remove_preco, remove_peso, remove_image]]))

        # editar o carrinho com o produto deletado 
        user.banco_nosql.Deletar_Produtos_Carrinho_De_Compras_Usuario(self.pegar_cookies, lista_produtos_carrinho)

        return flask.redirect("/emporio")

    """
    Pagamentos
        """
    # pagar pelo produto separado
    def Pagar_Produto_Separado(self, produto_info: list):
        try:
            if self.endereço_conta == None:
                raise UnregisteredAddress
        except UnregisteredAddress:
            flask.flash("error_endereco")

            return flask.redirect("/emporio")
        else:
            pag = Pagamentos()

            pag_produtos = pag.Pagamentos(produto=produto_info[0],
                                          preco=produto_info[1])
            
            """
            Mandar o produto para o site dos correios
                """
            correios = Correios()

            correios.Adicionar_Produto_Pagina(self.email_conta, # email do usuario que comprou o produto
                                              produto_info[0],  # nome do produto comprado
                                              self.cep_conta,   # cep do comprador
                                              self.endereço_conta, # rua do comprador
                                              self.bairro_conta, # bairro do comprador
                                              self.numero_residencia_conta, # numero de residencia do comprador
                                              self.complemento_conta)  # complemento do comprador
            
            return flask.redirect(pag_produtos)

    # pagar por todos os produtos
    def Pagar_Produto_Carrinho(self):
        """
        Lista carrinho
            """
        # produtos do carrinho
        produtos_carrinho = [

        ]

        # quantidade produtos carrinho
        quantidade_produtos_carrinho = [

        ]

        # preço produtos carrinho
        preco_produtos_carrinho = [

        ]
        
        try:
            if self.endereço_conta == None:
                raise UnregisteredAddress
        except UnregisteredAddress:
            flask.flash("error_endereco")

            return flask.redirect("/emporio")
        else:        
            for pegar_info_produtos in self.produtos_carrinho:
                # adicionar o valor do nome dos produtos
                produtos_carrinho.append(pegar_info_produtos[0][0])

                # adicionar o valor do preço dos produtos
                preco_produtos_carrinho.append(float(pegar_info_produtos[0][1]))

                # adicionar o valor de quantidade dos produtos
                if pegar_info_produtos[0][2].endswith("kg"):
                    quantidade_kg = pegar_info_produtos[0][2][:-2]
                    quantidade_produtos_carrinho.append(int(quantidade_kg)*1000)
                else:
                    try:
                        quantidade_g = pegar_info_produtos[0][2][:-1]
                        quantidade_produtos_carrinho.append(int(quantidade_g))
                    except ValueError:
                        quantidade_g = pegar_info_produtos[0][2]
                        quantidade_produtos_carrinho.append(int(quantidade_g))

        
        pag = Pagamentos()

        correios = Correios()

        if len(produtos_carrinho) > 1:
            produtos = ",".join(produtos_carrinho)
        else:
            produtos = produtos_carrinho[0]

        correios.Adicionar_Produto_Pagina(self.email_conta, # email do usuario que comprou o produto
                                          produtos,  # nome do produto comprado
                                          self.cep_conta,   # cep do comprador
                                          self.endereço_conta, # rua do comprador
                                          self.bairro_conta, # bairro do comprador
                                          self.numero_residencia_conta, # numero de residencia do comprador
                                          self.complemento_conta)  # complemento do comprador

        pag_produtos = pag.Pagamentos(produto=produtos,
                                      preco=sum(preco_produtos_carrinho))
            
        return flask.redirect(pag_produtos)
    def Cadastrar_Endereco(self):
        try:
            if self.input_cep == "":
                raise EmptyZipCode
            elif self.input_rua == "":
                raise EmptyStreet
            elif self.input_bairro == "":
                raise EmptyNeighborhood
            elif self.input_numero_de_residencia == "":
                 raise EmptyResidenceNumber
            elif len(self.input_cep) < 8:
                raise SmallZipCode
            
        except EmptyZipCode:
            flask.flash("campo de cep vazio")

            return flask.redirect("/emporio")
        except EmptyStreet:
            flask.flash("campo de rua vazio")

            return flask.redirect("/emporio")
        except EmptyNeighborhood:
            flask.flash("campo de bairro vazio")

            return flask.redirect("/emporio")
        except EmptyResidenceNumber:
            flask.flash("campo de numero residencia vazio")

            return flask.redirect("/emporio")
        except SmallZipCode:
            flask.flash("cep pequeno")

            return flask.redirect("/emporio")
        else:
            """
            Cadastrar meus endereços
                """
            # cadastrar cep
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Cep-user", self.input_cep)

            # cadastrar rua
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Rua-user", self.input_rua)
            
            # cadastrar bairro
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Bairro-user", self.input_bairro)
            
            # cadastrar numero de residencia
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Numero-de-residencia-user", self.input_numero_de_residencia)

            # cadastrar complemento
            if self.input_complemento == "":
                user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Complemento-user", "")
            else:
                user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Complemento-user", self.input_complemento)
                
            """
            Avisos para enviar no html
                """
            flask.flash(self.input_cep)
            flask.flash(self.input_rua)
            flask.flash(self.input_bairro)
            flask.flash(self.input_numero_de_residencia)
            flask.flash(self.input_complemento)
        
            return flask.redirect("/emporio")
    

    def Trocar_Endereco(self):
        try: 
            if self.input_cep_trocar == "":
                raise EmptyZipCode
            elif self.input_rua_trocar == "":
                raise EmptyStreet
            elif self.input_bairro_trocar == "":
                raise EmptyNeighborhood
            elif self.input_numero_de_residencia_trocar == "":
                 raise EmptyResidenceNumber
            elif len(self.input_cep_trocar) < 8:
                raise SmallZipCode
        except EmptyZipCode:
            return flask.redirect("/emporio")
        except EmptyStreet:
            return flask.redirect("/emporio")
        except EmptyNeighborhood:
            return flask.redirect("/emporio")
        except EmptyResidenceNumber:
            return flask.redirect("/emporio")
        except SmallZipCode:
            return flask.redirect("/emporio")
        else:
            """
            Recadastrar meus endereços
                """
            # recaadastrar cep
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Cep-user", self.input_cep_trocar)

            # recadastrar rua
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Rua-user", self.input_rua_trocar)
            
            # recadastrar bairro
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Bairro-user", self.input_bairro_trocar)
            
            # recadastrar numero de residencia
            user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Numero-de-residencia-user", self.input_numero_de_residencia_trocar)

            # recadastrar complemento
            if self.input_complemento_trocar == "":
                user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Complemento-user", "")
            else:
                user.banco_nosql.Atualizar_Informações_Do_Usuario(self.pegar_cookies, "Complemento-user", self.input_complemento_trocar)
                
            """
            Avisos para enviar no html
                """
            flask.flash(self.input_cep_trocar)
            flask.flash(self.input_rua_trocar)
            flask.flash(self.input_bairro_trocar)
            flask.flash(self.input_numero_de_residencia_trocar)
            flask.flash(self.input_complemento_trocar)
        
            return flask.redirect("/emporio")