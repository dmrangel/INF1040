import streamlit as st # pyright: ignore[reportMissingImports]
try:
	from modules import usuario, autenticacao
	from modules.codigos import (
		SUCESSO, USUARIO_EXISTENTE, USUARIO_NAO_EXISTENTE,
		SENHA_INVALIDA, SENHA_INCORRETA,
	)
except ImportError:
	usuario = autenticacao = None

def _set_logged_in(dados, nome_usuario):
	_, info = usuario.buscaUsuario(dados, nome_usuario)
	st.session_state["usuario_logado"] = info
	st.session_state["logado"] = True

def main():
	st.page_link("app.py", label="<")
	_, title_col = st.columns([1, 3.5])
	with title_col:
		st.title("Entrar ou Registrar")

	_, form_col, _ = st.columns([1, 1, 1])
	_, login_bttn, register_bttn, _ = st.columns([2.2, 1, 1, 2], vertical_alignment="top")

	with form_col:
		user = st.text_input("Usuário:")
		pw = st.text_input("Senha:", type="password")

	with login_bttn:
		if st.button("Entrar", width=80, type="primary"):
			if not user or not pw:
				st.error("Preencha usuário e senha")
			elif autenticacao is None or usuario is None:
				st.switch_page("app.py")
			else:
				dados = st.session_state.get("dados")
				code, _ = autenticacao.loginUsuario(dados, user, pw)
				if code == SUCESSO:
					_set_logged_in(dados, user)
					st.switch_page("app.py")
				elif code in (USUARIO_NAO_EXISTENTE, SENHA_INCORRETA):
					st.error("Dados incorretos ou usuário não existente")
				else:
					st.error("Erro")

	with register_bttn:
		if st.button("Registrar", width=80):
			if not user or not pw:
				st.error("Preencha usuário e senha")
			elif autenticacao is None or usuario is None:
				st.switch_page("app.py")
			else:
				dados = st.session_state.get("dados")
				code, _ = autenticacao.registraUsuario(dados, user, pw)
				if code == SUCESSO:
					_set_logged_in(dados, user)
					st.switch_page("app.py")
				elif code == USUARIO_EXISTENTE:
					st.error("Usuário já existente")
				elif code == SENHA_INVALIDA:
					st.error("Senha inválida (mínimo 6 caracteres)")
				else:
					st.error("Erro")

if __name__ == "__main__":
	main()