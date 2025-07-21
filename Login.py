import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import panel as pn

pn.extension('tabulator', notifications=True)
pn.config.raw_css.append("""
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
""")


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
login_cpf = pn.widgets.TextInput(name="CPF", placeholder="Digite seu CPF")
login_senha = pn.widgets.PasswordInput(name="Senha", placeholder="Digite sua senha")
login_tipo = pn.widgets.RadioButtonGroup(name='Tipo de Login', options=['Paciente', 'Profissional da Saúde'], button_type='primary')

btn_entrar = pn.widgets.Button(name="Entrar", button_type='primary', width=200)
btn_cadastrar = pn.widgets.Button(name="Cadastrar", button_type='default', width=200)
btn_esqueci = pn.widgets.Button(name="Esqueci a Senha", button_type='default', width=200)

mensagem = pn.pane.Markdown("")
def autenticar(event=None):
    cpf = login_cpf.value.strip()
    senha = login_senha.value.strip()
    tipo = login_tipo.value

    if not cpf or not senha:
        mensagem.object = "Por favor, preencha todos os campos."
        return

    try:
        cursor = con.cursor()
        if tipo == "Paciente":
            cursor.execute("SELECT * FROM paciente WHERE cpf = %s AND senha = %s", (cpf, senha))
        else:
            cursor.execute("SELECT * FROM profissional_saude WHERE cpf = %s AND senha = %s", (cpf, senha))

        result = cursor.fetchone()

        if result:
            mensagem.object = f"Bem-vindo, {tipo.lower()}!"
        else:
            mensagem.object = "CPF ou senha incorretos."

    except Exception as e:
        mensagem.object = f"Erro ao autenticar: {str(e)}"

btn_entrar.on_click(autenticar)
logo1 = pn.pane.Image("https://portalhospitaisbrasil.com.br/wp-content/uploads/2021/03/unnamed-1.jpg", width=200)
logo2 = pn.pane.Image("https://cidadao.saude.al.gov.br/wp-content/uploads/2016/09/logo_sus.png", width=200)

login_painel = pn.Column(
    pn.Row(logo1, logo2, sizing_mode='stretch_width'),
    pn.pane.Markdown("## Acesso ao Sistema de Vacinação"),
    login_cpf,
    login_senha,
    login_tipo,
    btn_entrar,
    btn_cadastrar,
    btn_esqueci,
    mensagem,
    styles={
        'background': FUNDO_CLARO,
        'border': '1px solid #ccc',
        'padding': '15px',
        'border-radius': '10px'
    },
    width=450,
    align='center'
)
login_painel.servable()
