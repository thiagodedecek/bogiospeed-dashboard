import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="BogioSpeed Management Portal", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: #012e67 !important; }
    
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: left;
        border-left: 5px solid #ccc;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-income { border-left-color: #28a745; }
    .card-expense { border-left-color: #dc3545; }
    .card-profit { border-left-color: #007bff; }
    
    .metric-card h2 { margin: 0; font-size: 28px; }
    .metric-card p { margin: 0; font-size: 14px; color: #6c757d !important; font-weight: bold; }

    .stButton>button {
        background-color: #f1c40f;
        color: #012e67;
        font-weight: bold;
        border-radius: 8px;
    }
    input, select, textarea, div[data-baseweb="select"] > div { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO ---
def connect():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account_dashboard"] 
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Other / Altro"]
lista_fornecedores = ["None / Nessuno", "NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Other / Altro"]

sheet = connect()
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- 3. HEADER & DASHBOARD ---
st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=350)
st.title("Invoices Control & Management")

if not df.empty:
    total_in = pd.to_numeric(df['SOLD'], errors='coerce').sum()
    total_out = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER
