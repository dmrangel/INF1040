import pytest
from modules import autenticacao
from modules.codigos import (
    SUCESSO, ERRO, USUARIO_EXISTENTE,
    USUARIO_NAO_EXISTENTE, SENHA_INVALIDA, SENHA_INCORRETA,
)


# --- registraUsuario ---

def test_registra_sucesso(mock_dados):
    code, uid = autenticacao.registraUsuario(mock_dados["data"], "novo", "senha_valida")
    assert code == SUCESSO
    assert isinstance(uid, str) and uid
    assert mock_dados["data"]["usuarios"][uid]["nome"] == "novo"
    assert mock_dados["data"]["usuarios"][uid]["interesses"] == []

def test_registra_senha_hash_armazenada(mock_dados):
    _, uid = autenticacao.registraUsuario(mock_dados["data"], "hashed", "senha_valida")
    esperado = autenticacao._gerar_hash_senha("senha_valida")
    assert mock_dados["data"]["usuarios"][uid]["senha"] == esperado

def test_registra_usuario_existente(mock_dados):
    code, uid = autenticacao.registraUsuario(mock_dados["data"], "alice", "outra_senha")
    assert code == USUARIO_EXISTENTE
    assert uid is None

def test_registra_senha_invalida_curta(mock_dados):
    code, uid = autenticacao.registraUsuario(mock_dados["data"], "qualquer", "abc")
    assert code == SENHA_INVALIDA
    assert uid is None

def test_registra_senha_minimo_exato(mock_dados):
    code, _ = autenticacao.registraUsuario(mock_dados["data"], "exato", "123456")
    assert code == SUCESSO

def test_registra_dados_nulos():
    code, uid = autenticacao.registraUsuario(None, "qualquer", "senha_valida")
    assert code == ERRO
    assert uid is None

def test_registra_id_unico(mock_dados):
    _, uid1 = autenticacao.registraUsuario(mock_dados["data"], "user1", "senha_valida")
    _, uid2 = autenticacao.registraUsuario(mock_dados["data"], "user2", "senha_valida")
    assert uid1 != uid2


# --- loginUsuario ---

def test_login_sucesso(mock_dados):
    code, uid = autenticacao.loginUsuario(mock_dados["data"], "alice", "senha123")
    assert code == SUCESSO
    assert uid == "u_alice"

def test_login_usuario_nao_existente(mock_dados):
    code, uid = autenticacao.loginUsuario(mock_dados["data"], "fantasma", "qualquer")
    assert code == USUARIO_NAO_EXISTENTE
    assert uid is None

def test_login_senha_incorreta(mock_dados):
    code, uid = autenticacao.loginUsuario(mock_dados["data"], "alice", "senha_errada")
    assert code == SENHA_INCORRETA
    assert uid is None

def test_login_dados_nulos():
    code, uid = autenticacao.loginUsuario(None, "alice", "senha123")
    assert code == ERRO
    assert uid is None

def test_login_apos_registro(mock_dados):
    autenticacao.registraUsuario(mock_dados["data"], "novo_user", "senha_nova123")
    code, uid = autenticacao.loginUsuario(mock_dados["data"], "novo_user", "senha_nova123")
    assert code == SUCESSO
    assert uid is not None


# --- funções internas ---

def test_hash_determinista():
    h1 = autenticacao._gerar_hash_senha("teste")
    h2 = autenticacao._gerar_hash_senha("teste")
    assert h1 == h2

def test_hash_diferente_por_entrada():
    assert autenticacao._gerar_hash_senha("a") != autenticacao._gerar_hash_senha("b")

def test_validar_senha_aceita_minimo():
    assert autenticacao._validar_forca_senha("123456") is True

def test_validar_senha_rejeita_curta():
    assert autenticacao._validar_forca_senha("12345") is False
