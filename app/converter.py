from Logic.incopar import principal_incopar,tabela_incopar
from Logic.incoto import principal_incoto,tabela_incoto
from Logic.susipa import principal_susipa,tabela_susipa
from Logic.susito import principal_susito,tabela_susito
import pandas as pd

def func_principal(principal_incopar,principal_incoto,principal_susipa,principal_susito):
    return pd.concat([
        principal_incopar,principal_incoto,
        principal_susipa,principal_susito
    ],ignore_index=True)
def func_tabela(tabela_incopar,tabela_incoto,tabela_susipa,tabela_susito):
    return pd.concat([
        tabela_incopar,tabela_incoto,
        tabela_susipa,tabela_susito
    ],ignore_index=True)

principal = func_principal(principal_incopar,principal_incoto,principal_susipa,principal_susito)
tabela = func_tabela(tabela_incopar,tabela_incoto,tabela_susipa,tabela_susito)

def criar_csv(principal,tabela):
    principal.to_csv(
        "Output/planos.csv",
        index=False,
        header=False,
        encoding="utf-8-sig"
    )
    tabela.to_csv(
        "Output/planos_faixa_preco.csv",
        index=False,
        header=False,
        encoding="utf-8-sig"
    )