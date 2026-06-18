import pytest
from modules import filme

# caso 1: busca por nome exato retorna o filme correspondente
def test_busca_match_exato(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "matrix")
    assert code == 0
    assert any(f["nome"] == "matrix" for f in resultados)

# caso 2: busca por substring retorna filmes cujo nome contém o trecho
def test_busca_match_parcial(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "toy")
    assert code == 0
    assert any("toy" in f["nome"] for f in resultados)

# caso 3: busca em maiúsculas encontra filme cadastrado em minúsculas
def test_busca_case_insensitive(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "MATRIX")
    assert code == 0
    assert any(f["nome"] == "matrix" for f in resultados)

# caso 4: busca com capitalização mista também é normalizada corretamente
def test_busca_case_insensitive_misto(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "TiTaNiC")
    assert code == 0
    assert any(f["nome"] == "titanic" for f in resultados)

# caso 5: substring presente em vários nomes retorna múltiplos filmes
def test_busca_multiplos_resultados(mock_dados):
    # "a" aparece em matrix, alien, gladiador, clube da luta, parasita, etc.
    code, resultados = filme.buscaFilme(mock_dados["data"], "a")
    assert code == 0
    assert len(resultados) > 1

# caso 6: substring inexistente no catálogo retorna ERRO e lista vazia
def test_busca_sem_resultado(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "xyzabcnaoexiste")
    assert code == -1
    assert resultados == []

# caso 7: query vazia retorna ERRO sem percorrer o catálogo
def test_busca_query_vazia(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "")
    assert code == -1
    assert resultados == []

# caso 8: query composta apenas de espaços é tratada como vazia
def test_busca_query_so_espacos(mock_dados):
    code, resultados = filme.buscaFilme(mock_dados["data"], "   ")
    assert code == -1
    assert resultados == []

# caso 9: objeto retornado contém os campos obrigatórios id, nome e generos
def test_busca_retorna_campos_completos(mock_dados):
    _, resultados = filme.buscaFilme(mock_dados["data"], "matrix")
    f = resultados[0]
    assert "id" in f
    assert "nome" in f
    assert "generos" in f
