import pytest
from modules import recomendacoes
from modules.codigos import (
    SUCESSO, ERRO, USUARIO_NAO_EXISTENTE, SEM_RECOMENDACOES, ERRO_RECOMENDACOES
)

def test_busca_recomendacoes_sucesso(mock_dados):
    code, info = recomendacoes.buscaRecomendacoes(mock_dados["data"], "u_alice")
    assert code == SUCESSO
    assert isinstance(info, list)
    assert len(info) > 0

    # Validação do algoritmo de prioridade:
    posicao_matrix = info.index("f1")
    posicao_interestelar = info.index("f11")
    assert posicao_matrix < posicao_interestelar

def test_busca_recomendacoes_usuario_nao_existente(mock_dados):
    code, info = recomendacoes.buscaRecomendacoes(mock_dados["data"], "fantasma")
    assert code == USUARIO_NAO_EXISTENTE
    assert info == []


def test_busca_recomendacoes_usuario_sem_interesses(mock_dados):
    code, info = recomendacoes.buscaRecomendacoes(mock_dados["data"], "u_bob")
    assert code == SEM_RECOMENDACOES
    assert info == []


def test_busca_recomendacoes_limite_ranking(mock_dados):
    # testa caso possuam mais do que 10 filmes que podem ser de interesse
    _, info = recomendacoes.buscaRecomendacoes(mock_dados["data"], "u1")
    assert len(info) <= 10
    

def test_busca_recomendacoes_erro_calculo(mock_dados):
    # Salva a função original para não quebrar os outros testes
    funcao_original = recomendacoes.buscaFilmesRecomendados
    
    # Fazemos a função retornar SUCESSO, mas com dados que quebram o laço 'for' (None)
    recomendacoes.buscaFilmesRecomendados = lambda dados, generos: (0, None)

    try:
        code, info = recomendacoes.buscaRecomendacoes(mock_dados["data"], "u_alice")
        assert code == ERRO_RECOMENDACOES
        assert info == []
    finally:
        recomendacoes.buscaFilmesRecomendados = funcao_original