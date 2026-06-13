import pytest
import json
import os
from modules.authentication import (
    registraUsuario, loginUsuario,
    CODIGO_ERRO, CODIGO_SUCESSO, CODIGO_USUARIO_EXISTENTE,
    CODIGO_USUARIO_NAO_EXISTENTE, CODIGO_SENHA_INVALIDA, CODIGO_SENHA_INCORRETA,
    ARQUIVO_DADOS, _gerar_hash_senha
)

# Fixture para garantir um arquivo dados.json limpo para cada teste
@pytest.fixture(autouse=True)
def configurar_e_limpar_arquivo_dados():
    # Cria um arquivo dados.json vazio antes de cada teste
    dados_iniciais = {"users": {}, "movies": []}
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_iniciais, arquivo, indent=2, ensure_ascii=False)
    yield
    # Remove o arquivo dados.json após cada teste
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)

# --- Testes para registraUsuario ---

# Caso 21: Sucesso no Registro
def test_registra_usuario_sucesso():
    nome = "novo_usuario"
    senha = "senha_segura123"
    codigo, id_usuario = registraUsuario(nome, senha)
    assert codigo == CODIGO_SUCESSO
    assert id_usuario is not None
    assert isinstance(id_usuario, str)

    # Verifica se o usuário foi salvo no JSON
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        assert id_usuario in dados["users"]
        assert dados["users"][id_usuario]["nomeUser"] == nome
        assert dados["users"][id_usuario]["senhaUser"] == _gerar_hash_senha(senha)

# Caso 22: Usuário já cadastrado
def test_registra_usuario_existente():
    nome = "usuario_existente"
    senha = "senha123"
    
    # Registra o usuário uma primeira vez
    registraUsuario(nome, senha)
    
    # Tenta registrar o mesmo usuário novamente
    codigo, id_usuario = registraUsuario(nome, senha)
    assert codigo == CODIGO_USUARIO_EXISTENTE
    assert id_usuario is None

# Caso 23: Senha fora dos padrões
def test_registra_usuario_senha_invalida():
    nome = "usuario_senha_fraca"
    senha = "abc" # Senha muito curta (exemplo de validação)
    codigo, id_usuario = registraUsuario(nome, senha)
    assert codigo == CODIGO_SENHA_INVALIDA
    assert id_usuario is None

# Caso 24: Falha crítica de sistema (simulando arquivo JSON inacessível/corrompido)
def test_registra_usuario_erro_critico_sistema(mocker):
    # Simula um erro ao salvar o arquivo JSON
    mocker.patch('modules.authentication._salvar_dados', return_value=False)
    
    nome = "usuario_erro_salvar"
    senha = "senha_valida123"
    codigo, id_usuario = registraUsuario(nome, senha)
    assert codigo == CODIGO_ERRO
    assert id_usuario is None

# --- Testes para loginUsuario ---

# Caso 25: Login bem-sucedido
def test_login_usuario_sucesso():
    nome = "usuario_login"
    senha = "senha_login123"
    codigo_reg, id_usuario_reg = registraUsuario(nome, senha)
    assert codigo_reg == CODIGO_SUCESSO

    codigo_login, id_usuario_login = loginUsuario(nome, senha)
    assert codigo_login == CODIGO_SUCESSO
    assert id_usuario_login == id_usuario_reg

# Caso 26: Usuário não cadastrado
def test_login_usuario_nao_cadastrado():
    nome = "usuario_inexistente"
    senha = "qualquer_senha"
    codigo, id_usuario = loginUsuario(nome, senha)
    assert codigo == CODIGO_USUARIO_NAO_EXISTENTE
    assert id_usuario is None

# Caso 27: Senha incorreta
def test_login_usuario_senha_incorreta():
    nome = "usuario_com_senha"
    senha_correta = "senha_correta123"
    registraUsuario(nome, senha_correta)

    senha_incorreta = "senha_errada"
    codigo, id_usuario = loginUsuario(nome, senha_incorreta)
    assert codigo == CODIGO_SENHA_INCORRETA
    assert id_usuario is None

# Caso 28: Falha técnica no login (simulando arquivo JSON inacessível/corrompido)
def test_login_usuario_erro_critico_sistema(mocker):
    # Simula um erro ao carregar o arquivo JSON
    mocker.patch('modules.authentication._carregar_dados', return_value=None)
    codigo, id_usuario = loginUsuario("qualquer_nome", "qualquer_senha")
    assert codigo == CODIGO_ERRO
    assert id_usuario is None