from modules import filme

def test_buscaFilmes():
	dados = {"filmes": [{"id": "f1", "nome": "matrix", "generos": ["acao", "ficcao"]}]}
	nomeFilme = "matrix"
	resultado = filme.buscaFilme(dados=dados, nomeFilme=nomeFilme)

	assert isinstance(resultado, dict)
	assert resultado["id"] == "f1"
	assert resultado["nome"] == "matrix"
	assert isinstance(resultado["generos"], list)
	assert resultado["generos"][0] == "acao"
	assert resultado["generos"][1] == "ficcao"