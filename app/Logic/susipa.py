import os
import uuid
import sys
import pandas as pd
pasta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pasta_raiz not in sys.path:
    sys.path.append(pasta_raiz)
from scanner import susipa_scan

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

p,pfp = susipa_scan()

faixa = pfp.iloc[1:11,0].copy()
pfp_planos=pfp.iloc[0,2:6]
pfp_normal = pfp.iloc[1:11,2:6].copy()

nomes=pfp.columns[2:6]
colunas=pfp.iloc[0,2:6]

principal_susipa= pd.DataFrame({
    "Codigo_Plano":nomes,
    "Nome": colunas 
})

principal_susipa = principal_susipa.reset_index(drop=True)

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

resultado = principal_susipa.apply(trimming,axis=1)
resultado = resultado.rename(columns={
    0: "Plano",
    1: "Acomodacao",
    2: "Tipo_Cobertura",
    3: "Cobertura"
})

resultado["Codigo_Plano"] = principal_susipa["Codigo_Plano"]

principal_susipa = pd.merge(principal_susipa, resultado, on="Codigo_Plano", how="left")

principal_susipa["Operadora"] = "Hapvida%"
principal_susipa["Porcentagem_Promocao"] = "15%"
principal_susipa["Descricao_Promocao"] = "15% de desconto nas 3 primeiras mensalidades"
principal_susipa["Promocao_Ativa"] = True
principal_susipa["Ativo"] = True
principal_susipa["Coparticipacao"] = "Parcial"
principal_susipa["Observacao"] = "Super Simples"
principal_susipa["Id"] = [str(uuid.uuid4()) for _ in range(len(principal_susipa))]
principal_susipa["Descricao_Plano"] = "" 

principal_susipa["Codigo_Plano"] = principal_susipa["Codigo_Plano"].astype(str)
p["Codigo_Plano"] = p["Codigo_Plano"].astype(str)

colunas_p = ["Codigo_Plano", "Tipo_Rede", "Tipo_Contratacao", "Tipo_Rede_Nacional", "Registro_ANS", "Min_Beneficiarios", "Max_Beneficiarios"]
p_filtrada = p[colunas_p].drop_duplicates(subset=["Codigo_Plano"], keep="first")
principal_susipa = principal_susipa.merge(p_filtrada, on="Codigo_Plano", how="left")
nao_existe = principal_susipa["Registro_ANS"].isna()

principal_susipa.loc[nao_existe, "Tipo_Cobertura"] = "Ambulatorial + Hospitalar com Obstetrícia"
principal_susipa.loc[nao_existe, "Min_Beneficiarios"] = 1
principal_susipa.loc[nao_existe, "Tipo_Contratacao"] = "PME"
principal_susipa = principal_susipa.fillna("")

limpar_int = lambda val: str(int(float(val))) if (val != "" and pd.notna(val)) else ""
principal_susipa["Min_Beneficiarios"] = principal_susipa["Min_Beneficiarios"].apply(limpar_int)
principal_susipa["Max_Beneficiarios"] = principal_susipa["Max_Beneficiarios"].apply(limpar_int)
principal_susipa = principal_susipa[[
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
pfp_normal.columns = ["Faixa_Etaria"] + list(principal_susipa["Codigo_Plano"].unique())

tabela_b_longa = pd.melt(
    pfp_normal, 
    id_vars=["Faixa_Etaria"], 
    var_name="Codigo_Plano", 
    value_name="Valor"
)
tabela_b_longa["Codigo_Plano"] = tabela_b_longa["Codigo_Plano"].astype(str)

tabela_susipa = pd.merge(
    principal_susipa[["Id", "Codigo_Plano"]],tabela_b_longa,on="Codigo_Plano",how="inner")

tabela_susipa[["Idade_Min", "Idade_Max"]] = tabela_susipa["Faixa_Etaria"].str.extract(r"(\d+)\D*(\d*)")
tabela_susipa.loc[tabela_susipa["Idade_Max"] == "", "Idade_Max"] = "120"
tabela_susipa = tabela_susipa[["Id", "Idade_Min", "Idade_Max", "Valor"]]