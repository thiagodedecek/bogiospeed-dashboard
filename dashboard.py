import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. ESTILO VISUAL (CAMPOS BRANCOS E TEXTO VISÍVEL) ---
st.set_page_config(page_title="BogioSpeed Management", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3, label, p, span { color: #012e67 !important; }
    div[data-baseweb="input"] > div {
        background-color: white !important;
        border: 1px solid #012e67 !important;
        color: #012e67 !important;
    }
    .stButton>button { 
        background-color: #f1c40f !important; color: #012e67 !important; font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO ---
def connect():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Lê do formato TOML que você tem nos Secrets (image_4bc47e.png)
    creds_dict = st.secrets["gcp_service_account_dashboard"] 
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

try:
    sheet = connect()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        # Filtra linhas vazias (image_165f85.png)
        df = df[df['JOB Nº'].astype(str).str.strip() != ""]
except Exception as e:
    st.error(f"Erro ao conectar: {e}")
    df = pd.DataFrame()

# --- 3. DASHBOARD ---
st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=300)
st.title("Invoices Control & Management")

if not df.empty:
    # Correção do cálculo (SyntaxError da image_15efc2.png resolvido aqui)
    total_in = pd.to_numeric(df['SOLD'], errors='coerce').sum()
    total_out = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER II'], errors='coerce').sum()
    net_profit = pd.to_numeric(df['PROFIT'], errors='coerce').sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income", f"€ {total_in:,.2f}")
    c2.metric("Total Expenses", f"€ {total_out:,.2f}")
    c3.metric("Net Balance", f"€ {net_profit:,.2f}")

# --- 4. FORMULÁRIO ---
with st.expander("➕ ADD NEW INVOICE", expanded=True):
    with st.form(key="form_v5", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            f_job = st.text_input("JOB Nº")
            f_client = st.text_input("Customer")
            f_sold = st.number_input("Sold Value (€)", format="%.2f")
        with col2:
            f_pay1 = st.number_input("Cost I (€)", format="%.2f")
            f_pay2 = st.number_input("Cost II (€)", format="%.2f")
            f_plate = st.text_input("Plate Nº")

        if st.form_submit_button("SAVE DATA"):
            if f_job and f_client:
                f_profit = f_sold - f_pay1 - f_pay2
                # Ordem das colunas conforme image_af7e3d.png
                new_row = [f_job, str(date.today()), f_client, "Stradale", "", "", f_sold, f_pay1, f_pay2, f_profit, str(date.today()), "", "", f_plate]
                
                # Acha a próxima linha real ignorando as 1000 formatadas
                all_ids = sheet.col_values(1)
                next_row = len([x for x in all_ids if x.strip() != ""]) + 1
                
                sheet.insert_row(new_row, index=next_row)
                st.success("Date OK!")
                st.rerun()

# --- 5. TABELA ---
if not df.empty:
    st.markdown("---")
    st.subheader("Recent Records")
    st.dataframe(df.tail(10), use_container_width=True)
