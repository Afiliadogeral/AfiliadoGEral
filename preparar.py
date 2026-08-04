"""
preparar.py
-----------
Lê o arquivo entrada_ofertas.txt (preenchido manualmente por você com
as ofertas que escolheu no Mercado Livre) e gera:

  - ofertas.json           -> dados estruturados de cada oferta
  - urls_para_colar.txt    -> lista de URLs, pronta pra colar no
                               Gerador de Link de Afiliado do Mercado Livre
"""

import json

ENTRADA = "entrada_ofertas.txt"


def parse_bloco(bloco):
    dados = {}
    for linha in bloco.strip().splitlines():
        if ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        dados[chave.strip()] = valor.strip()
    return dados


def carregar_ofertas():
    with open(ENTRADA, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # ignora tudo que vem antes do primeiro bloco de comentário "# ==="
    blocos = conteudo.split("---")

    ofertas = []
    for bloco in blocos:
        dados = parse_bloco(bloco)
        titulo = dados.get("titulo", "").strip()
        url = dados.get("url", "").strip()

        if not titulo or not url:
            continue  # bloco vazio ou de exemplo não preenchido

        try:
            preco_de = float(dados.get("preco_de", "0").replace(",", "."))
            preco_por = float(dados.get("preco_por", "0").replace(",", "."))
        except ValueError:
            print(f"[aviso] preço inválido em '{titulo}', pulando produto.")
            continue

        desconto = 0
        if preco_de > 0 and preco_de > preco_por:
            desconto = round((1 - preco_por / preco_de) * 100)

        ofertas.append({
            "titulo": titulo,
            "preco_original": preco_de,
            "preco_atual": preco_por,
            "desconto": desconto,
            "url": url,
            "imagem": dados.get("imagem", "").strip(),
        })

    return ofertas


def main():
    ofertas = carregar_ofertas()

    if not ofertas:
        print("Nenhuma oferta válida encontrada em entrada_ofertas.txt. "
              "Preencha o arquivo com pelo menos um produto real.")

    with open("ofertas.json", "w", encoding="utf-8") as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)

    with open("urls_para_colar.txt", "w", encoding="utf-8") as f:
        for oferta in ofertas:
            f.write(oferta["url"] + "\n")

    print(f"{len(ofertas)} oferta(s) prontas.")
    print("Próximo passo: cole o conteúdo de urls_para_colar.txt no "
          "Gerador de Link do Mercado Livre e salve o resultado em "
          "links_gerados.txt (mesma ordem).")


if __name__ == "__main__":
    main()
