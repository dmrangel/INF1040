import json

CAMINHO = "./dados.json"

def carregaJson():
    try:
        with open(CAMINHO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def salvaJson(dados):
    try:
        with open(CAMINHO, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False