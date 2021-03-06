-- drop table licitacoes;

create table licitacoes (
    identificacao varchar(40) primary key,
    tipo varchar(20),
    comprador varchar(150),
    endereco varchar(150),
    cidade varchar(40),
    uf char(2),
    telefone varchar(20),
    email varchar(180),
    site varchar(180),

    codigo varchar(20),
    codigo_uasg varchar(6),
    modalidade varchar(30),
    objeto text,
    segmento text,

    data_entrega datetime,
    data_abertura datetime,
    termino_proposta datetime,
    cotacao_fim datetime,

    edital varchar(80),
    arquivo_edital varchar(80),

    valor_estimado numeric(15, 2),

    informacoes varchar(150),

    FULLTEXT(objeto)
) engine=MyISAM;
