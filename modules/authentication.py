import json
import os
import uuid
import hashlib

# Caminho para o arquivo de dados JSON
ARQUIVO_DADOS = 'dados.json'

# Códigos de retorno conforme especificação
CODIGO_ERRO = -1
CODIGO_SUCESSO = 0
CODIGO_USUARIO_EXISTENTE = 1
CODIGO_USUARIO_NAO_EXISTENTE = 2
CODIGO_SENHA_INVALIDA = 3
CODIGO_SENHA_INCORRETA = 4

def _carregar_dados():
    """Carrega os dados do arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return {"users": {}, "movies": []}
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        # Retorna uma estrutura vazia se o JSON estiver corrompido
        return {"users": {}, "movies": []}
    except Exception:
        return None # Indica erro crítico de leitura

def _salvar_dados(dados):
    """Salva os dados no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False # Indica erro crítico de escrita

def _gerar_id_usuario():
    """Gera um ID de usuário único."""
    return str(uuid.uuid4())

def _gerar_hash_senha(senha):
    """Gera um hash SHA256 da senha para armazenamento seguro."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def _validar_forca_senha(senha):
    """Valida a força da senha (ex: mínimo 6 caracteres)."""
    return len(senha) >= 6 # Exemplo simples: mínimo 6 caracteres

def registraUsuario(nomeUser: str, senhaUser: str) -> tuple:
    """
    Registra um novo usuário no sistema.
    Retorna (codigo, idUsuario)
    """
    if not _validar_forca_senha(senhaUser):
        return (CODIGO_SENHA_INVALIDA, None)

    dados = _carregar_dados()
    if dados is None: # Erro crítico ao carregar dados
        return (CODIGO_ERRO, None)

    for id_usuario, info_usuario in dados["users"].items():
        if info_usuario["nomeUser"] == nomeUser:
            return (CODIGO_USUARIO_EXISTENTE, None)

    novo_id_usuario = _gerar_id_usuario()
    senha_hash = _gerar_hash_senha(senhaUser)

    dados["users"][novo_id_usuario] = {
        "nomeUser": nomeUser,
        "senhaUser": senha_hash,
        "interesses": [] # Inicializa com lista de interesses vazia
    }

    if not _salvar_dados(dados): # Erro crítico ao salvar dados
        return (CODIGO_ERRO, None)

    return (CODIGO_SUCESSO, novo_id_usuario)

def loginUsuario(nomeUser: str, senhaUser: str) -> tuple:
    """
    Realiza o login de um usuário no sistema.
    Retorna (codigo, idUsuario)
    """
    dados = _carregar_dados()
    if dados is None: # Erro crítico ao carregar dados
        return (CODIGO_ERRO, None)

    for id_usuario, info_usuario in dados["users"].items():
        if info_usuario["nomeUser"] == nomeUser:
            if info_usuario["senhaUser"] == _gerar_hash_senha(senhaUser):
                return (CODIGO_SUCESSO, id_usuario)
            else:
                return (CODIGO_SENHA_INCORRETA, None)
    
    return (CODIGO_USUARIO_NAO_EXISTENTE, None)