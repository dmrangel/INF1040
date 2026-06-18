from modules.codigos import SUCESSO, ERRO

#***********************************************************************
# Módulo: filmes
# Descrição: Funções de consulta ao catálogo de filmes armazenado em
#            estrutura de dicionário carregada de arquivo externo.
#***********************************************************************

# obterGeneros
#
# Descrição:
#   Retorna a lista ordenada de todos os gêneros distintos presentes
#   no catálogo de filmes.
#
# Acoplamento:
#   dados   (dict) – estrutura de dados principal carregada do arquivo;
#                    deve conter a chave "filmes" com uma lista de objetos filme,
#                    cada um com a chave "generos" contendo uma lista de strings
#
# Retorno:
#   (list[str]) – lista de gêneros únicos em ordem alfabética;
#                 lista vazia se não houver filmes ou nenhum gênero cadastrado
#
# Assertivas de entrada:
#   - dados é um dict com a chave "filmes" (ou sem ela, retornando lista vazia)
#   - cada filme pode ter ou não a chave "generos"
#
# Assertivas de saída:
#   - o retorno é sempre uma lista (nunca None)
#   - não há gêneros duplicados
#   - os gêneros estão em ordem alfabética crescente
#-----------------------------------------------------------------------
def obterGeneros(dados):
    generos = set()
    for filme in dados.get("filmes", []):
        for g in filme.get("generos", []):
            generos.add(g)
    return sorted(generos)


#-----------------------------------------------------------------------
# buscaFilmesRecomendados
#
# Descrição:
#   Retorna todos os filmes do catálogo que pertencem a ao menos um
#   dos gêneros informados.
#
# Acoplamento:
#   dados    (dict)      – estrutura de dados principal carregada do arquivo;
#                          deve conter a chave "filmes" com uma lista de objetos filme
#   generos  (list[str]) – lista de gêneros de interesse do usuário
#
# Retorno:
#   (SUCESSO, list[dict]) – lista de objetos filme com ao menos um gênero em comum
#   (ERRO, [])            – lista de gêneros vazia ou nenhum filme encontrado
#
# Assertivas de entrada:
#   - dados é um dict com a chave "filmes"
#   - generos é uma lista (possivelmente vazia) de strings
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre SUCESSO ou ERRO
#   - se SUCESSO, o segundo elemento é uma lista não vazia de dicts de filme
#   - se ERRO, o segundo elemento é sempre uma lista vazia []
#-----------------------------------------------------------------------
def buscaFilmesRecomendados(dados, generos):
    if not generos:  # lista de generos vazia
        return (ERRO, [])

    generos_set = set(generos)  # set para busca O(1)
    resultados = []

    for filme in dados.get("filmes", []):
        generos_filme = set(filme.get("generos", []))
        if generos_set & generos_filme:  # filme tem ao menos um genero de interesse
            resultados.append(filme)

    if not resultados:  # nenhum filme encontrado
        return (ERRO, [])

    return (SUCESSO, resultados)


#-----------------------------------------------------------------------
# buscaFilme
#
# Descrição:
#   Retorna todos os filmes cujo nome contém a substring buscada,
#   com busca case-insensitive e ignorando espaços nas bordas.
#
# Acoplamento:
#   dados      (dict) – estrutura de dados principal carregada do arquivo;
#                       deve conter a chave "filmes" com uma lista de objetos filme
#   nomeFilme  (str)  – substring a ser buscada no nome dos filmes
#
# Retorno:
#   (SUCESSO, list[dict]) – lista de objetos filme cujo nome contém a substring
#   (ERRO, [])            – query vazia/só espaços ou nenhum filme encontrado
#
# Assertivas de entrada:
#   - dados é um dict com a chave "filmes"
#   - nomeFilme é uma string (possivelmente vazia ou com apenas espaços)
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre SUCESSO ou ERRO
#   - se SUCESSO, o segundo elemento é uma lista não vazia de dicts de filme
#   - se ERRO, o segundo elemento é sempre uma lista vazia []
#   - a comparação é case-insensitive (ambos normalizados com .lower())
#   - espaços nas bordas da query são ignorados via .strip()
#-----------------------------------------------------------------------
def buscaFilme(dados, nomeFilme):
    if not nomeFilme or not nomeFilme.strip():  # query vazia ou so espacos
        return (ERRO, [])

    nomeFilme = nomeFilme.strip().lower()  # normaliza para busca case-insensitive
    resultados = []

    for filme in dados.get("filmes", []):
        nomeAtual = filme.get("nome", "").lower()
        if nomeFilme in nomeAtual:  # busca por substring
            resultados.append(filme)

    if not resultados:  # nenhum filme encontrado
        return (ERRO, [])

    return (SUCESSO, resultados)
