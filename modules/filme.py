def buscaFilme(dados, nomeFilme):
	if dados and nomeFilme:
		filmes = dados["filmes"]
		if filmes:
			for filme in filmes:
				if filme["nome"] == nomeFilme:
					return 0, filme
	
	return -1, {}