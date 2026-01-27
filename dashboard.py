import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. CONFIGURAÇÃO VISUAL (CAMPOS BRANCOS) ---
st.set_page_config(page_title="BogioSpeed Management", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Forçar campos de entrada para fundo branco e texto escuro */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: white !important;
        color: #012e67 !important;
        border-radius: 8px !important;
    }
    
    /* Estilização das Métricas */
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        text-align: left; border-left: 5px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-income { border-left-color: #28a745; }
    .card-expense { border-left-color: #dc3545; }
    .card-profit { border-left-color: #007bff; }
    .metric-card h2 { margin: 0; font-size: 28px; color: #012e67; }
    .metric-card p { margin: 0; font-size: 14px; color: #6c757d !important; font-weight: bold; }
    
    /* Botão de salvar amarelo */
    .stButton>button { 
        background-color: #f1c40f; color: #012e67; 
        font-weight: bold; border-radius: 8px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO ---
def connect():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account_dashboard"] 
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

sheet = connect()

try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # Filtro para garantir que não leremos as linhas 2-1000 se estiverem vazias
    if not df.empty:
        df = df[df['JOB Nº'].astype(str).str.strip() != ""]
except:
    df = pd.DataFrame(columns=['JOB Nº', 'DATE', 'CUSTOMER', 'KIND', 'SUPPLIER', 'SUPPLIER II', 'SOLD', 'BUYER', 'BUYER II', 'PROFIT', 'CLOSED', 'INV I', 'INV II', 'PLATE Nº'])

# --- 3. DASHBOARD ---
st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=300)
st.title("Invoices Control & Management")

if not df.empty:
    # Usando 'PROFIT' conforme sua planilha
    total_in = pd.to_numeric(df['SOLD'], errors='coerce').sum()
    total_out = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER II'], errors='coerce').sum()
    net_balance = pd.to_numeric(df['PROFIT'], errors='coerce').sum()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card card-income"><p>Total Income</p><h2>€ {total_in:,.2f}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card card-expense"><p>Total Expenses</p><h2>€ {total_out:,.2f}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card card-profit"><p>Net Balance</p><h2>€ {net_balance:,.2f}</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. FORMULÁRIO DE CADASTRO ---
with st.expander("➕ ADD NEW INVOICE", expanded=True):
    # 'key' alterada para evitar erro de duplicidade
    with st.form(key="form_registro_v3", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_job = st.text_input("JOB Nº *")
            f_date = st.date_input("Date *", date.today())
            f_client = st.text_input("Customer Name *")
        with c2:
            f_sold = st.number_input("Sold Value (€) *", min_value=0.0, format="%.2f")
            f_plate = st.text_input("Plate Nº / Targa")
            f_kind = st.text_input("Kind of Service", value="Stradale")
        with c3:
            f_closed = st.date_input("Closing Date", date.today())
            f_pay1 = st.number_input("Buyer I Cost (€)", min_value=0.0, format="%.2f")
            f_pay2 = st.number_input("Buyer II Cost (€)", min_value=0.0, format="%.2f")

        if st.form_submit_button("SAVE DATA"):
            if f_job and f_client:
                f_profit = f_sold - f_pay1 - f_pay2
                # A ordem das colunas segue a imagem image_af7e3d.png
                new_row = [f_job, str(f_date), f_client, f_kind, "", "", f_sold, f_pay1, f_pay2, f_profit, str(f_closed), "", "", f_plate]
                
                # Localiza a próxima linha real (ponto 3 discutido)
                all_col_a = sheet.col_values(1)
                next_row = len([x for x in all_col_a if x.strip() != ""]) + 1
                
                sheet.insert_row(new_row, index=next_row)
                st.success(f"Job {f_job} salvo!")
                st.rerun()
            else:
                st.error("Preencha JOB Nº e Customer.")

# --- 5. HISTÓRICO ---
st.markdown("---")
if not df.empty:
    st.subheader("Registered Invoices")
    # Exibe os dados reais ignorando as linhas 2-1000 vazias
    st.dataframe(df[['JOB Nº', 'DATE', 'CUSTOMER', 'SOLD', 'PROFIT', 'PLATE Nº']].tail(10), use_container_width=True)
