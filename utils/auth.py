# utils/auth.py

import json
import os

CAMINHO_BANCO = "base_de_dados.json"

def autenticar_admin(usuario, senha):
    # Exemplo simples (substituir pela lógica real)
    return usuario == "admin@belmonte" and senha == "admin123"

def gerar_credenciais_aluno(nome_completo):
    nome_usuario = nome_completo.lower().replace(" ", "") + "@belmonte"
    senha = nome_completo.strip().split()[0].lower() + "123456"
    return nome_usuario, senha

def carregar_dados():
    if os.path.exists(CAMINHO_BANCO):
        with open(CAMINHO_BANCO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"usuarios": []}

def salvar_dados(data):
    with open(CAMINHO_BANCO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
