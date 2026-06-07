def buscaFilme(dados, nomeFilme):
	if dados:
		if nomeFilme:
			filmes = dados["filmes"]
			if filmes:
				for filme in filmes:
					if filme["nome"] == nomeFilme:
						return 0, filme
		else:
			return 0, dados["filmes"]
	
	return -1, {}