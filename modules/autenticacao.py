import uuid
import hashlib
from modules.codigos import (
    ERRO, SUCESSO, USUARIO_EXISTENTE,
    USUARIO_NAO_EXISTENTE, SENHA_INVALIDA, SENHA_INCORRETA,
)

def _gerar_id_usuario():
    return str(uuid.uuid4())

def _gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def _validar_forca_senha(senha):
    return len(senha) >= 6

def registraUsuario(dados, nomeUser: str, senhaUser: str) -> tuple:
    if not _validar_forca_senha(senhaUser):
        return (SENHA_INVALIDA, None)

    if dados is None:
        return (ERRO, None)

    for info_usuario in dados["usuarios"].values():
        if info_usuario["nome"] == nomeUser:
            return (USUARIO_EXISTENTE, None)

    novo_id = _gerar_id_usuario()
    dados["usuarios"][novo_id] = {
        "id": novo_id,
        "nome": nomeUser,
        "senha": _gerar_hash_senha(senhaUser),
        "interesses": []
    }

    return (SUCESSO, novo_id)

def loginUsuario(dados, nomeUser: str, senhaUser: str) -> tuple:
    if dados is None:
        return (ERRO, None)

    for id_usuario, info_usuario in dados["usuarios"].items():
        if info_usuario["nome"] == nomeUser:
            if info_usuario["senha"] == _gerar_hash_senha(senhaUser):
                return (SUCESSO, id_usuario)
            else:
                return (SENHA_INCORRETA, None)

    return (USUARIO_NAO_EXISTENTE, None)
