from modules.codigos import ERRO, SUCESSO, USUARIO_NAO_EXISTENTE, SEM_INTERESSES

# Retorna a lista de interesses (gênero, peso) de um usuário pelo ID
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

# Retorna o objeto de um usuário pelo nome
def buscaUsuario(dados, nome):
    if dados is None:  # falha ao carregar o arquivo
        return (ERRO, None)
    for u in dados["usuarios"].values():  # itera valores pois a chave é UUID, não o nome
        if u["nome"] == nome:
            return (SUCESSO, u)
    return (USUARIO_NAO_EXISTENTE, None)  # nenhum usuário com esse nome
