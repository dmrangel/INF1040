import streamlit as st  # pyright: ignore[reportMissingImports]

try:
    from modules import pesquisa, filme
except ImportError:
    pesquisa = filme = None


def main():
    st.page_link("app.py", label="<")
    gap, title, gap2 = st.columns([1, 4, 1])
    with title:
        st.write("# Pesquisa de Interesse")

    if not st.session_state.logado:
        st.warning("Você precisa estar logado para realizar a pesquisa.")
        st.stop()

    if pesquisa is None or filme is None:
        st.error("Módulo não disponível.")
        st.stop()

    dados = st.session_state.get("dados")
    id_usuario = st.session_state["usuario_logado"]["id"]

    # interesses atuais como {genero: peso}, para pre-preencher o formulario
    interesses_atuais = {
        genero: peso
        for genero, peso in dados["usuarios"][id_usuario].get("interesses", [])
    }

    generos = filme.obterGeneros(dados)

    st.write("Selecione os gêneros que você gosta e diga o quanto gosta de cada um:")
    selecionados = st.multiselect(
        "Gêneros",
        options=generos,
        default=list(interesses_atuais.keys()),
        format_func=lambda g: g.capitalize(),
        label_visibility="collapsed",
    )

    # um slider de peso (1 a 10) por genero selecionado
    pesos = {}
    for genero in selecionados:
        pesos[genero] = st.slider(
            f"Peso de {genero.capitalize()}",
            min_value=1,
            max_value=10,
            value=interesses_atuais.get(genero, 5),
        )

    if st.button("Salvar interesses", type="primary"):
        if not selecionados:
            st.error("Selecione ao menos um gênero.")
        else:
            if interesses_atuais:  # ja existia pesquisa -> modifica
                code, _ = pesquisa.modificaInteresses(dados, id_usuario, list(pesos.items()))
            else:                  # primeira pesquisa -> cria
                code, _ = pesquisa.criaInteresses(dados, id_usuario, pesos)

            if code == 0:
                st.session_state.pesquisa = True
                st.success("Interesses salvos com sucesso!")
            else:
                st.error("Erro ao salvar interesses.")


if __name__ == "__main__":
    main()
