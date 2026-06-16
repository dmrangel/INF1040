import streamlit as st  # pyright: ignore[reportMissingImports]

try:
    from modules import filme
except ImportError:
    filme = None

try:
    from modules import recomendacoes
except ImportError:
    recomendacoes = None


def _render_row(filmes):
    cards_html = ""
    for f in filmes:
        nome = f.get("nome", "").title()
        tags = " · ".join(g.capitalize() for g in f.get("generos", []))
        cards_html += (
            f'<div style="min-width:160px;max-width:160px;margin-right:12px;display:inline-block;vertical-align:top;">'
            f'<div style="width:160px;height:240px;background:#2a2a2a;border-radius:6px;margin-bottom:6px;"></div>'
            f'<div style="font-weight:bold;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{nome}</div>'
            f'<div style="font-size:12px;color:#888;">{tags}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div style="overflow-x:auto;white-space:nowrap;padding-bottom:16px;">{cards_html}</div>',
        unsafe_allow_html=True,
    )


def search(dados):
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
        st.session_state.search_error = False

    gap, input_search, search_btn = st.columns([0.5, 2, 1], vertical_alignment="bottom")

    with input_search:
        input_filme = st.text_input("Pesquisar filmes", label_visibility="hidden")
    with search_btn:
        if st.button("Pesquisar"):
            if filme:
                code, resultados = filme.buscaFilme(dados, input_filme)
                if code == 0:
                    st.session_state.search_results = resultados
                    st.session_state.search_error = False
                else:
                    st.session_state.search_results = None
                    st.session_state.search_error = True

    if st.session_state.search_results is not None:
        st.markdown("### Resultados")
        _render_row(st.session_state.search_results)
    elif st.session_state.search_error:
        st.error("Nenhum filme encontrado.")


def recommendation(dados):
    if not st.session_state.pesquisa:
        return

    st.markdown("### Recomendações")

    todos_filmes = []
    if recomendacoes and "usuario_logado" in st.session_state:
        id_usuario = st.session_state["usuario_logado"]["id"]
        code, result = recomendacoes.buscaRecomendacoes(dados, id_usuario)
        if code == 0 and result:
            todos_filmes = result

    if not todos_filmes:
        return

    _render_row(todos_filmes)


def login(dados):
    gap, login_reg = st.columns([4, 1], vertical_alignment="top")
    if "logado" not in st.session_state:
        st.session_state.logado = False
    if not st.session_state.logado:
        with login_reg:
            st.page_link("pages/login.py", label="Entrar")
    else:
        with login_reg:
            nome_usuario = st.session_state["usuario_logado"]["nome"]
            with st.popover(f"{nome_usuario}", width="stretch", type="tertiary"):
                st.page_link("pages/research.py", label="Pesquisa de interesses")
                if st.button("Desconectar", type="primary"):
                    del st.session_state["usuario_logado"]
                    st.session_state["logado"] = False
                    st.session_state["pesquisa"] = False
                    st.rerun()


def research(dados):
    if not st.session_state.pesquisa and st.session_state.logado:
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.page_link("pages/research.py", label="Realize a pesquisa de interesses!")


def feed(dados):
    if not dados:
        return

    filmes = dados.get("filmes", [])
    generos: dict[str, list] = {}
    for f in filmes:
        for g in f.get("generos", []):
            generos.setdefault(g, []).append(f)

    for genero, lista in sorted(generos.items()):
        st.markdown(f"### {genero.capitalize()}")
        _render_row(lista)
