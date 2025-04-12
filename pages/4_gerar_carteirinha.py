import streamlit as st
import os
from utils.auth import get_user_data, logout
from utils.gerar_carteirinha import gerar_carteirinha
from PIL import Image

cabecalho_pag("Gerar Carteirinha")

usuario = usuario_autenticado()

user_data = get_user_data()
if not user_data:
    st.warning("Faça login para continuar.")
    st.stop()

st.title("Minha Carteirinha")

if not user_data.get("aprovado", False):
    st.info("Seu cadastro ainda não foi aprovado pelo administrador.")
    st.stop()

if st.button("Gerar Carteirinha"):
    path_img = gerar_carteirinha(user_data)
    if os.path.exists(path_img):
        st.image(Image.open(path_img), caption="Carteirinha Gerada", use_column_width=True)
        st.success("Carteirinha gerada com sucesso!")

st.button("Sair", on_click=logout)
