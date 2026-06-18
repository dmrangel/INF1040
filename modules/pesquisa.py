"""
pesquisa.py  --  Modulo Pesquisa (dono: Joao Pedro Souza C de Oliveira).
"""

from modules.codigos import (
    ERRO, SUCESSO, USUARIO_NAO_EXISTENTE, INTERESSES_INVALIDOS,
)

#***********************************************************************
# Módulo: pesquisa
# Descrição: Funções de criação e atualização dos interesses do usuário
#            logado, persistindo os dados em memória via dicionário
#            principal. A gravação em arquivo é responsabilidade do
#            módulo modules.arquivo.
#***********************************************************************


# ------------------------- validacao interna -------------------------

#-----------------------------------------------------------------------
# _parValido (função interna)
#
# Descrição:
#   Valida se um par (gênero, peso) é estruturalmente correto.
#
# Acoplamento:
#   par   (list | tuple) – par a ser validado, esperado como (str, int)
#
# Retorno:
#   (bool) – True se o par é válido; False caso contrário
#
# Assertivas de entrada:
#   - par pode ser qualquer tipo; a função trata tipos inválidos internamente
#
# Assertivas de saída:
#   - retorna True somente se: par tem exatamente 2 elementos, gênero é
#     string não vazia, peso é int não booleano e maior ou igual a 1
#-----------------------------------------------------------------------
def _parValido(par):
    if not isinstance(par, (list, tuple)) or len(par) != 2:
        return False
    genero, peso = par
    if not isinstance(genero, str) or not genero.strip():
        return False
    if isinstance(peso, bool) or not isinstance(peso, int):  # bool e subclasse de int
        return False
    if peso < 1:
        return False
    return True


#-----------------------------------------------------------------------
# _listaInteressesValida (função interna)
#
# Descrição:
#   Valida se uma lista de interesses é estruturalmente correta,
#   verificando cada par e garantindo que não há gêneros repetidos.
#
# Acoplamento:
#   interesses   (list) – lista de pares (gênero, peso) a ser validada
#
# Retorno:
#   (bool) – True se a lista é válida; False caso contrário
#
# Assertivas de entrada:
#   - interesses pode ser qualquer tipo; a função trata tipos inválidos internamente
#
# Assertivas de saída:
#   - retorna True somente se: é uma lista não vazia, todos os pares são
#     válidos segundo _parValido, e não há gêneros duplicados
#-----------------------------------------------------------------------
def _listaInteressesValida(interesses):
    if not isinstance(interesses, list) or len(interesses) == 0:
        return False
    generos_vistos = set()
    for par in interesses:
        if not _parValido(par):
            return False
        genero = par[0]
        if genero in generos_vistos:  # genero repetido
            return False
        generos_vistos.add(genero)
    return True


#-----------------------------------------------------------------------
# _transformaPesquisa (função interna)
#
# Descrição:
#   Converte o dicionário {gênero: peso} recebido da pesquisa em uma
#   lista de tuplas [(gênero, peso)] para uso interno.
#
# Acoplamento:
#   pesquisaInteresses   (dict) – dicionário {str: int} com gêneros e pesos
#
# Retorno:
#   (list[tuple]) – lista de tuplas (gênero, peso)
#
# Assertivas de entrada:
#   - pesquisaInteresses deve ser um dict não vazio com chaves str e valores int
#
# Assertivas de saída:
#   - retorna lista de tuplas equivalente ao dict de entrada
#   - levanta ValueError se a estrutura for inválida; o chamador é
#     responsável por capturar e tratar como ERRO
#-----------------------------------------------------------------------
def _transformaPesquisa(pesquisaInteresses):
    """Converte o dict {genero: peso} da pesquisa em lista [(genero, peso)].
    Levanta ValueError em estrutura invalida; criaInteresses captura e
    reporta como erro de processamento (code -1, conforme Caso 05)."""
    if not isinstance(pesquisaInteresses, dict) or len(pesquisaInteresses) == 0:
        raise ValueError("pesquisa vazia ou de tipo invalido")
    interesses = []
    for genero, peso in pesquisaInteresses.items():
        if not isinstance(genero, str) or not genero.strip():
            raise ValueError("genero invalido")
        if isinstance(peso, bool) or not isinstance(peso, int):
            raise ValueError("peso invalido")
        interesses.append((genero, peso))
    return interesses


