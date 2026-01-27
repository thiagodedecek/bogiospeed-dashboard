import streamlit as st
import pandas as pd
from gspread_pandas import Spread

# 1. Configuração e Layout Visual (Baseado na sua vitória de design)
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    
    /* Estilo dos Cards */
    div[data-testid="column"] div[data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    /* Cores das Bordas e Números */
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] { border-left: 8px solid #28a745 !important; }
    div[data-testid="column"]:nth-of-type(1) [data-testid="stMetricValue"] > div { color: #28a745 !important; }
    
    div[data-testid="column"]:nth-of-type(2) div[data-testid="column"] div[data-testid="stMetric"] { border-left: 8px solid #dc3545 !important; }
    div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricValue"] > div { color: #dc3545 !important; }
    
    div[data-testid="column"]:nth-of-type(3) div[data-testid="column"] div[data-testid="stMetric"] { border-left: 8px solid #6c5ce7 !important; }
    div[data-testid="column"]:nth-of-type(3) [data-testid="stMetricValue"] > div { color: #6c5ce7 !important; }

    h1, h2, h3, p { color: #1e3d59 !important; }
    
    /* Botão Salvar Amarelo (Conforme sua imagem) */
    div.stButton > button {
        background-color: #ffc107 !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com Google Sheets
@st.cache_resource
def load_data():
    try:
        # Puxa as credenciais dos Secrets (TOML)
        creds = st.secrets["gcp_service_account"]
        spread = Spread('Gestao_BogioSpeed_v2', config=creds)
        df = spread.sheet_to_df(index=None)
        return spread, df
    except Exception as e:
        st.error(f"Erro ao conectar na planilha: {e}")
        return None, pd.DataFrame()

spread, df_real = load_data()

# --- CABEÇALHO ---
try:
    st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=200)

except:
    st.header("🚚 BOGIOSPEED SYSTEM")

st.title("Invoices Control & Management")

# --- FORMULÁRIO DE INSERÇÃO (Baseado na sua imagem image_3f8d7d.png) ---
with st.expander("➕ ADD NEW INVOICE", expanded=False):
    with st.form("invoice_form"):
        c1, c2 = st.columns(2)
        with c1:
            job_no = st.text_input("JOB Nº")
            customer = st.text_input("Customer")
            sold_val = st.number_input("Sold Value (€)", min_value=0.0)
        with c2:
            cost1 = st.number_input("Cost I (€)", min_value=0.0)
            cost2 = st.number_input("Cost II (€)", min_value=0.0)
            plate = st.text_input("Plate Nº")
        
        if st.form_submit_button("SAVE DATA"):
            # Envia para a planilha
            nova_linha = [[job_no, customer, sold_val, cost1, cost2, plate]]
            spread.df_to_sheet(pd.DataFrame(nova_linha), index=False, header=False, start='A' + str(len(df_real) + 2))
            st.success("Dados salvos com sucesso!")
            st.rerun()

st.divider()

# --- PAINEL DE SOMATÓRIO ---
st.subheader("Painel de Somatório")
# Conversão segura para números
if not df_real.empty:
    total_in = pd.to_numeric(df_real.iloc[:, 2], errors='coerce').sum() # Sold Value
    total_out = pd.to_numeric(df_real.iloc[:, 3], errors='coerce').sum() + pd.to_numeric(df_real.iloc[:, 4], errors='coerce').sum()
    saldo = total_in - total_out
else:
    total_in, total_out, saldo = 0, 0, 0

col1, col2, col3 = st.columns(3)
with col1: st.metric("Total de Entradas", f"€ {total_in:,.2f}")
with col2: st.metric("Total de Saídas", f"€ {total_out:,.2f}")
with col3: st.metric("Saldo Líquido", f"€ {saldo:,.2f}")

st.divider()

# --- TABELA DE DADOS ---
st.subheader("Faturas Registradas")
if not df_real.empty:
    st.dataframe(df_real, use_container_width=True, hide_index=True)
else:
    st.info("The spreadsheet is currently empty.")
