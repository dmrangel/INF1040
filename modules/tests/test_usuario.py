import pytest
from modules import usuario
from modules.codigos import SUCESSO, ERRO, USUARIO_NAO_EXISTENTE


def test_busca_sucesso(mock_dados):
    code, info = usuario.buscaUsuario("alice")
    assert code == SUCESSO
    assert info["id"] == "u_alice"
    assert info["nome"] == "alice"

def test_busca_retorna_dict_completo(mock_dados):
    _, info = usuario.buscaUsuario("alice")
    assert "id" in info
    assert "nome" in info
    assert "senha" in info
    assert "interesses" in info

def test_busca_usuario_nao_existente(mock_dados):
    code, info = usuario.buscaUsuario("fantasma")
    assert code == USUARIO_NAO_EXISTENTE
    assert info is None

def test_busca_erro_carregar(monkeypatch):
    monkeypatch.setattr("modules.arquivo.carregaJson", lambda: None)
    code, info = usuario.buscaUsuario("alice")
    assert code == ERRO
    assert info is None

def test_busca_case_sensitive(mock_dados):
    code, _ = usuario.buscaUsuario("Alice")
    assert code == USUARIO_NAO_EXISTENTE

def test_busca_segundo_usuario(mock_dados):
    code, info = usuario.buscaUsuario("bob")
    assert code == SUCESSO
    assert info["id"] == "u_bob"
