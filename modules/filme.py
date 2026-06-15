def buscaFilme(dados, query):
    if not query or not query.strip():
        return 1, []
    q = query.strip().lower()
    resultados = [f for f in dados.get("filmes", []) if q in f.get("nome", "").lower()]
    if not resultados:
        return 1, []
    return 0, resultados
