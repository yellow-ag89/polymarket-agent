import os
import time
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from exa_py import Exa
import google.generativeai as genai

load_dotenv()

# Configurazione API
exa = Exa(api_key=os.getenv("EXA_KEY"))
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Connessione al Mercato
client = ClobClient(
    host="https://clob.polymarket.com",
    key=os.getenv("WALLET_PRIVATE_KEY"),
    address=os.getenv("WALLET_ADDRESS")
)

print("Sistemi avviati. Inizio scansione mercati...")

while True:
    try:
        # L'agente cerca notizie e decide cosa fare
        print("Analisi in corso...")
        # (Qui il bot esegue la logica di scommessa)
        time.sleep(300) # Aspetta 5 minuti
    except Exception as e:
        print(f"Errore: {e}")
        time.sleep(60)
