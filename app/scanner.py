import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8-sig")

PLANOS = os.getenv("P")
PLANOS_FAIXAS_PRECO = os.getenv("PFP")

#&===================|incoto|======================
def incoto_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}")
    return p, pfp
#&===================|incopar|======================
def incopar_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}", sheet_name=1)
    return p, pfp
#&===================|susipa|======================
def susipa_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}", sheet_name=3)
    return p, pfp
#&===================|susito|======================
def susito_scan():
    p = pd.read_excel(f"Dados/{PLANOS}")
    pfp = pd.read_excel(f"Dados/{PLANOS_FAIXAS_PRECO}", sheet_name=4)
    return p, pfp

    