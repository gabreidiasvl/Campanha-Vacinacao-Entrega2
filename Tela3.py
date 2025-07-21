import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import panel as pn

pn.extension('tabulator', notifications=True)

AZUL_SUS = "#0072c6"
FUNDO_CLARO = "#f1f1f1"
VERDE_BOTAO = "#28a745"

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

cpf_paciente = pn.widgets.TextInput(name="CPF do Paciente")
unidade_select = pn.widgets.Select(name="Unidade de Saúde")
vacina_select = pn.widgets.Select(name="Vacina")
data_agendamento = pn.widgets.DatePicker(name="Data")
horario_agendamento = pn.widgets.TimePicker(name="Horário")
status_select = pn.widgets.Select(name="Status", options=["pendente", "confirmado", "cancelado"])

btn_agendar = pn.widgets.Button(name="Agendar Vacina", button_type='success', styles={
    'background-color': VERDE_BOTAO,
    'color': 'white'
})

filtro_busca = pn.widgets.TextInput(name="Buscar por CPF ou Nome")
tabela_agendamentos = pn.widgets.Tabulator(pagination='remote', page_size=10,  height=500, theme='site', sizing_mode='stretch_both')

def carregar_opcoes():
    unidades = pd.read_sql_query("SELECT id, nome FROM unidade_saude", engine)
    vacinas = pd.read_sql_query("SELECT id, nome FROM vacina", engine)

    unidade_select.options = {row['nome']: row['id'] for _, row in unidades.iterrows()}
    vacina_select.options = {row['nome']: row['id'] for _, row in vacinas.iterrows()}

def agendar_vacina(event=None):
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO agendamento (data, horario, status, paciente_cpf, unidade_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data_agendamento.value,
            horario_agendamento.value.strftime('%H:%M:%S'),
            status_select.value,
            cpf_paciente.value,
            unidade_select.value
        ))
        con.commit()
        atualizar_agendamentos()
        pn.state.notifications.success("Vacina agendada com sucesso!")
    except Exception as e:
        con.rollback()
        pn.state.notifications.error(f"Erro ao agendar: {e}")

def carregar_agendamentos(filtro=""):
    query = """
        SELECT a.id, a.data, a.horario, a.status, p.nome AS paciente, a.paciente_cpf, u.nome AS unidade
        FROM agendamento a
        JOIN paciente pa ON pa.cpf = a.paciente_cpf
        JOIN pessoa p ON p.cpf = pa.cpf
        JOIN unidade_saude u ON u.id = a.unidade_id
    """
    params = ()
    if filtro:
        query += " WHERE p.nome ILIKE %s OR a.paciente_cpf ILIKE %s"
        params = (f'%{filtro}%', f'%{filtro}%')

    df = pd.read_sql_query(query, engine, params=params)

    if 'horario' in df.columns:
        df['horario'] = df['horario'].apply(lambda x: x.strftime('%H:%M:%S') if pd.notnull(x) else '')

    return df

def atualizar_agendamentos(event=None):
    filtro = filtro_busca.value.strip()
    df = carregar_agendamentos(filtro)
    tabela_agendamentos.value = df

btn_agendar.on_click(agendar_vacina)
filtro_busca.param.watch(lambda e: atualizar_agendamentos(), 'value')

carregar_opcoes()
atualizar_agendamentos()

logo1 = pn.pane.Image("https://portalhospitaisbrasil.com.br/wp-content/uploads/2021/03/unnamed-1.jpg", width=200)
logo2 = pn.pane.Image("https://cidadao.saude.al.gov.br/wp-content/uploads/2016/09/logo_sus.png", width=200)

formulario = pn.Column(
    pn.Row(logo1, logo2, sizing_mode='stretch_width'),
    pn.pane.Markdown("## Agendamento de Vacina"),
    cpf_paciente,
    unidade_select,
    vacina_select,
    data_agendamento,
    horario_agendamento,
    status_select,
    btn_agendar,
    styles={
        'background': FUNDO_CLARO,
        'border': '1px solid #ccc',
        'padding': '15px',
        'border-radius': '10px'
    },
)
formulario = pn.Column(
    pn.Row(logo1, logo2, sizing_mode='stretch_width'),
    pn.pane.Markdown("## Agendamento de Vacina"),
    cpf_paciente,
    unidade_select,
    vacina_select,
    data_agendamento,
    horario_agendamento,
    status_select,
    btn_agendar,
    styles={
        'background': FUNDO_CLARO,
        'border': '1px solid #ccc',
        'padding': '15px',
        'border-radius': '10px'
    },
    width=500,
    align='center'
)


tabela_visualizacao = pn.Column(
    pn.pane.Markdown("## Agendamentos Existentes"),
    filtro_busca,
    tabela_agendamentos,
    sizing_mode="stretch_width"
)

layout = pn.Row(
    pn.Spacer(width=20),
    pn.Column(formulario, width=420),
    pn.layout.HSpacer(),
    tabela_visualizacao,
    pn.Spacer(width=20)
)

layout.servable()
