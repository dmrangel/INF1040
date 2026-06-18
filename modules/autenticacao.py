import uuid
import hashlib
from modules.codigos import (
    ERRO, SUCESSO, USUARIO_EXISTENTE,
    USUARIO_NAO_EXISTENTE, SENHA_INVALIDA, SENHA_INCORRETA,
)

#***********************************************************************
# Módulo: autenticação
# Descrição: Funções auxiliares e de autenticação para registro e login
#            de usuários, com hashing de senha e geração de UUID.
#***********************************************************************

#-----------------------------------------------------------------------
# _gerar_id_usuario (função interna)
#
# Descrição:
#   Gera um identificador único universal (UUID v4) para um novo usuário.
#
# Acoplamento:
#   (sem parâmetros)
#
# Retorno:
#   (str) – string UUID v4 no formato "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
#
# Assertivas de entrada:
#   - nenhuma pois não depende de estado externo
#
# Assertivas de saída:
#   - o retorno é sempre uma string UUID única e não vazia
#-----------------------------------------------------------------------
def _gerar_id_usuario():
    return str(uuid.uuid4())


#-----------------------------------------------------------------------
# _gerar_hash_senha (função interna)
#
# Descrição:
#   Gera o hash SHA-256 de uma senha em texto puro, codificada em UTF-8.
#
# Acoplamento:
#   senha   (str) – senha em texto puro a ser convertida em hash
#
# Retorno:
#   (str) – string hexadecimal de 64 caracteres representando o hash SHA-256
#
# Assertivas de entrada:
#   - senha é uma string não nula
#
# Assertivas de saída:
#   - o retorno é sempre uma string de 64 caracteres hexadecimais
#   - a mesma senha sempre gera o mesmo hash 
#   - senhas diferentes geram hashes diferentes 
#-----------------------------------------------------------------------
def _gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


#-----------------------------------------------------------------------
# _validar_forca_senha (função interna)
#
# Descrição:
#   Valida se a senha atende ao critério mínimo de força: ao menos 6 caracteres.
#
# Acoplamento:
#   senha   (str) – senha a ser validada
#
# Retorno:
#   (bool) – True se a senha tem 6 ou mais caracteres e False caso contrário
#
# Assertivas de entrada:
#   - senha é uma string não null
#
# Assertivas de saída:
#   - o retorno é sempre um booleano
#-----------------------------------------------------------------------
def _validar_forca_senha(senha):
    return len(senha) >= 6


#-----------------------------------------------------------------------
# registraUsuario
#
# Descrição:
#   Registra um novo usuário na estrutura de dados, gerando UUID e
#   armazenando a senha como hash SHA-256. Impede duplicatas por nome.
#
# Acoplamento:
#   dados      (dict) – estrutura de dados principal carregada do arquivo;
#                       deve conter a chave "usuarios" mapeando UUIDs a objetos
#   nomeUser   (str)  – nome de usuário desejado
#   senhaUser  (str)  – senha em texto puro do novo usuário
#
# Retorno:
#   (SUCESSO, str)           – UUID gerado para o novo usuário
#   (ERRO, None)             – dados inválidos ou não carregados
#   (SENHA_INVALIDA, None)   – senha não atende ao critério mínimo de força
#   (USUARIO_EXISTENTE, None) – já existe um usuário com o mesmo nome
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - nomeUser é uma string não vazia
#   - senhaUser é uma string não nula
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre um dos códigos definidos em modules.codigos
#   - se SUCESSO, o novo usuário é inserido em dados["usuarios"] com id, nome, senha (hash) e interesses vazios
#   - se SUCESSO, o segundo elemento é o UUID string do novo usuário
#   - em qualquer caso de erro, o segundo elemento é None
#   - a senha nunca é armazenada em texto puro
#-----------------------------------------------------------------------
def registraUsuario(dados, nomeUser: str, senhaUser: str) -> tuple:
    if not _validar_forca_senha(senhaUser):
        return (SENHA_INVALIDA, None)

    if dados is None:
        return (ERRO, None)

    for info_usuario in dados["usuarios"].values():
        if info_usuario["nome"] == nomeUser:
            return (USUARIO_EXISTENTE, None)

    novo_id = _gerar_id_usuario()
    dados["usuarios"][novo_id] = {
        "id": novo_id,
        "nome": nomeUser,
        "senha": _gerar_hash_senha(senhaUser),
        "interesses": []
    }

    return (SUCESSO, novo_id)


#-----------------------------------------------------------------------
# loginUsuario
#
# Descrição:
#   Autentica um usuário verificando nome e senha (comparada via hash).
#   Retorna o UUID do usuário em caso de sucesso.
#
# Acoplamento:
#   dados      (dict) – estrutura de dados principal carregada do arquivo;
#                       deve conter a chave "usuarios" mapeando UUIDs a objetos
#   nomeUser   (str)  – nome do usuário a autenticar
#   senhaUser  (str)  – senha em texto puro a ser verificada
#
# Retorno:
#   (SUCESSO, str)             – UUID do usuário autenticado
#   (ERRO, None)               – dados inválidos ou não carregados
#   (SENHA_INCORRETA, None)    – usuário encontrado mas senha não confere
#   (USUARIO_NAO_EXISTENTE, None) – nenhum usuário com o nome informado
#
# Assertivas de entrada:
#   - dados é None ou um dict com a chave "usuarios"
#   - nomeUser é uma string não vazia
#   - senhaUser é uma string não nula
#
# Assertivas de saída:
#   - o primeiro elemento da tupla é sempre um dos códigos definidos em modules.codigos
#   - se SUCESSO, o segundo elemento é o UUID string do usuário autenticado
#   - em qualquer caso de erro, o segundo elemento é None
#   - a comparação de senha é feita exclusivamente via hash (nunca texto puro)
#   - SENHA_INCORRETA só ocorre se o nome for encontrado; caso contrário é USUARIO_NAO_EXISTENTE
#-----------------------------------------------------------------------
def loginUsuario(dados, nomeUser: str, senhaUser: str) -> tuple:
    if dados is None:
        return (ERRO, None)

    for id_usuario, info_usuario in dados["usuarios"].items():
        if info_usuario["nome"] == nomeUser:
            if info_usuario["senha"] == _gerar_hash_senha(senhaUser):
                return (SUCESSO, id_usuario)
            else:
                return (SENHA_INCORRETA, None)

    return (USUARIO_NAO_EXISTENTE, None)
