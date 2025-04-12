import streamlit as st
import json
import os
from utils.auth import is_admin_logged_in, logout, load_usuarios, save_usuarios

cabecalho_pag("Gerenciar Usuários")

usuarios = carregar_usuarios()



def aprovar_usuario(email):
    usuarios = load_usuarios()
    for usuario in usuarios:
        if usuario['email'] == email:
            usuario['aprovado'] = True
            break
    save_usuarios(usuarios)

def remover_usuario(email):
    usuarios = load_usuarios()
    usuarios = [u for u in usuarios if u['email'] != email]
    save_usuarios(usuarios)

def editar_usuario(email, novo_nome, novo_email):
    usuarios = load_usuarios()
    for usuario in usuarios:
        if usuario['email'] == email:
            usuario['nome'] = novo_nome
            usuario['email'] = novo_email
            break
    save_usuarios(usuarios)

if not is_admin_logged_in():
    st.warning("Acesso restrito. Faça login como administrador.")
    st.stop()

st.title("Gerenciar Usuários")

usuarios = load_usuarios()

for usuario in usuarios:
    with st.expander(f"{usuario['nome']} ({usuario['email']})"):
        st.write("Aprovado:", usuario.get("aprovado", False))
        col1, col2, col3 = st.columns(3)

        if col1.button("Aprovar", key=f"aprovar_{usuario['email']}"):
            aprovar_usuario(usuario["email"])
            st.experimental_rerun()
        if col2.button("Remover", key=f"remover_{usuario['email']}"):
            remover_usuario(usuario["email"])
            st.experimental_rerun()
        if col3.button("Editar", key=f"editar_{usuario['email']}"):
            novo_nome = st.text_input("Novo nome", value=usuario['nome'], key=f"nome_{usuario['email']}")
            novo_email = st.text_input("Novo email", value=usuario['email'], key=f"email_{usuario['email']}")
            if st.button("Salvar alterações", key=f"salvar_{usuario['email']}"):
                editar_usuario(usuario["email"], novo_nome, novo_email)
                st.success("Usuário atualizado com sucesso!")
                st.experimental_rerun()

st.button("Sair", on_click=logout)
