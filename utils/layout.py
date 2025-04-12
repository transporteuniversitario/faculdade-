# utils/layout.py

import streamlit as st

def cabecalho_pag(titulo):
    st.markdown(f"""
        <div style='text-align:center; padding: 10px; background-color: #003366; color: white;'>
            <h2>{titulo}</h2>
        </div>
    """, unsafe_allow_html=True)

def rodape():
    st.markdown("""
        <hr style='margin-top: 40px;'>
        <div style='text-align: center; font-size: 13px; color: gray;'>
            Desenvolvido por Secretaria de Educação de Belmonte - 2024
        </div>
    """, unsafe_allow_html=True)
