from modules.codigos import SUCESSO, ERRO

# Retorna todos os generos distintos presentes no catalogo
def obterGeneros(dados):
    generos = set()
    for filme in dados.get("filmes", []):
        for g in filme.get("generos", []):
            generos.add(g)
    return sorted(generos)

# Retorna filmes que pertencem a ao menos um dos generos recebidos
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

# Retorna filmes cujo nome contem a substring buscada
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
