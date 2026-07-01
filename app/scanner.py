import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8-sig")

PLANOS = os.getenv("P")
PLANOS_FAIXAS_PRECO = os.getenv("PFP")

#&===================|incoto|======================
def validate_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}")
    return p, pfp

#&===================|incopar|======================
def validate_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}", sheet_name=1)
    return p, pfp
#&===================|incopar|======================