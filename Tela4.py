import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import panel as pn

pn.extension('tabulator', notifications=True)

AZUL_SUS = "#0072c6"
FUNDO_CLARO = "#f1f1f1"
pn.config.raw_css.append(f"""
h1, h2, h3 {{
    color: {AZUL_SUS};
    font-family: Arial, sans-serif;
}}
.pn-widget-button {{
    font-weight: bold;
}}
""")

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

con = pg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')

filtro_vacina = pn.widgets.TextInput(name="Buscar Vacina ou Fabricante")
tabela_vacinas = pn.widgets.Tabulator(pagination='remote', page_size=10, height=500, sizing_mode='stretch_both', theme='site')

def carregar_vacinas(filtro=""):
    query = """
        SELECT 
            v.id,
            v.nome,
            v.fabricante,
            v.numero_doses,
            e.lote,
            e.validade,
            e.quantidade,
            u.nome AS unidade
        FROM vacina v
        JOIN estoque_vacinas e ON e.vacina_id = v.id
        JOIN unidade_saude u ON u.id = e.unidade_id
    """
    params = ()
    if filtro:
        query += " WHERE v.nome ILIKE %s OR v.fabricante ILIKE %s"
        params = (f'%{filtro}%', f'%{filtro}%')

    return pd.read_sql_query(query, engine, params=params)

def atualizar_vacinas(event=None):
    filtro = filtro_vacina.value.strip()
    df = carregar_vacinas(filtro)
    tabela_vacinas.value = df

filtro_vacina.param.watch(lambda e: atualizar_vacinas(), 'value')

logo1 = pn.pane.Image("https://portalhospitaisbrasil.com.br/wp-content/uploads/2021/03/unnamed-1.jpg", width=200)
logo2 = pn.pane.Image("https://cidadao.saude.al.gov.br/wp-content/uploads/2016/09/logo_sus.png", width=200)

cabecalho = pn.Row(
    logo1,
    pn.Spacer(width=20),
    logo2,
    sizing_mode="stretch_width"
)

painel_vacinas = pn.Column(
    cabecalho,
    pn.pane.Markdown("## Visualização de Vacinas"),
    filtro_vacina,
    tabela_vacinas,
    sizing_mode="stretch_both",
    styles={
        'background': FUNDO_CLARO,
        'padding': '20px',
        'border-radius': '10px'
    }
)

atualizar_vacinas()

painel_vacinas.servable()
