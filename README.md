# 🤖 Bot de Telegram — Mossegalapoma

Bot de Telegram per al grup de [Mossegalapoma](https://mossegalapoma.cat), el podcast de tecnologia en català. Gestiona propostes de contingut, links d'Amazon amb afiliats, agraïments i alguns easter eggs.

---

## Funcionalitats

### 📋 Propostes de contingut
Quan un membre del grup escriu un missatge amb un hashtag de proposta (per exemple `#proposta`, `#propostamossegui`...), el bot el detecta i el reenvía al grup intern de propostes.

Hi ha tres casos:
- **Missatge directe** — el hashtag va al mateix missatge que la proposta. El bot confirma la recepció i envia el contingut al grup de propostes amb el nom de l'autor.
- **Resposta a un missatge** — el hashtag va en un reply sobre un missatge existent. El bot reenvía el missatge original (amb el cap de "Reenviat de...") i afegeix un comentari amb qui l'ha proposat.
- **Missatge editat** — si s'edita un missatge que ja tenia un hashtag de proposta, el bot torna a processar-lo i avisa al grup de propostes que hi ha hagut un canvi (amb el cap ✏️).

El format original del missatge (negreta, cursiva, tatxat, etc.) es preserva correctament al reenviar-lo.

### ❌ Fe d'errates
Hashtags com `#federrates` o `#federrades` activen el mateix flux que les propostes però amb missatges de confirmació específics.

### 🛒 Links d'Amazon amb afiliats
Quan algú comparteix un link d'Amazon sense el tag d'afiliats, el bot:
1. Detecta el link (suporta `amazon.es`, `amazon.com` i links curts `amzn.eu`)
2. Resol els links curts a la URL completa
3. Afegeix el tag d'afiliats (`&tag=pempins-21`) i respon amb el link corregit

### 🎁 Palasaca / Agraïments
Quan es detecten paraules clau com `#palasaca`, `#afiliats` o mencions a compres via afiliats, el bot respon amb un missatge d'agraïment o un GIF animat obtingut de Giphy.

### 🚀 The Mandalorian
Hashtags com `#thisistheway` o `#mandalorian` fan que el bot respongui amb un GIF temàtic.

---

## Arquitectura

```
main.py          # Entry point, handler principal i webhook per a GCF
handlers.py      # Lògica de propostes (directes, replies, editades, palasaca)
amazon.py        # Detecció i processament de links d'Amazon
utils.py         # Client de Giphy
constants.py     # Configuració, tokens i llistes de respostes
```

El bot utilitza [python-telegram-bot v21](https://python-telegram-bot.org/) i segueix el patró recomanat per a entorns serverless: `asyncio.run()` + `async with app:` per gestionar el cicle de vida de l'aplicació per request.

---

## Desplegament — Google Cloud Functions (2ª gen)

El bot està allotjat a **Google Cloud Functions** (2ª generació, sobre Cloud Run) a la regió `europe-west1`.

### Variables d'entorn necessàries
| Variable | Descripció |
|---|---|
| `TELEGRAM_TOKEN` | Token del bot obtingut a [@BotFather](https://t.me/BotFather) |
| `GIPHY_API_KEY` | API key de [Giphy](https://developers.giphy.com/) |

### Entry point
```
webhook
```

### Deploy via CLI
```bash
gcloud functions deploy propostes \
  --gen2 \
  --runtime python312 \
  --region europe-west1 \
  --entry-point webhook \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars TELEGRAM_TOKEN=<token>,GIPHY_API_KEY=<key>
```

### Registrar el webhook a Telegram
Un cop desplegada la funció, cal registrar la URL a Telegram:
```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<URL_DE_LA_FUNCIÓ>
```

Per verificar que el webhook està actiu:
```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/getWebhookInfo
```

---

## Desenvolupament local

### Instal·lació
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Executar en local (polling)
Canvia `G_CLOUD = False` a `constants.py` i executa:
```bash
python main.py
```

### Tests
```bash
pytest
```

24 tests cobreixen tots els handlers, el flux d'Amazon, la detecció de tipus d'update (reaccions, edicions) i la preservació del format dels missatges.

