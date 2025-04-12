import os
import datetime
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO

# Função para gerar imagem da carteirinha com layout personalizado
def gerar_carteirinha(carteirinha, diretorio_saida='carteirinhas_geradas'):
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)

    largura, altura = 800, 500
    imagem = Image.new('RGB', (largura, altura), (255, 255, 255))
    draw = ImageDraw.Draw(imagem)
    
    # Carregar fontes (ajuste o caminho conforme seu projeto)
    try:
        fonte_titulo = ImageFont.truetype("arialbd.ttf", 28)
        fonte_texto = ImageFont.truetype("arial.ttf", 22)
    except:
        fonte_titulo = ImageFont.load_default()
        fonte_texto = ImageFont.load_default()

    # Cabeçalho
    draw.rectangle([0, 0, largura, 80], fill=(0, 102, 204))
    draw.text((20, 20), carteirinha["cabecalho"], font=fonte_titulo, fill=(255, 255, 255))

    # Informações
    draw.text((150, 100), f"Nome: {carteirinha['nome']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 130), f"Curso: {carteirinha['curso']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 160), f"Matrícula: {carteirinha['matricula']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 190), f"CPF: {carteirinha['cpf']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 220), f"Nascimento: {carteirinha['nascimento']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 250), f"Dias de Aula: {carteirinha['dias_aula']}", font=fonte_texto, fill=(0, 0, 0))
    draw.text((150, 280), f"Validade: {carteirinha['validade']}", font=fonte_texto, fill=(255, 0, 0))

    # Assinatura
    if carteirinha.get("assinatura"):
        assinatura = Image.open(carteirinha["assinatura"]).resize((120, 50))
        imagem.paste(assinatura, (150, 320))
    draw.text((150, 380), f"{carteirinha['secretario']}", font=fonte_texto, fill=(0, 0, 0))

    # Foto
    if carteirinha.get("foto"):
        foto = Image.open(carteirinha["foto"]).resize((120, 140))
        imagem.paste(foto, (20, 100))

    # Logos
    if carteirinha.get("logo_prefeitura"):
        prefeitura = Image.open(carteirinha["logo_prefeitura"]).resize((100, 60))
        imagem.paste(prefeitura, (650, 20))
    if carteirinha.get("logo_secretaria"):
        secretaria = Image.open(carteirinha["logo_secretaria"]).resize((100, 60))
        imagem.paste(secretaria, (530, 20))

    # QR Code
    dados_qr = f"Nome: {carteirinha['nome']}\nCurso: {carteirinha['curso']}\nValidade: {carteirinha['validade']}"
    qr = qrcode.make(dados_qr)
    qr = qr.resize((120, 120))
    imagem.paste(qr, (650, 350))

    nome_arquivo = f"carteirinha_{carteirinha['matricula']}.png"
    caminho_arquivo = os.path.join(diretorio_saida, nome_arquivo)
    imagem.save(caminho_arquivo)

    return caminho_arquivo
