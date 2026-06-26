from decimal import Decimal
import uuid

class Planos:
    def __init__(self,
        nome:str,
        registro_ans:str,
        codigo_plano:int,
        coparticipacao:str,
        acomodacao:str,
        tipo_contratacao:str,
        cobertura:str,
        tipo_cobertura:str,
        tipo_rede:str,
        tipo_rede_nacional:str,
        observacao:str,
        min_beneficiarios:int,
        max_beneficiarios:int,
        descricao_plano:str
    ):
        self.id = uuid.uuid4()
        self.operadora = "Hapvida"
        self.nome = nome
        self.registro_ans = registro_ans
        self.codigo_plano = codigo_plano
        self.coparticipacao = coparticipacao
        self.acomodacao = acomodacao
        self.tipo_contratacao = tipo_contratacao
        self.cobertura = cobertura
        self.tipo_cobertura = tipo_cobertura
        self.tipo_rede = tipo_rede
        self.tipo_rede_nacional = tipo_rede_nacional
        self.observacao = observacao
        self.min_beneficiarios = min_beneficiarios
        self.max_beneficiarios = max_beneficiarios
        self.ativo = True
        self.descricao_plano = descricao_plano
        self.promocao_ativa = True
        self.porcentagem_promocao = 15
        self.descricao_promocao = f"15% de desconto nas 3 primeiras mensalidades."


class Planos_faixas_preco:
    def __init__(self,
        plano_id:str,
        idade_min:int,
        idade_max:int,
        valor:Decimal
    ):
        self.plano_id = plano_id
        self.idade_min = idade_min
        self.idade_max = idade_max
        self.valor = valor