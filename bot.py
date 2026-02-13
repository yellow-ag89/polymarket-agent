import os
import time
import requests
from exa_py import Exa
import google.generativeai as genai

# Caricamento chiavi (usa quelle che hai già messo su Railway)
EXA_KEY = os.getenv("EXA_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

exa = Exa(api_key=EXA_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def invia_telegram(messaggio):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "text": messaggio}
    requests.get(url, params=params)

print("--- SIMULATORE DI GUERRA AVVIATO ---")
invia_telegram("🤖 Agente in modalità Ombra attivato. Inizio simulazione scommesse.")

while True:
    try:
        # 1. SCANNERIZZA I MERCATI (Dati pubblici, no login richiesto)
        resp = requests.get("https://clob.polymarket.com/markets")
        mercati = resp.json()[:5] # Analizziamo i primi 5 per test
        
        for m in mercati:
            domanda = m.get('question', 'N/A')
            prezzo = m.get('last_trade_price', 0.5)
            
            # 2. CERCA NOTIZIE SUL TEMA
            news = exa.search(domanda, num_results=3)
            
            # 3. L'IA RAGIONA
            prompt = f"Analizza: {domanda}. Prezzo attuale: {prezzo}. News: {news}. Se la probabilità di vittoria è > 80%, scrivi 'SCOMMESSA SIMULATA'. Altrimenti 'PASSA'."
            risposta = model.generate_content(prompt).text
            
            if "SCOMMESSA SIMULATA" in risposta:
                invia_telegram(f"🎯 SCOMMESSA TEORICA:\nEvento: {domanda}\nPrezzo: {prezzo}\nMotivazione: {risposta[:100]}...")

        time.sleep(3600) # Controlla ogni ora per non bruciare i 5$ di Railway
    except Exception as e:
        print(f"Errore: {e}")
        time.sleep(300)
