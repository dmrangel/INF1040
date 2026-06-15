import streamlit as st  # pyright: ignore[reportMissingImports]

try:
    from modules import arquivo
except ImportError:
    arquivo = None

try:
    from modules import pesquisa
except ImportError:
    pesquisa = None

def main():
    st.page_link("app.py", label="<")
    gap, title, gap2 = st.columns([1, 4, 1])
    with title:
         st.write("# Pesquisa de Interesse")

    if not st.session_state.logado:
        st.warning("Você precisa estar logado para realizar a pesquisa.")
        st.stop()

    if pesquisa is None or arquivo is None:
        st.error("Módulo não disponível.")
        st.stop()

    dados = arquivo.carregaJson()
    id_usuario = st.session_state["usuario_logado"]["id"]
    interesses_atuais = [i[0] for i in dados["usuarios"][id_usuario].get("interesses", [])]

    generos = pesquisa.obterGeneros(dados)

    st.write("Selecione os gêneros que você gosta:")
    selecionados = st.multiselect(
        "Gêneros",
        options=generos,
        default=interesses_atuais,
        format_func=lambda g: g.capitalize(),
        label_visibility="collapsed",
    )

    if st.button("Salvar interesses", type="primary"):
        pesquisa.salvarInteresses(dados, id_usuario, selecionados)
        st.session_state.pesquisa = True
        st.success("Interesses salvos com sucesso!")

if __name__ == "__main__":
    main()
