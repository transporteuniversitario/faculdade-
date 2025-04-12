# visualizar_carteirinha.py

import streamlit as st
from utils.auth import carregar_usuarios
from utils.gerar_carteirinha import gerar_imagem_carteirinha
from utils.layout import cabecalho_pag, rodape
import os

cabecalho_pag("Visualizar Carteirinha de Alunos")

usuarios = carregar_usuarios()
alunos = [u for u in usuarios if u["tipo"] == "aluno" and u.get("aprovado")]

nome_usuario = st.selectbox("Selecione um aluno", [a["nome"] for a in alunos])

selecionado = next((a for a in alunos if a["nome"] == nome_usuario), None)

if selecionado:
    imagem_path = gerar_imagem_carteirinha(selecionado)
    if imagem_path and os.path.exists(imagem_path):
        st.image(imagem_path, caption=f"Carteirinha de {selecionado['nome']}", use_column_width=True)
        with open(imagem_path, "rb") as file:
            st.download_button("📥 Baixar Carteirinha", data=file, file_name="carteirinha.png", mime="image/png")
    else:
        st.warning("Erro ao gerar imagem.")
rodape()
