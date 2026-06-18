from modules.filme import buscaFilmesRecomendados
from modules.usuario import buscaInteresses
from modules.codigos import (
    SUCESSO, ERRO, USUARIO_NAO_EXISTENTE, SEM_RECOMENDACOES, SEM_INTERESSES, ERRO_RECOMENDACOES, INTERESSES_INVALIDOS
)
#***********************************************************************
# Módulo: recomendacoes
# Descrição: Funções de recomendação de filmes baseadas nos interesses
#            e pesos definidos pelo usuário. Depende dos módulos
#            usuario e filme para obter dados intermediários.
#***********************************************************************

#-----------------------------------------------------------------------
# buscaRecomendacoes
#
# Descrição:
#   Retorna uma lista de até 10 IDs de filmes recomendados para o usuário,
#   ordenados por score de relevância calculado a partir dos pesos dos
#   gêneros de interesse do usuário.
#
# Acoplamento:
#   dados   (dict) – estrutura de dados principal carregada do arquivo;
#                    deve conter as chaves "usuarios" e "filmes"
#   userID  (str)  – UUID do usuário para o qual gerar recomendações
#
# Retorno:
#   (SUCESSO, list[str])         – lista de até 10 IDs de filmes ordenados por score
#   (ERRO, [])                   – dados inválidos ou erro no módulo usuario/filmes
#   (USUARIO_NAO_EXISTENTE, [])  – UUID não encontrado na base de usuários
#   (SEM_RECOMENDACOES, [])      – usuário existe mas não possui interesses definidos
#   (ERRO_RECOMENDACOES, [])     – falha durante o cálculo do score de recomendação
#
# Assertivas de entrada:
#   - dados é None ou um dict com as chaves "usuarios" e "filmes"
#   - userID é uma string não vazia representando um UUID válido
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre um dos códigos definidos em modules.codigos
#   - se SUCESSO, o segundo elemento é uma lista de 1 a 10 strings de IDs de filmes
#   - se SUCESSO, a lista está ordenada por score decrescente (mais relevante primeiro)
#   - em qualquer caso de erro, o segundo elemento é sempre uma lista vazia []
#   - o score de cada filme é a soma dos pesos dos gêneros em comum com os interesses do usuário
#-----------------------------------------------------------------------
def buscaRecomendacoes(dados, userID):
    aux = buscaInteresses(dados, userID)

    if (aux[0] == ERRO):
        #print("Modulo recomendacoes: Modulo Usuario retornou erro!\n")
        return (ERRO, [])
    elif (aux[0] == USUARIO_NAO_EXISTENTE):
        #print("Modulo recomendacoes: Usuário não existente!\n")
        return (USUARIO_NAO_EXISTENTE, [])
    elif (aux[0] == SEM_INTERESSES):
        #print("Modulo recomendacoes: Usuario não possui interesses!\n")
        return (SEM_RECOMENDACOES, [])

    listaInteressesComPesos = aux[1]

    mapaPesos = {item[0]: item[1] for item in listaInteressesComPesos}

    listaGenerosApenas = list(mapaPesos.keys()) 

    aux_filmes = buscaFilmesRecomendados(dados, listaGenerosApenas)

    if aux_filmes[0] == ERRO:
        #print("Modulo recomendacoes: Modulo Filmes retornou erro!\n")
        return (ERRO, [])
    
    filmes_completos = aux_filmes[1]

    try:
        filmes_com_score = []
        
        for filme in filmes_completos:
            score = 0
            for g in filme["generos"]:
                if g in mapaPesos:
                    score += mapaPesos[g]
            
            filmes_com_score.append((filme, score))
        
        filmes_com_score.sort(key=lambda x: x[1], reverse=True)
        
        lista_ids = [str(item[0]['id']) for item in filmes_com_score]
        ranking_final = lista_ids[:10]
        
        #print("Modulo recomendacoes: Retorno padrão de êxito\n")
        return (SUCESSO, ranking_final)
    
    except Exception:
        #print("Modulo recomendacoes: Não foi possível calcular a recomendação!\n")
        return (ERRO_RECOMENDACOES, [])