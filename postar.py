"""
postar.py
---------
Junta as ofertas (ofertas.json) com os links de afiliado que você colou
manualmente (links_gerados.txt) e publica automaticamente no Telegram
e no Instagram. Também gera um arquivo "para_whatsapp.txt" pronto pra
você colar no Canal do WhatsApp (posta manual, ~30s por oferta - não
existe automação oficial/segura pra isso ainda).

Pré-requisitos antes de rodar:
  1. preparar.py já rodou e gerou ofertas.json + urls_para_colar.txt
  2. Você colou o conteúdo de urls_para_colar.txt no Gerador de Link
     do Mercado Livre, copiou o resultado e salvou em links_gerados.txt
     (um link por linha, NA MESMA ORDEM de urls_para_colar.txt)
"""

import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


def carregar_ofertas_com_links():
    with open("ofertas.json", "r", encoding="utf-8") as f:
        ofertas = json.load(f)

    if not ofertas:
        return []

    try:
        with open("links_gerados.txt", "r", encoding="utf-8") as f:
            links = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print("ERRO: links_gerados.txt não encontrado. "
              "Faça o passo manual no Mercado Livre antes de postar.")
        return []

    if len(links) < len(ofertas):
        print(f"AVISO: {len(ofertas)} ofertas mas só {len(links)} links. "
              "Publicando só o que tem link correspondente.")

    for oferta, link in zip(ofertas, links):
        oferta["link_afiliado"] = link

    return [o for o in ofertas if o.get("link_afiliado")]


def montar_legenda(oferta):
    return (
        f"🔥 {oferta['titulo']}\n\n"
        f"~~R$ {oferta['preco_original']:.2f}~~\n"
        f"💰 R$ {oferta['preco_atual']:.2f}  ({oferta['desconto']}% OFF)\n\n"
        f"🔗 {oferta['link_afiliado']}\n\n"
        f"#ofertas #achadinhos #promocao"
    )


def postar_telegram(oferta):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram não configurado (faltam variáveis de ambiente).")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": montar_legenda(oferta),
        "photo": oferta["imagem"],
    }
    resp = requests.post(url, data=payload, timeout=15)
    if resp.status_code != 200:
        print(f"[Telegram] erro ao postar '{oferta['titulo']}': {resp.text}")
        return False
    return True


def postar_instagram(oferta, cliente_ig=None):
    """
    Posta no Instagram via instagrapi (login não-oficial).
    ATENÇÃO: automatizar login do Instagram viola os termos de uso da
    plataforma e pode resultar em bloqueio/banimento da conta. Use por
    sua conta e risco, de preferência numa conta secundária/comercial.
    """
    if cliente_ig is None:
        return False

    try:
        img_bytes = requests.get(oferta["imagem"], timeout=15).content
        caminho_temp = f"/tmp/{abs(hash(oferta['url']))}.jpg"
        with open(caminho_temp, "wb") as f:
            f.write(img_bytes)

        cliente_ig.photo_upload(caminho_temp, montar_legenda(oferta))
        return True
    except Exception as e:
        print(f"[Instagram] erro ao postar '{oferta['titulo']}': {e}")
        return False


def conectar_instagram():
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        print("Instagram não configurado (faltam variáveis de ambiente).")
        return None
    try:
        from instagrapi import Client
        cl = Client()
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        return cl
    except Exception as e:
        print(f"[Instagram] falha ao logar: {e}")
        return None


def gerar_arquivo_whatsapp(ofertas):
    """
    Gera um arquivo de texto com todas as legendas prontas, cada uma
    separada por uma linha de traços, pra você copiar e colar uma por
    uma no Canal do WhatsApp (postagem manual - ver aviso no README).
    """
    with open("para_whatsapp.txt", "w", encoding="utf-8") as f:
        for oferta in ofertas:
            f.write(montar_legenda(oferta))
            f.write("\n\n" + ("-" * 40) + "\n\n")
    print("Legendas prontas pra colar no WhatsApp em: para_whatsapp.txt")


def main():
    ofertas = carregar_ofertas_com_links()
    if not ofertas:
        print("Nada para postar hoje.")
        return

    cliente_ig = conectar_instagram()

    for oferta in ofertas:
        ok_tg = postar_telegram(oferta)
        ok_ig = postar_instagram(oferta, cliente_ig)
        print(f"{oferta['titulo'][:40]:40s} | Telegram: {ok_tg} | Instagram: {ok_ig}")
        time.sleep(5)  # evita postar tudo de uma vez / parecer spam

    gerar_arquivo_whatsapp(ofertas)


if __name__ == "__main__":
    main()