# ------------------------- funcoes do modulo -------------------------

#-----------------------------------------------------------------------
# modificaInteresses
#
# Descrição:
#   Atualiza a lista de interesses de um usuário existente na estrutura
#   de dados, substituindo completamente os interesses anteriores.
#
# Acoplamento:
#   dados       (dict)       – estrutura de dados principal carregada do arquivo;
#                              deve conter a chave "usuarios" mapeando UUIDs a objetos
#   userID      (str)        – UUID do usuário a ter os interesses atualizados
#   interesses  (list)       – lista de pares (gênero (str), peso (int))
#
# Retorno:
#   (SUCESSO, None)              – interesses atualizados com sucesso
#   (ERRO, None)                 – dados inválidos, não carregados ou exceção inesperada
#   (USUARIO_NAO_EXISTENTE, None) – UUID não encontrado na base de usuários
#   (INTERESSES_INVALIDOS, None) – lista de interesses não passa na validação
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - userID é uma string não vazia representando um UUID válido
#   - interesses é uma lista de pares (str, int)
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre um dos códigos definidos em modules.codigos
#   - o segundo elemento é sempre None
#   - se SUCESSO, dados["usuarios"][userID]["interesses"] contém a nova lista no
#     formato [[genero, peso], ...] compatível com modules.usuario.buscaInteresses
#   - os interesses anteriores são completamente substituídos pelos novos
#-----------------------------------------------------------------------
def modificaInteresses(dados, userID, interesses):
    try:
        if dados is None:
            return (ERRO, None)
        if not _listaInteressesValida(interesses):
            return (INTERESSES_INVALIDOS, None)
        if userID not in dados["usuarios"]:
            return (USUARIO_NAO_EXISTENTE, None)
        dados["usuarios"][userID]["interesses"] = [[genero, peso] for genero, peso in interesses]
        return (SUCESSO, None)
    except Exception:
        return (ERRO, None)


#-----------------------------------------------------------------------
# criaInteresses
#
# Descrição:
#   Cria a lista de interesses de um usuário a partir do dicionário
#   retornado pela pesquisa. Converte o formato dict para lista de tuplas
#   e delega a persistência a modificaInteresses.
#
# Acoplamento:
#   dados               (dict) – estrutura de dados principal carregada do arquivo;
#                                deve conter a chave "usuarios" mapeando UUIDs a objetos
#   userID              (str)  – UUID do usuário a ter os interesses criados
#   pesquisaInteresses  (dict) – dicionário {gênero (str): peso (int)} vindo da pesquisa
#
# Retorno:
#   (SUCESSO, None)              – interesses criados com sucesso
#   (ERRO, None)                 – dados inválidos, falha na transformação ou exceção inesperada
#   (USUARIO_NAO_EXISTENTE, None) – UUID não encontrado na base de usuários
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - userID é uma string não vazia representando um UUID válido
#   - pesquisaInteresses é um dict {str: int} não vazio
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre um dos códigos definidos em modules.codigos
#   - o segundo elemento é sempre None
#   - se SUCESSO, os interesses foram persistidos via modificaInteresses
#   - INTERESSES_INVALIDOS de modificaInteresses é absorvido e retornado como ERRO,
#     pois indica falha interna de processamento desta função, não input direto do usuário
#-----------------------------------------------------------------------
def criaInteresses(dados, userID, pesquisaInteresses):
    try:
        if dados is None:
            return (ERRO, None)
        interesses = _transformaPesquisa(pesquisaInteresses)
        code, _ = modificaInteresses(dados, userID, interesses)
        if code == SUCESSO:
            return (SUCESSO, None)
        if code == USUARIO_NAO_EXISTENTE:
            return (USUARIO_NAO_EXISTENTE, None)
        # code 8 ou inesperado aqui significa falha de processamento desta funcao
        return (ERRO, None)
    except Exception:
        return (ERRO, None)
