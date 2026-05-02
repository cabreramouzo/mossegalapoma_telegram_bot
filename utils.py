from telegram import Update
from telegram.ext import ContextTypes
import requests
import datetime
import random
from constants import GIPHY_API_KEY


async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    missatge = str(datetime.datetime.now())
    await update.effective_message.reply_text(text=missatge)

def get_giphy_url(search_terms):
    """
    Searches Giphy for a GIF and returns the URL of the original file.
    """
    if not GIPHY_API_KEY:
        return None
        
    search_term = random.choice(search_terms)
    try:
        params = {
            "api_key": GIPHY_API_KEY,
            "q": search_term,
            "limit": 5,
            "rating": "g" # Safe content rating
        }
        r = requests.get("https://api.giphy.com/v1/gifs/search", params=params, timeout=5)
        
        if r.status_code == 200:
            results = r.json().get('data', [])
            if results:
                # Giphy returns the direct URL in this structure:
                selected_gif = random.choice(results)
                return selected_gif['images']['original']['url']
    except Exception as e:
        print(f"Giphy error: {e}")
    
    return None