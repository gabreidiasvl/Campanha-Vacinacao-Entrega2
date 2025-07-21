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
VERMELHO_BOTAO = "#dc3545"

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

nome = pn.widgets.TextInput(name="Nome")
cpf = pn.widgets.TextInput(name="CPF")
email = pn.widgets.TextInput(name="E-mail")
nascimento = pn.widgets.DatePicker(name="Nascimento")
endereco = pn.widgets.TextInput(name="Endereço")
telefone = pn.widgets.TextInput(name="Telefone")
cartao_sus = pn.widgets.TextInput(name="Cartão do SUS")

btn_inserir = pn.widgets.Button(name="Inserir Paciente", button_type='success', styles={
    'background-color': VERDE_BOTAO, 'color': 'white'
})
btn_excluir = pn.widgets.Button(name="Excluir Paciente", button_type='danger', styles={
    'background-color': VERMELHO_BOTAO, 'color': 'white'
})
btn_salvar_edicoes = pn.widgets.Button(name="Salvar Alterações", button_type="primary")

busca = pn.widgets.TextInput(name="Buscar por nome ou CPF")
tabela = pn.widgets.Tabulator(
    pagination='remote',
    page_size=10,
    layout='fit_data',
    theme='site',
    configuration={
        "columns": [
            {"title": "Nome", "field": "nome", "editor": "input"},
            {"title": "E-mail", "field": "email", "editor": "input"},
            {"title": "Nascimento", "field": "data_nascimento", "editor": "input"},
            {"title": "Endereço", "field": "endereco", "editor": "input"},
            {"title": "Telefone", "field": "telefone", "editor": "input"},
            {"title": "Cartão SUS", "field": "cartao_sus", "editor": "input"},
        ]
    }
)

def carregar_pacientes(filtro=""):
    query = """
        SELECT p.cpf, p.nome, p.email, p.data_nascimento, p.endereco, p.telefone, pa.cartao_sus
        FROM pessoa p
        JOIN paciente pa ON p.cpf = pa.cpf
    """
    if filtro:
        query += " WHERE p.nome ILIKE %s OR p.cpf ILIKE %s"
        df = pd.read_sql_query(query, engine, params=(f'%{filtro}%', f'%{filtro}%'))
    else:
        df = pd.read_sql_query(query, engine)
    return df

def atualizar_tabela(event=None):
    filtro = busca.value.strip()
    df = carregar_pacientes(filtro)
    tabela.value = df

def on_inserir(event=None):
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO paciente (cpf, nome, email, data_nascimento, endereco, telefone, cartao_sus)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cpf.value, nome.value, email.value, nascimento.value, endereco.value, telefone.value, cartao_sus.value))
        con.commit()
        atualizar_tabela()
        pn.state.notifications.success("Paciente inserido com sucesso!")
    except Exception as e:
        con.rollback()
        pn.state.notifications.error(f"Erro ao inserir: {str(e)}")

def on_excluir(event=None):
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM paciente WHERE cpf = %s", (cpf.value,))
        con.commit()
        atualizar_tabela()
        pn.state.notifications.success("Paciente removido com sucesso!")
    except Exception as e:
        con.rollback()
        pn.state.notifications.error(f"Erro ao excluir: {str(e)}")

def salvar_edicoes(event=None):
    df = tabela.value
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            try:
                cursor = con.cursor()
                cursor.execute("""
                    UPDATE pessoa
                    SET nome = %s, email = %s, data_nascimento = %s,
                        endereco = %s, telefone = %s
                    WHERE cpf = %s
                """, (row['nome'], row['email'], row['data_nascimento'],
                      row['endereco'], row['telefone'], row['cpf']))

                cursor.execute("""
                    UPDATE paciente
                    SET cartao_sus = %s
                    WHERE cpf = %s
                """, (row['cartao_sus'], row['cpf']))

                con.commit()
            except Exception as e:
                con.rollback()
                pn.state.notifications.error(f"Erro ao salvar: {str(e)}")
        pn.state.notifications.success("Alterações salvas com sucesso!")

btn_inserir.on_click(on_inserir)
btn_excluir.on_click(on_excluir)
btn_salvar_edicoes.on_click(salvar_edicoes)
busca.param.watch(lambda e: atualizar_tabela(), 'value')

logo1 = pn.pane.Image("https://portalhospitaisbrasil.com.br/wp-content/uploads/2021/03/unnamed-1.jpg", width=200)
logo2 = pn.pane.Image("https://cidadao.saude.al.gov.br/wp-content/uploads/2016/09/logo_sus.png", width=200)

formulario = pn.Column(
    pn.Row(logo1, logo2, sizing_mode='stretch_width'),
    pn.pane.Markdown("## Cadastro de Pacientes"),
    nome, cpf, email, nascimento, endereco, telefone, cartao_sus,
    pn.Row(btn_inserir, btn_excluir),
    styles={
        'background': FUNDO_CLARO,
        'border': '1px solid #ccc',
        'padding': '15px',
        'border-radius': '10px'
    },
    width=450,
    align='center'
)

tabela_pacientes = pn.Column(
    pn.pane.Markdown("## Lista de Pacientes"),
    busca,
    tabela,
    btn_salvar_edicoes,
    sizing_mode="stretch_width"
)

layout = pn.Row(
    pn.Spacer(width=20),
    pn.Column(formulario, width=420),
    pn.layout.HSpacer(),
    tabela_pacientes,
    pn.Spacer(width=20)
)

atualizar_tabela()
layout.servable()
