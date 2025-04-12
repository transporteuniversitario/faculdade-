import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))import streamlit as st
import json
from utils.auth import autenticar_admin
from utils.gerar_carteirinha import gerar_imagem_carteirinha
from datetime import datetime

# Caminhos dos arquivos
ALUNOS_DB = "data/alunos.json"
CONFIG_DB = "data/config.json"

# Carrega dados de alunos
def carregar_alunos():
    if os.path.exists(ALUNOS_DB):
        with open(ALUNOS_DB, "r") as f:
            return json.load(f)
    return []

# Salva dados dos alunos
def salvar_alunos(alunos):
    with open(ALUNOS_DB, "w") as f:
        json.dump(alunos, f, indent=4)

# Carrega configurações globais
def carregar_config():
    if os.path.exists(CONFIG_DB):
        with open(CONFIG_DB, "r") as f:
            return json.load(f)
    return {}

# Salva configurações globais
def salvar_config(config):
    with open(CONFIG_DB, "w") as f:
        json.dump(config, f, indent=4)

st.title("Painel do Administrador")

# Login do admin
with st.expander("Login de Administrador"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    logar = st.button("Entrar")

if logar:
    if autenticar_admin(usuario, senha):
        st.session_state['admin_logado'] = True
    else:
        st.error("Credenciais inválidas!")

# Se admin estiver logado
if st.session_state.get("admin_logado"):

    st.success("Administrador logado!")

    # Aprovação de cadastros pendentes
    alunos = carregar_alunos()
    pendentes = [a for a in alunos if a["status"] == "pendente"]
    if pendentes:
        st.subheader("Aprovar Alunos")
        for aluno in pendentes:
            with st.expander(f"{aluno['nome']} ({aluno['usuario']})"):
                st.write(f"Curso: {aluno['curso']}")
                st.write(f"Matrícula: {aluno['matricula']}")
                st.write(f"CPF: {aluno['cpf']}")
                st.write(f"Dias de Aula: {aluno['dias_aula']}")
                if aluno['foto_nome']:
                    st.image(f"static/fotos/{aluno['foto_nome']}", width=100)
                if st.button("Aprovar", key=aluno['usuario']):
                    aluno["status"] = "aprovado"
                    gerar_imagem_carteirinha(aluno)
                    salvar_alunos(alunos)
                    st.success(f"{aluno['nome']} aprovado!")

    else:
        st.info("Nenhum cadastro pendente.")

    # Edição de configurações globais
    st.subheader("Editar Informações Globais")
    config = carregar_config()

    validade = st.text_input("Validade das carteirinhas", value=config.get("validade", "31/12/2025"))
    nome_secretario = st.text_input("Nome do Secretário", value=config.get("nome_secretario", "Secretário de Educação"))

    assinatura = st.file_uploader("Assinatura do Secretário", type=["png", "jpg", "jpeg"])
    logo_prefeitura = st.file_uploader("Logo da Prefeitura", type=["png", "jpg", "jpeg"])
    logo_secretaria = st.file_uploader("Logo da Secretaria", type=["png", "jpg", "jpeg"])

    if st.button("Salvar Configurações"):
        config["validade"] = validade
        config["nome_secretario"] = nome_secretario

        if assinatura:
            assinatura_path = f"static/assinaturas/{assinatura.name}"
            with open(assinatura_path, "wb") as f:
                f.write(assinatura.getbuffer())
            config["assinatura"] = assinatura_path

        if logo_prefeitura:
            prefeitura_path = f"static/logos/{logo_prefeitura.name}"
            with open(prefeitura_path, "wb") as f:
                f.write(logo_prefeitura.getbuffer())
            config["logo_prefeitura"] = prefeitura_path

        if logo_secretaria:
            secretaria_path = f"static/logos/{logo_secretaria.name}"
            with open(secretaria_path, "wb") as f:
                f.write(logo_secretaria.getbuffer())
            config["logo_secretaria"] = secretaria_path

        salvar_config(config)
        st.success("Configurações atualizadas com sucesso!")



