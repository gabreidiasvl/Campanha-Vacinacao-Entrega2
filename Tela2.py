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

try:
    unidades_df = pd.read_sql("SELECT id, nome FROM unidade_saude ORDER BY nome", engine)
    unidades_dict = dict(zip(unidades_df['nome'], unidades_df['id']))
except Exception as e:
    unidades_df = pd.DataFrame()
    unidades_dict = {}
    pn.state.notifications.error(f"Erro ao carregar unidades: {e}")

seletor_unidade = pn.widgets.Select(name="Unidade de Saúde", options=unidades_dict)
tabela_profissionais = pn.widgets.Tabulator(name="Profissionais da Unidade", pagination='remote', page_size=10, theme='site')
tabela_vacinas = pn.widgets.Tabulator(name="Estoque de Vacinas", pagination='remote', page_size=10, theme='site')

def filtrar_por_unidade(event=None):
    if not seletor_unidade.value:
        tabela_profissionais.value = pd.DataFrame()
        tabela_vacinas.value = pd.DataFrame()
        return

    unidade_id = seletor_unidade.value
    try:
        prof_query = """
            SELECT cpf, nome, email, telefone, funcao
            FROM profissional_saude
            WHERE unidade_id = %s
        """
        df_profissionais = pd.read_sql_query(prof_query, engine, params=(unidade_id,))
        tabela_profissionais.value = df_profissionais

        vacina_query = """
            SELECT e.lote, e.validade, e.quantidade, v.nome AS vacina, v.fabricante, v.numero_doses
            FROM estoque_vacinas e
            JOIN vacina v ON v.id = e.vacina_id
            WHERE e.unidade_id = %s
        """
        df_vacinas = pd.read_sql_query(vacina_query, engine, params=(unidade_id,))
        tabela_vacinas.value = df_vacinas

        pn.state.notifications.success("Dados carregados com sucesso.")

    except Exception as e:
        pn.state.notifications.error(f"Erro ao buscar: {e}")

seletor_unidade.param.watch(filtrar_por_unidade, 'value')

logo1 = pn.pane.Image("https://portalhospitaisbrasil.com.br/wp-content/uploads/2021/03/unnamed-1.jpg", width=200)
logo2 = pn.pane.Image("https://cidadao.saude.al.gov.br/wp-content/uploads/2016/09/logo_sus.png", width=200)

layout = pn.Column(
    pn.Row(logo1, logo2, sizing_mode='stretch_width'),
    pn.pane.Markdown("# Consulta de Unidade de Saúde"),
    seletor_unidade,
    pn.pane.Markdown("## Profissionais da Unidade"),
    tabela_profissionais,
    pn.pane.Markdown("## Estoque de Vacinas"),
    tabela_vacinas,
    styles={
        'background': FUNDO_CLARO,
        'border': '1px solid #ccc',
        'padding': '15px',
        'border-radius': '10px'
    },
    width=700,
    align='center'
)

layout.servable()
