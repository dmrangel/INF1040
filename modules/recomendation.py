def buscaRecomendacoes(userID):
    aux = buscaInteresses(userID)

    if (aux[0] == -1):
        #print("Modulo recomendacoes: Modulo Usuario retornou erro")
        return (-1, [])
    elif (aux[0] == 2):
        #print("Modulo recomendacoes: Usuário não existente!")
        return (2, [])
    #TODO discutir se a saída 5 e 6 pode ser unificada
    elif (aux[0] == 5):
        #print("Modulo recomendacoes: Usuario não possui interesses!")
        return (5, [])

    listaInteresses = aux[1]

    


    return -1;