import streamlit as st
import sqlite3
from utils.autenticar import autenticar_usuario, gerar_credenciais
from utils.gerar_carteirinha import gerar_carteirinha
from utils.gerar_qrcode import gerar_qrcode
import os
from PIL import Image
from config import CONFIG

st.set_page_config(page_title="Carteirinhas Belmonte", layout="centered")

# Banco de dados
conn = sqlite3.connect("db/banco.db", check_same_thread=False)
c = conn.cursor()

# Criação das tabelas
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'aluno',
    autorizado INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS carteirinhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    matricula TEXT,
    curso TEXT,
    cpf TEXT,
    data_nascimento TEXT,
    dias_aula TEXT,
    validade TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)''')

conn.commit()

# Sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.session_state.tipo = None

# Funções de interface
def login():
    st.title("Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuario = autenticar_usuario(email, senha)
        if usuario:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.tipo = usuario[4]
            st.experimental_rerun()
        else:
            st.error("Credenciais inválidas.")

def cadastro():
    st.title("Cadastro de Aluno")
    nome = st.text_input("Nome completo")
    matricula = st.text_input("Matrícula")
    curso = st.text_input("Curso")
    cpf = st.text_input("CPF")
    nascimento = st.date_input("Data de nascimento")
    dias = st.text_input("Dias de aula (ex: Segunda, Quarta, Sexta)")

    if st.button("Cadastrar"):
        email, senha = gerar_credenciais(nome)
        c.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        usuario_id = c.lastrowid
        c.execute("INSERT INTO carteirinhas (usuario_id, matricula, curso, cpf, data_nascimento, dias_aula, validade) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (usuario_id, matricula, curso, cpf, nascimento.strftime('%d/%m/%Y'), dias, CONFIG['validade']))
        conn.commit()
        st.success(f"Cadastro enviado! Aguarde a autorização do administrador.\nLogin: {email} | Senha: {senha}")


def painel_admin():
    st.title("Painel do Administrador")
    st.header("Alunos pendentes de aprovação")
    pendentes = c.execute("SELECT * FROM usuarios WHERE autorizado = 0 AND tipo = 'aluno'").fetchall()
    for aluno in pendentes:
        st.write(f"{aluno[1]} ({aluno[2]})")
        if st.button(f"Aprovar {aluno[1]}"):
            c.execute("UPDATE usuarios SET autorizado = 1 WHERE id = ?", (aluno[0],))
            conn.commit()
            st.success(f"{aluno[1]} aprovado.")

    st.header("Todos os alunos")
    alunos = c.execute("SELECT * FROM usuarios WHERE tipo = 'aluno'").fetchall()
    for aluno in alunos:
        st.markdown(f"**{aluno[1]}** - {aluno[2]}")
        if st.button(f"Gerar Carteirinha {aluno[0]}"):
            dados = c.execute("SELECT * FROM carteirinhas WHERE usuario_id = ?", (aluno[0],)).fetchone()
            if dados:
                gerar_carteirinha(aluno, dados)
                st.success("Carteirinha gerada com sucesso!")
                st.image(f"assets/carteirinhas/{aluno[1].replace(' ', '_')}.png")


def painel_aluno():
    st.title("Área do Aluno")
    usuario = st.session_state.usuario
    if usuario[5] == 0:
        st.warning("Aguarde a aprovação do administrador.")
    else:
        st.success("Cadastro aprovado! Abaixo sua carteirinha.")
        caminho = f"assets/carteirinhas/{usuario[1].replace(' ', '_')}.png"
        if os.path.exists(caminho):
            st.image(caminho)
        else:
            st.info("Sua carteirinha ainda não foi gerada. Aguarde o administrador.")

# Layout principal
menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro", "Sair"])

if menu == "Login" and not st.session_state.autenticado:
    login()
elif menu == "Cadastro" and not st.session_state.autenticado:
    cadastro()
elif st.session_state.autenticado:
    if st.session_state.tipo == "admin":
        painel_admin()
    else:
        painel_aluno()
elif menu == "Sair":
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.session_state.tipo = None
    st.success("Você saiu da conta.")
