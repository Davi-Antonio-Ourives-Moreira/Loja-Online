class Produtos:
    def __init__(self, produto, preco) -> None:
        # produto
        self.produto = produto
        
        # preço do produto
        self.preco = preco
    
    def __repr__(self) -> str:
        return f"Produto: {self.produto}\nPreço: R$ {self.preco}"