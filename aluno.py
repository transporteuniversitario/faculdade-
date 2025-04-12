import streamlit as st
import os
import json
from utils.auth import gerar_credenciais_aluno

ALUNOS_DB = "dados/alunos.json"  # ou "data/alunos.json"

# Garante que a pasta existe
os.makedirs(os.path.dirname(ALUNOS_DB), exist_ok=True)

# Se o arquivo não existir, crie um vazio
if not os.path.exists(ALUNOS_DB):
    with open(ALUNOS_DB, "w") as f:
        json.dump([], f)

def salvar_aluno(aluno):
    with open(ALUNOS_DB, "r") as f:
        dados = json.load(f)
    dados.append(aluno)
    with open(ALUNOS_DB, "w") as f:
        json.dump(dados, f, indent=4)

st.title("Cadastro de Aluno")
with st.form("form_cadastro"):
    nome = st.text_input("Nome completo")
    matricula = st.text_input("Matrícula")
    curso = st.text_input("Curso")
    cpf = st.text_input("CPF")
    data_nascimento = st.date_input("Data de Nascimento")
    dias_aula = st.text_input("Dias de Aula (ex: Segunda, Quarta)")
    foto = st.file_uploader("Foto", type=["jpg", "jpeg", "png"])

    enviar = st.form_submit_button("Cadastrar")

if enviar:
    if nome and matricula and curso:
        usuario, senha = gerar_credenciais_aluno(nome)
        aluno = {
            "nome": nome,
            "usuario": usuario,
            "senha": senha,
            "matricula": matricula,
            "curso": curso,
            "cpf": cpf,
            "data_nascimento": str(data_nascimento),
            "dias_aula": dias_aula,
            "foto_nome": foto.name if foto else "",
            "status": "pendente"
        }

        if foto:
            with open(f"static/fotos/{foto.name}", "wb") as f:
                f.write(foto.getbuffer())

        salvar_aluno(aluno)
        st.success("Cadastro enviado! Aguarde aprovação do administrador.")
        st.info(f"Usuário gerado: `{usuario}`\nSenha: `{senha}`")
    else:
        st.warning("Preencha os campos obrigatórios.")
