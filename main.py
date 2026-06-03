import streamlit as st # pyright: ignore[reportMissingImports]
import json
import pandas as pd

from modules import filme

def carregaJson() -> dict:
	with open("dados.json", "r") as f:
		dados = json.load(f)
	return dados

def main() -> None:
	dados = carregaJson()

	title_left, title_center, title_right = st.columns([1, 4, 1])
	input_search, search = st.columns([3, 1], vertical_alignment="bottom")
	df_left, df_center, df_right = st.columns([1,4,1])

	with title_center:
		st.title("Catálogo de Filmes")
		st.write("INF1040 - Proj Prog Modular 2026.1 - 3WA - Grupo 2")
	
	with input_search:
		input_filme = st.text_input("Pesquisar filmes", label_visibility="hidden")
	with search:
		if st.button("Pesquisar"):
			dict_filme = filme.buscaFilme(dados, input_filme)
			with df_center:
				table = pd.DataFrame(dict_filme)
				st.dataframe(table)
			

if __name__ == "__main__":
	main()
