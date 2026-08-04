# Bot de Afiliados - Mercado Livre

Bot semi-automático que posta ofertas escolhidas por você no Telegram,
Instagram e (manualmente) no Canal do WhatsApp, usando o link de
afiliado `rafaelrafa13`.

## Por que não é 100% automático

Duas plataformas não permitem automação total sem quebrar as regras:

- **Mercado Livre** não tem API pública pra gerar link de afiliado
  automaticamente — só pelo Portal, manual.
- **Canais do WhatsApp** ainda não têm API oficial da Meta pra postar
  programaticamente — as ferramentas que fazem isso usam automação
  não-oficial (mesmo risco de banimento das ferramentas de "disparo em
  massa").

Por isso o fluxo tem 2 partes manuais rápidas (juntas, ~15 min/dia) e
o resto é 100% automático.

## Rotina diária

**1. Você escolhe as ofertas (~10 min)**
   Abra o Mercado Livre, escolha 5-10 produtos com desconto bom pro
   seu nicho (academia, roupas de marca, produtos pet). Preencha o
   arquivo `entrada_ofertas.txt` com os dados de cada um (título,
   preço de/por, link do produto, link da imagem).

**2. Rode `preparar.py` (automático)**
   ```bash
   python preparar.py
   ```
   Isso gera `urls_para_colar.txt` com todos os links dos produtos.

**3. Gere os links de afiliado (~2 min, manual)**
   - Copie o conteúdo de `urls_para_colar.txt`
   - Cole no [Gerador de Link](https://www.mercadolivre.com.br/afiliados)
     do Portal de Afiliados e clique em Gerar
   - Copie os links gerados (na mesma ordem) e cole em
     `links_gerados.txt`, um por linha

**4. Rode `postar.py` (automático)**
   ```bash
   python postar.py
   ```
   Isso:
   - Posta automaticamente no Telegram (canal @FitAchados)
   - Posta automaticamente no Instagram
   - Gera `para_whatsapp.txt` com as legendas prontas — você só
     copia e cola cada uma no Canal do WhatsApp (~30s por oferta)

## Deixando 1-4 no automático via GitHub Actions

Se você preencher `entrada_ofertas.txt` e `links_gerados.txt` e subir
pro repositório, o workflow roda sozinho todo dia às 20h (Brasília) e
faz os passos 2 e 4 automaticamente. Ele também deixa disponível pra
download o arquivo `para_whatsapp.txt` pronto (aba **Actions** → o
run do dia → seção **Artifacts**).

Pra rodar manualmente e testar: aba **Actions** → **Bot de Afiliados**
→ **Run workflow**.

## Configuração necessária (Settings → Secrets and variables → Actions)

| Secret | O que é |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token do @AchadosFitBot |
| `TELEGRAM_CHAT_ID` | `@FitAchados` |
| `INSTAGRAM_USERNAME` | usuário da conta comercial |
| `INSTAGRAM_PASSWORD` | senha da conta |

## Rodando no seu computador (opcional, pra testar antes)

```bash
pip install -r requirements.txt
cp .env.example .env
# edite o .env com seus dados
python preparar.py
# faça o passo manual no Mercado Livre
python postar.py
```

## Avisos importantes

- **Instagram:** login automatizado (via `instagrapi`) não é um método
  oficial e pode resultar em bloqueio da conta. Use numa conta
  secundária/comercial dedicada, evite volume alto por dia.
- **WhatsApp:** de propósito deixamos a postagem manual. Ferramentas
  que automatizam Canais do WhatsApp usam conexão não-oficial via QR
  Code e podem banir o número conectado — o mesmo risco das
  plataformas de "disparo em massa" pra grupos. Se um dia quiser
  automatizar isso mesmo assim, pesquise bem e use um número
  secundário, nunca o principal.
