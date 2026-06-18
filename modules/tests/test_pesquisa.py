import pytest
from modules import pesquisa
from modules.codigos import (
    SUCESSO, ERRO, USUARIO_NAO_EXISTENTE, INTERESSES_INVALIDOS,
)

# Fixture mock_dados (modules/tests/conftest.py):
#   u_alice -> interesses [["acao", 5], ["drama", 3]]
#   u_bob   -> interesses []  (sem interesses)


# ----------------- criaInteresses -----------------

# caso 1: criação bem-sucedida com dicionário válido de gêneros e pesos
def test_cria_sucesso(mock_dados):                              # Caso 03
    code, payload = pesquisa.criaInteresses(
        mock_dados["data"], "u_bob", {"acao": 8, "comedia": 3, "drama": 5}
    )
    assert code == SUCESSO
    assert payload is None
    assert mock_dados["data"]["usuarios"]["u_bob"]["interesses"] == [
        ["acao", 8], ["comedia", 3], ["drama", 5]
    ]

# caso 2: UUID inexistente na base retorna USUARIO_NAO_EXISTENTE
def test_cria_usuario_inexistente(mock_dados):                 # Caso 04
    code, payload = pesquisa.criaInteresses(mock_dados["data"], "u_fantasma", {"acao": 8})
    assert code == USUARIO_NAO_EXISTENTE
    assert payload is None

# caso 3: peso com tipo inválido (string) causa erro de processamento
def test_cria_erro_processamento_peso_invalido(mock_dados):    # Caso 05
    code, payload = pesquisa.criaInteresses(mock_dados["data"], "u_bob", {"acao": "muito"})
    assert code == ERRO
    assert payload is None

# caso 4: dados nulos retornam ERRO antes de qualquer processamento
def test_cria_dados_nulos():                                   # Caso 05 (falha de persistencia)
    code, payload = pesquisa.criaInteresses(None, "u_bob", {"acao": 8})
    assert code == ERRO
    assert payload is None

# caso 5: dicionário de pesquisa vazio retorna ERRO por ausência de conteúdo
def test_cria_pesquisa_vazia(mock_dados):                      # robustez
    code, _ = pesquisa.criaInteresses(mock_dados["data"], "u_bob", {})
    assert code == ERRO


# --------------- modificaInteresses ---------------

# caso 1: atualização bem-sucedida substitui completamente os interesses anteriores
def test_modifica_sucesso(mock_dados):                         # Caso 06
    code, payload = pesquisa.modificaInteresses(
        mock_dados["data"], "u_alice", [("acao", 9), ("terror", 2)]
    )
    assert code == SUCESSO
    assert payload is None
    assert mock_dados["data"]["usuarios"]["u_alice"]["interesses"] == [
        ["acao", 9], ["terror", 2]
    ]

# caso 2: UUID inexistente na base retorna USUARIO_NAO_EXISTENTE
def test_modifica_usuario_inexistente(mock_dados):            # Caso 07
    code, payload = pesquisa.modificaInteresses(mock_dados["data"], "u_fantasma", [("acao", 9)])
    assert code == USUARIO_NAO_EXISTENTE
    assert payload is None

# caso 3: lista vazia é rejeitada como inválida
def test_modifica_lista_vazia(mock_dados):                    # Caso 08
    code, payload = pesquisa.modificaInteresses(mock_dados["data"], "u_alice", [])
    assert code == INTERESSES_INVALIDOS
    assert payload is None

# caso 4: lista com strings soltas em vez de pares é rejeitada como malformada
def test_modifica_lista_malformada(mock_dados):               # Caso 08 (formato divergente)
    code, _ = pesquisa.modificaInteresses(mock_dados["data"], "u_alice", ["acao", "drama"])
    assert code == INTERESSES_INVALIDOS

# caso 5: peso do tipo float é rejeitado pois o contrato exige int
def test_modifica_peso_nao_inteiro(mock_dados):               # Caso 08 (peso invalido)
    code, _ = pesquisa.modificaInteresses(mock_dados["data"], "u_alice", [("acao", 5.5)])
    assert code == INTERESSES_INVALIDOS

# caso 6: dados nulos retornam ERRO antes de qualquer processamento
def test_modifica_dados_nulos():                              # Caso 09
    code, payload = pesquisa.modificaInteresses(None, "u_alice", [("acao", 5)])
    assert code == ERRO
    assert payload is None

# caso 7: modificação de um usuário não altera os dados de outro (isolamento)
def test_modifica_nao_afeta_outro_usuario(mock_dados):       # robustez (isolamento)
    pesquisa.modificaInteresses(mock_dados["data"], "u_alice", [("acao", 1)])
    assert mock_dados["data"]["usuarios"]["u_bob"]["interesses"] == []
