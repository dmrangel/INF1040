from modules.filme import buscaFilmesRecomendados
from modules.usuario import buscaInteresses

def buscaRecomendacoes(dados, userID):
    aux = buscaInteresses(dados, userID)

    if (aux[0] == -1):
        #print("Modulo recomendacoes: Modulo Usuario retornou erro!\n")
        return (-1, [])
    elif (aux[0] == 2):
        #print("Modulo recomendacoes: Usuário não existente!\n")
        return (2, [])
    #TODO discutir se a saída 5 e 6 pode ser unificada
    elif (aux[0] == 6):
        #print("Modulo recomendacoes: Usuario não possui interesses!\n")
        return (5, [])

    listaInteressesComPesos = aux[1]

    mapaPesos = {item[0]: item[1] for item in listaInteressesComPesos}

    listaGenerosApenas = list(mapaPesos.keys())

    aux_filmes = buscaFilmesRecomendados(dados, listaGenerosApenas)

    if aux_filmes[0] == -1:
        #print("Modulo recomendacoes: Modulo Filmes retornou erro!\n")
        return (-1, [])
    elif aux_filmes[0] == 8: 
        #print("Modulo recomendacoes: Não foi possível calcular a recomendação pois lista de interesses é inválida!\n")
        return (7, [])    
    
    filmes_completos = aux_filmes[1]

    try:
        # 3. ALGORITMO DE PRIORIDADE e CÁLCULO DE SCORE
        filmes_com_score = []
        
        for filme in filmes_completos:
            score = 0
            # Soma o peso de cada gênero do filme que coincide com o interesse do usuário
            for g in filme["generos"]:
                if g in mapaPesos:
                    score += mapaPesos[g]
            
            # Guarda o filme junto com o seu score calculado
            filmes_com_score.append((filme, score))
        
        # Ordena a lista pelo score de forma DECRESCENTE (maiores scores na posição 0)
        filmes_com_score.sort(key=lambda x: x[1], reverse=True)
        
        lista_ids = [str(item[0]['id']) for item in filmes_com_score]
        ranking_final = lista_ids[:10]
        
        #print("Modulo recomendacoes: Retorno padrão de êxito\n")
        return (0, ranking_final)
    
    except Exception:
        #print("Modulo recomendacoes: Não foi possível calcular a recomendação!\n")
        return (7, [])