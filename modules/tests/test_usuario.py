import pytest
from modules import usuario
from modules.codigos import SUCESSO, ERRO, USUARIO_NAO_EXISTENTE, SEM_INTERESSES

# caso 1: busca bem-sucedida retorna objeto do usuário com id e nome corretos
def test_busca_sucesso(mock_dados):
    code, info = usuario.buscaUsuario(mock_dados["data"], "alice")
    assert code == SUCESSO
    assert info["id"] == "u_alice"
    assert info["nome"] == "alice"

# caso 2: objeto retornado contém todos os campos obrigatórios do usuário
def test_busca_retorna_dict_completo(mock_dados):
    _, info = usuario.buscaUsuario(mock_dados["data"], "alice")
    assert "id" in info
    assert "nome" in info
    assert "senha" in info
    assert "interesses" in info

# caso 3: nome inexistente na base retorna USUARIO_NAO_EXISTENTE
def test_busca_usuario_nao_existente(mock_dados):
    code, info = usuario.buscaUsuario(mock_dados["data"], "fantasma")
    assert code == USUARIO_NAO_EXISTENTE
    assert info is None

# caso 4: dados nulos retornam ERRO antes de qualquer busca
def test_busca_dados_nulos():
    code, info = usuario.buscaUsuario(None, "alice")
    assert code == ERRO
    assert info is None

# caso 5: busca por nome com capitalização diferente não encontra o usuário (case-sensitive)
def test_busca_case_sensitive(mock_dados):
    code, _ = usuario.buscaUsuario(mock_dados["data"], "Alice")
    assert code == USUARIO_NAO_EXISTENTE

# caso 6: busca pelo segundo usuário cadastrado retorna o objeto correto
def test_busca_segundo_usuario(mock_dados):
    code, info = usuario.buscaUsuario(mock_dados["data"], "bob")
    assert code == SUCESSO
    assert info["id"] == "u_bob"


# ----------------- buscaInteresses -----------------

# caso 1: interesses retornados corretamente como lista de tuplas (gênero, peso)
def test_busca_interesses_sucesso(mock_dados):
    code, interesses = usuario.buscaInteresses(mock_dados["data"], "u_alice")
    assert code == SUCESSO
    assert interesses == [("acao", 5), ("drama", 3)]

# caso 2: cada item da lista retornada é uma tupla de exatamente 2 elementos
def test_busca_interesses_formato_tupla(mock_dados):
    _, interesses = usuario.buscaInteresses(mock_dados["data"], "u_alice")
    for item in interesses:
        assert isinstance(item, tuple)
        assert len(item) == 2

# caso 3: usuário sem interesses definidos retorna SEM_INTERESSES
def test_busca_interesses_sem_interesses(mock_dados):
    code, interesses = usuario.buscaInteresses(mock_dados["data"], "u_bob")
    assert code == SEM_INTERESSES
    assert interesses is None

# caso 4: UUID inexistente na base retorna USUARIO_NAO_EXISTENTE
def test_busca_interesses_usuario_nao_existente(mock_dados):
    code, interesses = usuario.buscaInteresses(mock_dados["data"], "u_fantasma")
    assert code == USUARIO_NAO_EXISTENTE
    assert interesses is None

# caso 5: dados nulos retornam ERRO antes de qualquer busca
def test_busca_interesses_dados_nulos():
    code, interesses = usuario.buscaInteresses(None, "u_alice")
    assert code == ERRO
    assert interesses is None
