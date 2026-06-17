"""
pesquisa.py  --  Modulo Pesquisa (dono: Joao Pedro Souza C de Oliveira).
INF1040 - Projeto de Programacao Modular. Grupo 2, turma 3WA.

Coleta a pesquisa de interesses do usuario logado e a persiste no objeto
de dados em memoria (o app salva o dados.json ao final, via modules.arquivo).

Convencao do projeto: toda funcao recebe o dicionario 'dados' como primeiro
argumento, opera sobre ele e retorna uma tupla (codigo, conteudo).

Funcoes (chamadas por pages/research.py):
  criaInteresses(dados, userID, pesquisaInteresses)  -> (code, None)  # codes: -1, 0, 2
  modificaInteresses(dados, userID, interesses)      -> (code, None)  # codes: -1, 0, 2, 8

Formatos:
  pesquisaInteresses : dict {genero(str): peso(int)}      ex: {"acao": 8, "drama": 5}
  interesses         : list de pares (genero(str), peso(int))  ex: [("acao", 8), ("drama", 5)]
  Armazenado em dados["usuarios"][userID]["interesses"] como [[genero, peso], ...],
  formato lido por modules.usuario.buscaInteresses e usado por modules.recomendacoes.
"""

from modules.codigos import (
    ERRO, SUCESSO, USUARIO_NAO_EXISTENTE, INTERESSES_INVALIDOS,
)


# ------------------------- validacao interna -------------------------

def _parValido(par):
    if not isinstance(par, (list, tuple)) or len(par) != 2:
        return False
    genero, peso = par
    if not isinstance(genero, str) or not genero.strip():
        return False
    if isinstance(peso, bool) or not isinstance(peso, int):  # bool e subclasse de int
        return False
    if peso < 1:
        return False
    return True


def _listaInteressesValida(interesses):
    if not isinstance(interesses, list) or len(interesses) == 0:
        return False
    generos_vistos = set()
    for par in interesses:
        if not _parValido(par):
            return False
        genero = par[0]
        if genero in generos_vistos:  # genero repetido
            return False
        generos_vistos.add(genero)
    return True


def _transformaPesquisa(pesquisaInteresses):
    """Converte o dict {genero: peso} da pesquisa em lista [(genero, peso)].
    Levanta ValueError em estrutura invalida; criaInteresses captura e
    reporta como erro de processamento (code -1, conforme Caso 05)."""
    if not isinstance(pesquisaInteresses, dict) or len(pesquisaInteresses) == 0:
        raise ValueError("pesquisa vazia ou de tipo invalido")
    interesses = []
    for genero, peso in pesquisaInteresses.items():
        if not isinstance(genero, str) or not genero.strip():
            raise ValueError("genero invalido")
        if isinstance(peso, bool) or not isinstance(peso, int):
            raise ValueError("peso invalido")
        interesses.append((genero, peso))
    return interesses


# ------------------------- funcoes do modulo -------------------------

def modificaInteresses(dados, userID, interesses):
    """Atualiza a lista de interesses de um usuario existente.
      0  : sucesso
      2  : usuario nao existente
      8  : lista de interesses invalida
      -1 : erro tecnico (ex.: dados nao carregados)
    """
    try:
        if dados is None:
            return (ERRO, None)
        if not _listaInteressesValida(interesses):
            return (INTERESSES_INVALIDOS, None)
        if userID not in dados["usuarios"]:
            return (USUARIO_NAO_EXISTENTE, None)
        dados["usuarios"][userID]["interesses"] = [[genero, peso] for genero, peso in interesses]
        return (SUCESSO, None)
    except Exception:
        return (ERRO, None)


def criaInteresses(dados, userID, pesquisaInteresses):
    """Cria a lista de interesses a partir da pesquisa (dict {genero: peso}).
    Valida e transforma a pesquisa e delega a escrita a modificaInteresses.
      0  : sucesso
      2  : usuario nao existente
      -1 : erro de processamento
    """
    try:
        if dados is None:
            return (ERRO, None)
        interesses = _transformaPesquisa(pesquisaInteresses)
        code, _ = modificaInteresses(dados, userID, interesses)
        if code == SUCESSO:
            return (SUCESSO, None)
        if code == USUARIO_NAO_EXISTENTE:
            return (USUARIO_NAO_EXISTENTE, None)
        # code 8 ou inesperado aqui significa falha de processamento desta funcao
        return (ERRO, None)
    except Exception:
        return (ERRO, None)
