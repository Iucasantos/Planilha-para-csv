import os
import re
import uuid
import sys
import pandas as pd
pasta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pasta_raiz not in sys.path:
    sys.path.append(pasta_raiz)
from scanner import incopar_scan

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


p,pfp = incopar_scan()

pfp_planos=pfp.iloc[0,1:6]
pfp_normal = pfp.iloc[1:11,0:6].copy()

nomes=pfp.columns[1:6]
colunas=pfp.iloc[0,1:6]

principal_incopar= pd.DataFrame({
    "Codigo_Plano":nomes,
    "Nome": colunas 
})
principal_incopar = principal_incopar.reset_index(drop=True)

def trimming(linha):
    texto = str(linha["Nome"]).strip()
    Tipo_Cobertura = ""

    if "Nosso Plano" in texto:
        plano = "Nosso Plano"
        local = texto.replace("Nosso Plano","").strip()
        if "Ambulatorial" in texto:
            Tipo_Cobertura = "Ambulatorial" 
            local = local.replace("Ambulatorial","").strip()   
        else:
            Tipo_Cobertura = "" 
    
    elif "Nosso Médico" in texto:

        plano = "Nosso Médico"
        local = texto.replace("Nosso Médico","").strip()
        if "Ambulatorial" in texto:
            Tipo_Cobertura = "Ambulatorial" 
            local = local.replace("Ambulatorial","").strip()
        else:
            Tipo_Cobertura = "" 

    else:
        plano = None
        local = texto

    convert = {
        "Enf.":"Enfermaria",
        "Apto.":"Apartamento"
    }

    local_limpo = local.strip()
    atendimento=convert.get(local_limpo,local_limpo)

    return pd.Series([plano,atendimento,Tipo_Cobertura])

resultado = principal_incopar.apply(trimming,axis=1)
resultado = resultado.rename(columns={
    0: "Plano",
    1: "Acomodacao",
    2: "Tipo_Cobertura"
})

resultado["Codigo_Plano"] = principal_incopar["Codigo_Plano"]

principal_incopar = pd.merge(principal_incopar, resultado, on='Codigo_Plano', how='left')

principal_incopar["Operadora"] = "Hapvida%"
principal_incopar["Porcentagem_Promocao"] = "15%"
principal_incopar["Descricao_Promocao"] = "15% de desconto nas 3 primeiras mensalidades"
principal_incopar["Promocao_Ativa"] = True
principal_incopar["Ativo"] = True
principal_incopar["Coparticipacao"] = "Parcial"
principal_incopar["Cobertura"] = "Municipal"
principal_incopar["Observacao"] = ""
principal_incopar["Id"] = [str(uuid.uuid4()) for _ in range(len(principal_incopar))]
principal_incopar["Descricao_Plano"] = ""

principal_incopar["Codigo_Plano"] = principal_incopar["Codigo_Plano"].astype(str)
p["Codigo_Plano"] = p["Codigo_Plano"].astype(str)

colunas_p = ["Codigo_Plano", "Tipo_Rede", "Tipo_Contratacao", "Tipo_Rede_Nacional", "Registro_ANS", "Min_Beneficiarios", "Max_Beneficiarios"]
p_filtrada = p[colunas_p].drop_duplicates(subset=["Codigo_Plano"], keep="first")
principal_incopar = principal_incopar.merge(p_filtrada, on="Codigo_Plano", how="left")
nao_existe = principal_incopar["Registro_ANS"].isna()

principal_incopar.loc[nao_existe, "Tipo_Cobertura"] = "Ambulatorial + Hospitalar com Obstetrícia"
principal_incopar.loc[nao_existe, "Min_Beneficiarios"] = 1
principal_incopar = principal_incopar.fillna("")
principal_incopar["Tipo_Contratacao"] = "PME"

limpar_int = lambda val: str(int(float(val))) if (val != "" and pd.notna(val)) else ""
principal_incopar["Min_Beneficiarios"] = principal_incopar["Min_Beneficiarios"].apply(limpar_int)
principal_incopar["Max_Beneficiarios"] = principal_incopar["Max_Beneficiarios"].apply(limpar_int)
def principal_incopar(principal_incopar):
    return principal_incopar[[
    "Id",
    "Operadora", 
    "Nome", 
    "Registro_ANS", 
    "Codigo_Plano", 
    "Coparticipacao", 
    "Acomodacao", 
    "Tipo_Contratacao", 
    "Cobertura", 
    "Tipo_Cobertura", 
    "Tipo_Rede", 
    "Tipo_Rede_Nacional", 
    "Observacao", 
    "Min_Beneficiarios", 
    "Max_Beneficiarios", 
    "Ativo", 
    "Descricao_Plano", 
    "Promocao_Ativa", 
    "Porcentagem_Promocao", 
    "Descricao_Promocao"
]]

print(principal_incopar)
#&=======================================================================================================================================
pfp_normal.columns = ["Faixa_Etaria"] + list(principal_incopar["Codigo_Plano"].unique())

tabela_b_longa = pd.melt(
    pfp_normal, 
    id_vars=["Faixa_Etaria"], 
    var_name="Codigo_Plano", 
    value_name="Valor"
)

tabela_b_longa["Codigo_Plano"] = tabela_b_longa["Codigo_Plano"].astype(str)

tabela_incopar = pd.merge(
    principal_incopar[["Id", "Codigo_Plano"]],tabela_b_longa,on="Codigo_Plano",how="inner")

tabela_incopar[['Idade_Min', 'Idade_Max']] = tabela_incopar['Faixa_Etaria'].str.extract(r'(\d+)\D*(\d*)')
tabela_incopar.loc[tabela_incopar['Idade_Max'] == '', 'Idade_Max'] = '120'
def tabela_incopar():
    return tabela_incopar[["Id", "Idade_Min", "Idade_Max", "Valor"]]