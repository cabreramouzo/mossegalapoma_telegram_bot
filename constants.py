import os

# --- CONFIGURATION & CONSTANTS ---
INTERNAL_VERSION = '2.0'
G_CLOUD = True  # Change to false for local mode

GROUP_PROPOSALS_DEV = -1001965997481 
GROUP_PROPOSALS = -1001928595896
TAG_AMAZON = '&tag=pempins-21'
GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# --- REPLY TEXT LISTS ---
HASHTAGS_PROPOSTA = [
    '#propostamossegui', '#proposta', '#propostesmossegui', '#propostesmosseguis',
    '#propostamosseguis', '#propostamosegui', '#propostamoseguis', '#propostesmosegui',
    '#propostesmoseguis'
]
FEDERRATES = ['#federrates', '#federrades', '#federates', "fe d'errates"]

PALASACA = [
    '#palasaca', '#amazon', '#palasaka', '#afiliats', 'compra per afiliats', 
    'compra feta per afiliats', 'comprat via afiliats', 'compra via afiliats'
]
THIS_IS_THE_WAY = ['#thisistheway', '#thiswastheway', '#aquesteselcami', '#mandalorian']

TEXT_TROLL_REPLY = [
    f"Això no té pinta de proposta... 😒", f"Ets un troll!!! 😝",
    f"Ho tens clar! 🙄", f"Alerta...TROLL!!! 🚨"
]

TEXT_REPLY_ERRATA = [
    "Una altra vegada!? 😫", "Deixa'm apostar: Ha estat en Ludo 😒",
    "Sort en tenim de vosaltres! 😅", "Anoto la fe d'errates! 📝"
]

TEXT_REPLY_PROPOSAL = [
    f"Anoto la proposta! 💪", f"Proposta anotada 😉", f"Els hi anoto la proposta 😁",
    f"L'apunto! 📬", f"Els la deixo al guió 📮", f"Apuntada! 📎", 
    f"Viatjant cap al guió... 🚀", f"Clar que sí! 🤖", f"Fot-li! 😜"
]

TEXT_REPLY_EDITED_PROPOSAL = [
    f"Anoto l'edició de la proposta! ✏️",
    f"Veig que has canviat d'opinió, la anoto 😉",
    f"Va, no l'editis més que em canso! 🙄"
]

TEXT_REPLY_PALASACA = [
    f"En @tomasmanz i tot l'equip t'estem molt agraïts! 😘",
    f"Gràcies! Cada dia estem més aprop del Tesla Model S... 😜",
    f"La targeta fot fum!!! 🔥💨", f"De mica en mica s'omple la pica! 🚰💰"
]

TEXT_REPLY_AFILIATS_LINK = [
    f"M'ha semblat veure un link d'Amazon sense afiliats 🤔: ",
    f"Gràcies per recomanar un producte! Li afegeixo l'enllaç d'afiliats 😜: ",
    f"Amazon? Afiliats!!! 🔥💰: ", f"Enllaç d'afiliats al canto! 🚨: "
]