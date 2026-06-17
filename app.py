import streamlit as st  # pyright: ignore[reportMissingImports]
st.set_page_config(initial_sidebar_state="collapsed")
if "pesquisa" not in st.session_state:
    st.session_state.pesquisa = False

from modules import arquivo
from ui.functions import (
    login, search, recommendation, feed, research
)

def main():
    if "dados" not in st.session_state:
        st.session_state["dados"] = arquivo.carregaJson()

    dados = st.session_state["dados"]

    login(dados)

    gap, title, gap2 = st.columns([1, 4, 1])
    with title:
        st.title("Catálogo de Filmes")

    search(dados)

    recommendation(dados)

    feed(dados)

    arquivo.salvaJson(dados)


if __name__ == "__main__":
    main()
