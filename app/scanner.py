import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8-sig")

PLANOS = os.getenv("P")
PLANOS_FAIXAS_PRECO = os.getenv("PFP")

p = pd.read_excel(f"Dados/{PLANOS}")
pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}")
