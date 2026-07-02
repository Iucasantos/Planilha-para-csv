import os
import uuid
import sys
import pandas as pd
pasta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pasta_raiz not in sys.path:
    sys.path.append(pasta_raiz)
from scanner import susito_scan

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

p,pfp = susito_scan()

faixa = pfp.iloc[1:11,0].copy()
pfp_planos=pfp.iloc[0,1:5]
pfp_normal = pfp.iloc[1:11,1:5].copy()
print(pfp_planos)

nomes=pfp.columns[1:5]
colunas=pfp.iloc[0,1:5]

principal_susito= pd.DataFrame({
    "Codigo_Plano":nomes,
    "Nome": colunas 
})

principal_susito = principal_susito.reset_index(drop=True)

def trimming(linha):
    texto = str(linha["Nome"]).strip()
    Tipo_Cobertura = ""

    if "Nosso Plano" in texto:
        plano = "Nosso Plano"
        resto = texto.replace("Nosso Plano","").strip()
        if "Enf." in resto:
            local = "Enfermaria"
            Cobertura = resto.replace("Enf.","").strip()
            Tipo_Cobertura = "" 
        elif "Apto." in resto:
            local = "Apartamento"
            Cobertura = resto.replace("Apto.","").strip()
            Tipo_Cobertura = "" 
        elif "Ambulatorial" in resto:
            Tipo_Cobertura = "Ambulatorial"
            Cobertura = resto.replace("Ambulatorial","").strip()
            local = ""

    elif "Nosso Médico" in texto:
        plano = "Nosso Médico"
        resto = texto.replace("Nosso Médico","").strip()
        
        if "Enf." in resto:
            local = "Enfermaria"
            Cobertura = resto.replace("Enf.","").strip()
            Tipo_Cobertura = "" 
        elif "Apto." in resto:
            local = "Apartamento"
            Cobertura = resto.replace("Apto.","").strip()
            Tipo_Cobertura = "" 
        elif "Ambulatorial" in resto:
            Tipo_Cobertura = "Ambulatorial"
            Cobertura = resto.replace("Ambulatorial","").strip()
            local = ""

    convert = {
        "Norte/Nordeste":"Regional",
        "Teresina":"Municipal"
    }

    Cobertura = convert.get(Cobertura,Cobertura)
    atendimento=local.strip()

    return pd.Series([plano,atendimento,Tipo_Cobertura,Cobertura])

resultado = principal_susito.apply(trimming,axis=1)
resultado = resultado.rename(columns={
    0: "Plano",
    1: "Acomodacao",
    2: "Tipo_Cobertura",
    3: "Cobertura"
})

resultado["Codigo_Plano"] = principal_susito["Codigo_Plano"]

principal_susito = pd.merge(principal_susito, resultado, on='Codigo_Plano', how='left')

principal_susito["Operadora"] = "Hapvida%"
principal_susito["Porcentagem_Promocao"] = "15%"
principal_susito["Descricao_Promocao"] = "15% de desconto nas 3 primeiras mensalidades"
principal_susito["Promocao_Ativa"] = True
principal_susito["Ativo"] = True
principal_susito["Coparticipacao"] = "Total"
principal_susito["Observacao"] = "Super Simples"
principal_susito["Id"] = [str(uuid.uuid4()) for _ in range(len(principal_susito))]
principal_susito["Descricao_Plano"] = "" 

principal_susito["Codigo_Plano"] = principal_susito["Codigo_Plano"].astype(str)
p["Codigo_Plano"] = p["Codigo_Plano"].astype(str)

colunas_p = ["Codigo_Plano", "Tipo_Rede", "Tipo_Contratacao", "Tipo_Rede_Nacional", "Registro_ANS", "Min_Beneficiarios", "Max_Beneficiarios"]
p_filtrada = p[colunas_p].drop_duplicates(subset=["Codigo_Plano"], keep="first")
principal_susito = principal_susito.merge(p_filtrada, on="Codigo_Plano", how="left")
nao_existe = principal_susito["Registro_ANS"].isna()

principal_susito.loc[nao_existe, "Tipo_Cobertura"] = "Ambulatorial + Hospitalar com Obstetrícia"
principal_susito.loc[nao_existe, "Min_Beneficiarios"] = 1
principal_susito.loc[nao_existe, "Tipo_Contratacao"] = "PME"
principal_susito = principal_susito.fillna("")

limpar_int = lambda val: str(int(float(val))) if (val != "" and pd.notna(val)) else ""
principal_susito["Min_Beneficiarios"] = principal_susito["Min_Beneficiarios"].apply(limpar_int)
principal_susito["Max_Beneficiarios"] = principal_susito["Max_Beneficiarios"].apply(limpar_int)
def principal_incopar(principal_susito):
    return principal_susito[[
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

# #&=======================================================================================================================================
pfp_normal.insert(0, "Faixa_Etaria", faixa.values)
pfp_normal.columns = ["Faixa_Etaria"] + list(principal_susito["Codigo_Plano"].unique())

tabela_b_longa = pd.melt(
    pfp_normal, 
    id_vars=["Faixa_Etaria"], 
    var_name="Codigo_Plano", 
    value_name="Valor"
)
tabela_b_longa["Codigo_Plano"] = tabela_b_longa["Codigo_Plano"].astype(str)

tabela_susito = pd.merge(
    principal_susito[["Id", "Codigo_Plano"]],tabela_b_longa,on="Codigo_Plano",how="inner")

tabela_susito[['Idade_Min', 'Idade_Max']] = tabela_susito['Faixa_Etaria'].str.extract(r'(\d+)\D*(\d*)')
tabela_susito.loc[tabela_susito['Idade_Max'] == '', 'Idade_Max'] = '120'
def tabela_susito();
    return tabela_susito[["Id", "Idade_Min", "Idade_Max", "Valor"]]