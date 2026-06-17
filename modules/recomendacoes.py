from modules.filme import buscaFilmesRecomendados
from modules.usuario import buscaInteresses
from modules.codigos import (
    ERRO, USUARIO_NAO_EXISTENTE, SEM_RECOMENDACOES, SEM_INTERESSES, ERRO_RECOMENDACOES,INTERESSES_INVALIDOS
)

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
    elif aux_filmes[0] == INTERESSES_INVALIDOS: 
        #print("Modulo recomendacoes: Não foi possível calcular a recomendação pois lista de interesses é inválida!\n")
        return (ERRO_RECOMENDACOES, [])    
    
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
        return (0, ranking_final)
    
    except Exception:
        #print("Modulo recomendacoes: Não foi possível calcular a recomendação!\n")
        return (ERRO_RECOMENDACOES, [])