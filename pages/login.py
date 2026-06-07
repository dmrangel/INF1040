import streamlit as st # pyright: ignore[reportMissingImports]
try:
	from modules import usuario, autenticacao
except ImportError:
	usuario = autenticacao = None

def main():
	st.page_link("app.py", label="<")
	gap, title = st.columns([1, 3.5])
	with title:
		st.title("Entrar ou Registrar")

	gap, input, gap2  = st.columns([1,1,1])
	gap3, login_bttn, register_bttn, gap4 = st.columns([2.2,1,1,2], vertical_alignment="bottom")
	with input:
		user = st.text_input("Usuário:")
		pw = st.text_input("Senha:")
	with login_bttn:
		if st.button("Entrar", width=80, type="primary"):
			if usuario:
				code, info_usuario = usuario.buscaUsuario(user)
				if code == 0:
					st.session_state["usuario_logado"] = info_usuario
					st.switch_page("app.py")
				elif code == 2:
					st.error("Dados incorretos ou usuário não existente")
				else:
					st.error("Erro")
			else:
				st.switch_page("app.py")

	with register_bttn:
		if st.button("Registrar", width=80):
			if usuario:
				code, info_usuario = autenticacao.registraUsuario(user, pw)
				if code == 0:
					st.session_state["usuario_logado"] = info_usuario
					st.switch_page("app.py")
				elif code == 1:
					st.error("Usuário já existente")
				elif code == 3:
					st.error("Senha inválida")
				else:
					st.error("Erro")
	
if __name__ == "__main__":
	main()