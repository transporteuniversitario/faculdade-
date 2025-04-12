import json
import os

CAMINHO_BANCO = "base_de_dados.json"

def carregar_banco():
    if not os.path.exists(CAMINHO_BANCO):
        return {"usuarios": [], "alunos": []}
    with open(CAMINHO_BANCO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_banco(banco):
    with open(CAMINHO_BANCO, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=4)
