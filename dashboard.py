import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. CONFIGURAÇÃO VISUAL (RESOLVE O TÍTULO INVISÍVEL) ---
st.set_page_config(page_title="BogioSpeed Management", layout="wide")

st.markdown("""
    <style>
    /* Resolve image_4c30e1.png: Força textos para Azul Escuro no fundo branco */
    .stApp { background-color: white; }
    h1, h2, h3, label, p, span { color: #012e67 !important; }
    
    /* Campos de entrada Brancos com borda nítida */
    div[data-baseweb="input"] > div, .stNumberInput input, .stTextInput input {
        background-color: white !important;
        color: #012e67 !important;
        border: 1px solid #012e67 !important;
    }
    
    /* Botão Salvar Amarelo */
    .stButton>button { 
        background-color: #f1c40f !important; 
        color: #012e67 !important; 
        font-weight: bold; border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO (RESOLVE O INCORRECT PADDING) ---
def connect():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # O Streamlit converte automaticamente o formato da image_4bc47e para dicionário
    creds_dict = st.secrets["gcp_service_account_dashboard"] 
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    # Nome validado pela image_4b5bf8.png
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

try:
    sheet = connect()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # Filtra linhas vazias para evitar pular 1000 linhas (image_165f85.png)
    if not df.empty:
        df = df[df['JOB Nº'].astype(str).str.strip() != ""]
except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    df = pd.DataFrame()

# --- 3. HEADER & MÉTRICAS ---
st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=300)
st.title("Invoices Control & Management")

if not df.empty:
    # Usando PROFIT (image_af7e3d.png) e removendo o erro de PRIFIT (image_af79dd.png)
    total_in = pd.to_numeric(df['SOLD'], errors='coerce').sum()
    total_out = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER II'], errors='coerce').sum()
    net_balance = pd.to_numeric(df['PROFIT'], errors='coerce').sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Income", f"€ {total_in:,.2f}")
    m2.metric("Total Expenses", f"€ {total_out:,.2f}")
    m3.metric("Net Balance", f"€ {net_balance:,.2f}")

# --- 4. FORMULÁRIO (CHAVE ÚNICA PARA EVITAR image_240a2c.png) ---
with st.expander("➕ ADD NEW INVOICE", expanded=True):
    with st.form(key="form_bogiospeed_final", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_job = st.text_input("JOB Nº *")
            f_date = st.date_input("Date", date.today())
            f_client = st.text_input("Customer Name *")
        with c2:
            f_sold = st.number_input("Sold Value (€)", min_value=0.0, format="%.2f")
            f_plate = st.text_input("Plate Nº / Targa")
            f_kind = st.text_input("Service", value="Rodoviário")
        with c3:
            f_closed = st.date_input("Closing Date", date.today())
            f_pay1 = st.number_input("Buyer I Cost (€)", min_value=0.0, format="%.2f")
            f_pay2 = st.number_input("Buyer II Cost (€)", min_value=0.0, format="%.2f")

        if st.form_submit_button("SAVE TO GOOGLE SHEETS"):
            if f_job and f_client:
                f_profit = f_sold - f_pay1 - f_pay2
                # Ordem exata da planilha (image_af7e3d.png)
                new_row = [f_job, str(f_date), f_client, f_kind, "", "", f_sold, f_pay1, f_pay2, f_profit, str(f_closed), "", "", f_plate]
                
                # Inteligência para não pular as 1000 linhas formatadas
                all_col_a = sheet.col_values(1)
                next_row = len([x for x in all_col_a if x.strip() != ""]) + 1
                
                sheet.insert_row(new_row, index=next_row)
                st.success(f"Job {f_job} salvo com sucesso!")
                st.rerun()
            else:
                st.warning("JOB Nº e Customer são obrigatórios.")

# --- 5. TABELA DE DADOS ---
if not df.empty:
    st.markdown("---")
    st.subheader("Last Registered Invoices")
    st.dataframe(df.tail(10), use_container_width=True)
