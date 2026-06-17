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
    interesses_atuais = [i[0] for i in dados["usuarios"][id_usuario].get("interesses", [])]

    generos = filme.obterGeneros(dados)

    st.write("Selecione os gêneros que você gosta:")
    selecionados = st.multiselect(
        "Gêneros",
        options=generos,
        default=interesses_atuais,
        format_func=lambda g: g.capitalize(),
        label_visibility="collapsed",
    )

    if st.button("Salvar interesses", type="primary"):
        if interesses_atuais:
            code, _ = pesquisa.modificaInteresses(dados, id_usuario, selecionados)
        else:
            code, _ = pesquisa.criaInteresses(dados, id_usuario, selecionados)

        if code == 0:
            st.session_state.pesquisa = True
            st.success("Interesses salvos com sucesso!")
        else:
            st.error("Erro ao salvar interesses.")

if __name__ == "__main__":
    main()
