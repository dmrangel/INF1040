from modules.codigos import ERRO, SUCESSO, USUARIO_NAO_EXISTENTE

def buscaUsuario(dados, nome):
    if dados is None:
        return (ERRO, None)
    for u in dados["usuarios"].values():
        if u["nome"] == nome:
            return (SUCESSO, u)
    return (USUARIO_NAO_EXISTENTE, None)
