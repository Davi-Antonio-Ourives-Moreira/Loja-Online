"""
Erros página de cadastro
    """
# email não existente
class NonExistentEmail(Exception):
    pass

# senha diferentes
class DifferentPasswords(Exception):
    pass

# campos cadastros vazios
class EmptyRegistrationFields(Exception):
    pass

# email já utilizado
class EmailAlreadyUsed(Exception):
    pass

"""
Erros da página de login
    """
# email não encontrado
class EmailNotFound(Exception):
    pass

# senha errada
class WrongPassword(Exception):
    pass

# campos de login vazios
class EmptyLoginFields(Exception):
    pass

"""
Erros da página de mudança de senha
    """
# campos de email vazios
class EmptyEmailFields(Exception):
    pass

# email não cadastrado
class EmailNotRegistered(Exception):
    pass

# campo de codigo vazio
class EmptyCodeFields(Exception):
    pass

# codigo errado
class WrongCode(Exception):
    pass

# input senhas vazios
class EmptyPasswordFields(Exception):
    pass

# a senha não pode ser a mesma do que a anterior
class ThePasswordCannotBeTheSameAsThePreviousOne(Exception):
    pass

"""
Erros de pagamento
    """
class UnregisteredAddress(Exception):
    pass

"""
Erros de cadastro endereço
    """
# cep vazio
class EmptyZipCode(Exception):
    pass

# rua vazio
class EmptyStreet(Exception):
    pass

# bairro vazio
class EmptyNeighborhood(Exception):
    pass

# numero de residencia vazio
class EmptyResidenceNumber(Exception):
    pass

# cep pequeno
class SmallZipCode(Exception):
    pass