import streamlit as st
from utils.database import carregar_banco, salvar_banco
import hashlib

st.set_page_config(page_title="Cadastro de Aluno", page_icon="📝")
st.title("📝 Cadastro de Aluno")

def gerar_usuario_senha(nome):
    nome_sem_espaco = nome.replace(" ", "").lower()
    partes_nome = nome.lower().split()
    primeiro_nome = partes_nome[0]
    usuario = nome_sem_espaco + "@belmonte"
    senha = primeiro_nome + "123456"
    return usuario, senha

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

banco = carregar_banco()

with st.form("cadastro_form"):
    nome = st.text_input("Nome Completo", max_chars=100)
    curso = st.text_input("Curso")
    matricula = st.text_input("Matrícula")
    cpf = st.text_input("CPF")
    data_nascimento = st.date_input("Data de Nascimento")
    dias_aula = st.text_input("Dias de Aula", help="Ex: Segunda, Quarta, Sexta")
    submit = st.form_submit_button("Cadastrar")

if submit:
    usuario, senha_gerada = gerar_usuario_senha(nome)

    novo_aluno = {
        "nome": nome,
        "curso": curso,
        "matricula": matricula,
        "cpf": cpf,
        "data_nascimento": str(data_nascimento),
        "dias_aula": dias_aula,
        "usuario": usuario,
        "senha": senha_gerada,
        "autorizado": False
    }

    banco["alunos"].append(novo_aluno)
    salvar_banco(banco)

    st.success("Cadastro realizado com sucesso!")
    st.info(f"Seu usuário é: **{usuario}**")
    st.info(f"Sua senha é: **{senha_gerada}**")
    st.warning("Aguarde a aprovação do administrador para gerar sua carteirinha.")
