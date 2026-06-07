import json
import pandas as pd
import streamlit as st # pyright: ignore[reportMissingImports]
st.set_page_config(initial_sidebar_state="collapsed")

try:
    from modules import filme, recomendacoes, pesquisa
except ImportError:
    filme = recomendacoes = pesquisa = None

def carregaJson():
	with open("./dados.json", "r") as f:
		dados = json.load(f)
	return dados

def search(dados):
	gap, input_search, search = st.columns([0.5, 2, 1], vertical_alignment="bottom")
	gap2, df, gap3 = st.columns([1,4,1])

	with input_search:
		input_filme = st.text_input("Pesquisar filmes", label_visibility="hidden")
	with search:
		if st.button("Pesquisar"):
			if filme:
				code, dict_filme = filme.buscaFilme(dados, input_filme)
				if code == 0:
					with df:
						table = pd.DataFrame(dict_filme)
						st.dataframe(table)
				else:
					st.error("Erro")

def recomendation(dados):
	if recomendacoes:
		if "usuario_logado" in st.session_state:
			id_usuario = st.session_state["usuario_logado"]["id"]
			list_recomendacoes = recomendacoes.buscaRecomendacoes(id_usuario)
		else:
			filmes = filme.buscaFilme(dados, None)

def login(dados):
	gap, login_reg = st.columns([4,1], vertical_alignment="top")
	if "logado" not in st.session_state:
		st.session_state.logado = False
	if not st.session_state.logado:
		with login_reg:
			st.page_link("pages/login.py", label="Login")
	else:
		with login_reg:
			nome_usuario = st.session_state["usuario_logado"]["nome"]
			with st.popover(f"{nome_usuario}", width="stretch", type="tertiary"):
				if st.button("Desconectar"):
					del st.session_state["usuario_logado"]
					st.rerun

def main():
	dados = carregaJson()

	login(dados)

	gap, title, gap2 = st.columns([1, 4, 1])
	with title:
		st.title("Catálogo de Filmes")
	
	search(dados)

	recomendation(dados)

if __name__ == "__main__":
	main()
