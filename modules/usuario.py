from modules.codigos import ERRO, SUCESSO, USUARIO_NAO_EXISTENTE, SEM_INTERESSES

#***********************************************************************
# Descrição: Funções de consulta a dados de usuários armazenados em
#            estrutura de dicionário carregada de arquivo externo.
#***********************************************************************

# função buscaInteresses
# Propósito:
#   - Obter a lista de interesses de um usuário a partir de seu ID;
#   - Retorna a lista de interesses (gênero, peso) de um usuário pelo ID
#
# Acoplamento:
#   Parâmetros:
#   dados        (dict)  – estrutura de dados principal carregada do arquivo;
#                          deve conter a chave "usuarios" mapeando UUIDs a objetos
#   id_usuario   (str)   – UUID do usuário a ser consultado
#
# Retorno:
#   (SUCESSO, [(str, int/float), ...]) – lista de tuplas (gênero, peso)
#   (ERRO, None)                       – dados inválidos ou não carregados
#   (USUARIO_NAO_EXISTENTE, None)      – UUID não encontrado
#   (SEM_INTERESSES, None)             – usuário existe mas sem interesses definidos
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - id_usuario é uma string não vazia representando um UUID válido
#
# Assertivas de saída:
#   - o primeiro elemento da tupla retornada é sempre um dos códigos definidos em modules.codigos
#   - se SUCESSO, o segundo elemento é uma lista não vazia de tuplas (gênero, peso)
#   - em qualquer caso de erro, o segundo elemento é None
#-----------------------------------------------------------------------
def buscaInteresses(dados, id_usuario):
    if dados is None:  # falha ao carregar o arquivo
        return (ERRO, None)
    usuario = dados["usuarios"].get(id_usuario)  # busca por UUID (chave do dict)
    if not usuario:  # ID não existe
        return (USUARIO_NAO_EXISTENTE, None)
    interesses = usuario.get("interesses", [])
    if not interesses:  # usuário ainda não definiu interesses
        return (SEM_INTERESSES, None)
    return (SUCESSO, [(genero, peso) for genero, peso in interesses])  # converte de [[g, p], ...] para [(g, p), ...]


# função buscaUsuario
#
# Descrição:
#   Retorna o objeto completo de um usuário buscando pelo nome.
#
# Acoplamento:
#   dados   (dict) – estrutura de dados principal carregada do arquivo;
#                    deve conter a chave "usuarios" mapeando UUIDs a objetos
#   nome    (str)  – nome do usuário a ser localizado (busca exata, case-sensitive)
#
# Retorno:
#   (SUCESSO, dict)              – dicionário com os dados completos do usuário
#   (ERRO, None)                 – dados inválidos ou não carregados
#   (USUARIO_NAO_EXISTENTE, None) – nenhum usuário com o nome informado
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - nome é uma string não vazia
#
# Assertivas de saída:
#   - o primeiro elemento da tupla retornada é sempre um dos códigos definidos em modules.codigos
#   - se SUCESSO, o segundo elemento é um dict representando o usuário encontrado
#   - em qualquer caso de erro, o segundo elemento é None
#   - a busca percorre todos os valores de "usuarios" e retorna o primeiro match encontrado
#-----------------------------------------------------------------------
def buscaUsuario(dados, nome):
    if dados is None:  # falha ao carregar o arquivo
        return (ERRO, None)
    for u in dados["usuarios"].values():  # itera valores pois a chave é UUID, não o nome
        if u["nome"] == nome:
            return (SUCESSO, u)
    return (USUARIO_NAO_EXISTENTE, None)  # nenhum usuário com esse nome
