import os
import uuid
import sys
import pandas as pd
pasta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pasta_raiz not in sys.path:
    sys.path.append(pasta_raiz)
from scanner import incoto_scan

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


p,pfp = incoto_scan()

pfp_planos=pfp.iloc[0,1:6].copy()
pfp_normal = pfp.iloc[1:11,0:6].copy()

nomes=pfp.columns[1:6].copy()
colunas=pfp.iloc[0,1:6].copy()

principal_incoto= pd.DataFrame({
    "Codigo_Plano":nomes,
    "Nome": colunas 
})
principal_incoto = principal_incoto.reset_index(drop=True)

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

    convert = {
        "Enf.":"Enfermaria",
        "Apto.":"Apartamento"
    }

    local_limpo = local.strip()
    atendimento=convert.get(local_limpo,local_limpo)

    return pd.Series([plano,atendimento,Tipo_Cobertura])

resultado = principal_incoto.apply(trimming,axis=1)
resultado = resultado.rename(columns={
    0: "Plano",
    1: "Acomodacao",
    2: "Tipo_Cobertura"
})

resultado["Codigo_Plano"] = principal_incoto["Codigo_Plano"]

principal_incoto = pd.merge(principal_incoto, resultado, on="Codigo_Plano", how="left")

principal_incoto["Operadora"] = f"Hapvida%"
principal_incoto["Porcentagem_Promocao"] = f"15%"
principal_incoto["Descricao_Promocao"] = f"15% de desconto nas 3 primeiras mensalidades"
principal_incoto["Promocao_Ativa"] = True
principal_incoto["Ativo"] = True
principal_incoto["Coparticipacao"] = f"Total"
principal_incoto["Cobertura"] = f"Municipal"
principal_incoto["Observacao"] = ""
principal_incoto["Tipo_Contratacao"] = f"Individual/Familiar"
principal_incoto["Id"] = [str(uuid.uuid4()) for _ in range(len(principal_incoto))]
principal_incoto["Descricao_Plano"] = ""

principal_incoto["Codigo_Plano"] = principal_incoto["Codigo_Plano"].astype(str)
p["Codigo_Plano"] = p["Codigo_Plano"].astype(str)

colunas_p = ["Codigo_Plano", "Tipo_Rede", "Tipo_Rede_Nacional", "Registro_ANS", "Min_Beneficiarios", "Max_Beneficiarios"]
p_filtrada = p[colunas_p].drop_duplicates(subset=["Codigo_Plano"], keep="first")
principal_incoto = principal_incoto.merge(p_filtrada, on="Codigo_Plano", how="left")
nao_existe = principal_incoto["Registro_ANS"].isna()

principal_incoto.loc[nao_existe, "Tipo_Cobertura"] = "Ambulatorial + Hospitalar com Obstetrícia"
principal_incoto.loc[nao_existe, "Min_Beneficiarios"] = 1
principal_incoto = principal_incoto.fillna("")

limpar_int = lambda val: str(int(float(val))) if (val != "" and pd.notna(val)) else ""
principal_incoto["Min_Beneficiarios"] = principal_incoto["Min_Beneficiarios"].apply(limpar_int)
principal_incoto["Max_Beneficiarios"] = principal_incoto["Max_Beneficiarios"].apply(limpar_int)
principal_incoto = principal_incoto[[
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

#&=======================================================================================================================================
pfp_normal.columns = ["Faixa_Etaria"] + list(principal_incoto["Codigo_Plano"].unique())

tabela_merge = pd.melt(
    pfp_normal, 
    id_vars=["Faixa_Etaria"], 
    var_name="Codigo_Plano", 
    value_name="Valor"
)

tabela_merge["Codigo_Plano"] = tabela_merge["Codigo_Plano"].astype(str)

tabela_incoto = pd.merge(
    principal_incoto[["Id", "Codigo_Plano"]],tabela_merge,on="Codigo_Plano",how="inner")

tabela_incoto[["Idade_Min", "Idade_Max"]] = tabela_incoto["Faixa_Etaria"].str.extract(r"(\d+)\D*(\d*)")
tabela_incoto.loc[tabela_incoto["Idade_Max"] == "", "Idade_Max"] = "120"
tabela_incoto = tabela_incoto[["Id", "Idade_Min", "Idade_Max", "Valor"]]
tabela_incoto = tabela_incoto[["Id", "Idade_Min", "Idade_Max", "Valor"]]