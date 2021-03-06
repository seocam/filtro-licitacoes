from peewee import *
from peewee import RawQuery

from settings import database


def formata_data(data):
    dia, mes, ano = data.split('/')
    return "%s-%s-%s" % (ano, mes, dia)

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Cidade(BaseModel):
    nome = CharField(db_column='cidade')

def carrega_cidades():
    return RawQuery(Cidade, 'select distinct cidade from licitacoes order by cidade')

class Estado(BaseModel):
    uf = CharField(db_column='uf')

def carrega_estados():
    return RawQuery(Estado, 'select distinct uf from licitacoes where uf<>"" order by 1')

class Modalidade(BaseModel):
    descricao = CharField(db_column='modalidade')

def carrega_modalidades():
    return RawQuery(Modalidade, 'select distinct modalidade from licitacoes')

class Licitacao(BaseModel):

    class Meta:
        db_table = 'licitacoes'

    identificacao        = CharField(primary_key = True)
    cidade               = CharField(null = True)
    codigo               = CharField(null = True)
    comprador            = CharField(null = True)
    email                = CharField(null = True)
    endereco             = CharField(null = True)
    modalidade           = CharField(null = True)
    objeto               = TextField(null = True)
    edital               = CharField(max_length=80)
    segmento             = TextField(null = True)
    site                 = CharField(null = True)
    telefone             = CharField(null = True)
    tipo                 = CharField(null = True)
    uf                   = CharField(null = True)
    data_entrega         = DateTimeField(null = True)
    data_abertura        = DateTimeField(null = True)
    cotacao_fim          = DateTimeField(null = True)
    termino_proposta     = DateTimeField(null = True)
    informacoes          = CharField(null = True)
    arquivo_edital       = CharField(max_length=80)
    valor_estimado       = DecimalField()
    codigo_uasg          = CharField(null = True)

    @staticmethod
    def filtrar_por(**kwargs):
        select = Licitacao.select()
        if kwargs['cidade']!='todas':
            select = select.where(Licitacao.cidade==kwargs['cidade'])
        if kwargs['estado']!='todos':
            select = select.where(Licitacao.uf==kwargs['estado'])
        if kwargs['modalidade']!='todas':
            select = select.where(Licitacao.modalidade==kwargs['modalidade'])
        if kwargs['data_entrega']:
            data1 = formata_data(kwargs['data_entrega'])+' 00:00:00'
            data2 = formata_data(kwargs['data_entrega'])+' 23:59:59'
            select = select.where(Licitacao.data_entrega.between(data1, data2))
        if kwargs['data_abertura']:
            data1 = formata_data(kwargs['data_abertura'])+' 00:00:00'
            data2 = formata_data(kwargs['data_abertura'])+' 23:59:59'
            select = select.where(Licitacao.data_abertura.between(data1, data2))
        if kwargs['termino_proposta'] and kwargs['cotacao_fim']:
            select = select.where(
            (Licitacao.termino_proposta>=formata_data(kwargs['termino_proposta'])+' 00:00:00') &
            (Licitacao.cotacao_fim<=formata_data(kwargs['cotacao_fim'])+' 23:59:59'))
        if kwargs['objeto']:
            select = select.where(SQL("match (objeto) against ('{0}')".format(kwargs['objeto'])))

        select = select.limit(30)
        print select
        return select

if __name__ == '__main__':
    database.connect()
    database.create_tables([Cidade, Estado, Licitacao, Modalidade])
