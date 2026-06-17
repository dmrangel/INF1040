import json

CAMINHO = "./dados.json"  # caminho do arquivo de dados

# Lê e retorna o conteúdo do JSON; retorna None em caso de erro
def carregaJson():
    try:
        with open(CAMINHO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # arquivo ausente ou corrompido
        return None

# Salva o dicionário de dados no JSON; retorna True se bem-sucedido
def salvaJson(dados):
    try:
        with open(CAMINHO, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)  # ensure_ascii=False preserva acentuação
        return True
    except Exception:
        return False
