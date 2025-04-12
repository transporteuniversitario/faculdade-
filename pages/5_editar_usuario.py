# editar_usuario.py

import streamlit as st
from utils.layout import cabecalho_pag, rodape
from utils.auth import carregar_usuarios, salvar_usuarios

cabecalho_pag("Editar Usuário")

usuarios = carregar_usuarios()

usuario_escolhido = st.selectbox("Selecione o usuário", [u["usuario"] for u in usuarios if u["tipo"] != "admin"])

usuario = next((u for u in usuarios if u["usuario"] == usuario_escolhido), None)

if usuario:
    nome = st.text_input("Nome", value=usuario["nome"])
    email = st.text_input("E-mail", value=usuario["email"])
    aprovado = st.checkbox("Aprovado", value=usuario.get("aprovado", False))

    if st.button("Salvar Alterações"):
        usuario["nome"] = nome
        usuario["email"] = email
        usuario["aprovado"] = aprovado
        salvar_usuarios(usuarios)
        st.success("Dados atualizados com sucesso.")
rodape()
