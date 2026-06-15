import copy
import hashlib
import pytest


def _hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


DADOS_BASE = {
    "usuarios": {
        "u_alice": {
            "id": "u_alice",
            "nome": "alice",
            "senha": _hash("senha123"),
            "interesses": [["acao", 5], ["drama", 3]],
        },
        "u_bob": {
            "id": "u_bob",
            "nome": "bob",
            "senha": _hash("senha456"),
            "interesses": [],
        },
    },
    "filmes": [
        {"id": "f1", "nome": "matrix",    "generos": ["acao", "ficcao"]},
        {"id": "f2", "nome": "titanic",   "generos": ["romance", "drama"]},
        {"id": "f3", "nome": "toy story", "generos": ["animacao", "aventura"]},
        {"id": "f4", "nome": "parasita",  "generos": ["suspense", "drama"]},
        {"id": "f5", "nome": "alien",     "generos": ["ficcao", "terror"]},
        {"id": "f6", "nome": "shrek",     "generos": ["animacao", "comedia"]},
        {"id": "f7", "nome": "gladiador", "generos": ["acao", "historico"]},
        {"id": "f8", "nome": "clube da luta",   "generos": ["drama", "suspense"]},
        {"id": "f9", "nome": "o iluminado",     "generos": ["terror", "suspense"]},
        {"id": "f10", "nome": "vingadores",     "generos": ["acao", "aventura"]},
        {"id": "f11", "nome": "interestelar",   "generos": ["ficcao", "drama"]},
    ],
}


@pytest.fixture
def mock_dados(monkeypatch):
    """Isolates every test from the real dados.json."""
    store = {"data": copy.deepcopy(DADOS_BASE)}

    def fake_carrega():
        return copy.deepcopy(store["data"])

    def fake_salva(d):
        store["data"] = copy.deepcopy(d)
        return True

    monkeypatch.setattr("modules.arquivo.carregaJson", fake_carrega)
    monkeypatch.setattr("modules.arquivo.salvaJson", fake_salva)
    return store
