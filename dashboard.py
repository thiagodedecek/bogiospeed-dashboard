import streamlit as st
import pandas as pd
from gspread_pandas import Spread
import os

st.set_page_config(page_title="BogioSpeed Management", layout="wide")

# Estilo visual
st.markdown("""
<style>
.stApp { background-color: #f8f9fa !important; }
div[data-testid="column"] div[data-testid="stMetric"] {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
}
div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
    border-left: 8px solid #28a745 !important;
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
    border-left: 8px solid #dc3545 !important;
}
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
    border-left: 8px solid #6c5ce7 !important;
}
div.stButton > button {
    background-color: #ffc107 !important;
    color: #000 !important;
    font-weight: bold !important;
    border: none !important;
}
h1, h2, h3, p { color: #1e3d59 !important; }
</style>
""", unsafe_allow_html=True)

# Conexão com Google Sheets
@st.cache_resource
def load_data():
    try:
        creds = st.secrets["gcp_service_account"]
        spread = Spread('Gestao_BogioSpeed_v2', config=creds)
        df = spread.sheet_to_df(index=None)
        return spread, df
    except Exception as e:
        st.error(f"Erro ao conectar na planilha: {e}")
        return None, pd.DataFrame()

spread, df_real = load_data()

# Cabeçalho
logo_path = "BOGIO-SPEED-Logo-1-1536x217.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
else:
    st.header("🚚 BOGIOSPEED SYSTEM")

st.title("Controle de Faturas")

# Listas suspensas dinâmicas
clientes = sorted(df_real["CUSTOMER"].dropna().unique()) if not df_real.empty else []
fornecedores = sorted(df_real["SUPPLIER"].dropna().unique()) if not df_real.empty else []
compradores = sorted(df_real["BUYER"].dropna().unique()) if not df_real.empty else []

# Formulário completo
with st.expander("➕ Adicionar Fatura", expanded=False):
    with st.form("invoice_form"):
        c1, c2 = st.columns(2)
        with c1:
            job_no = st.text_input("JOB Nº")
            date = st.date_input("DATE")
            customer = st.selectbox("CUSTOMER", options=clientes + ["Outro"], index=0)
            if customer == "Outro":
                customer = st.text_input("Novo CUSTOMER")
            kind = st.text_input("KIND")
            supplier = st.selectbox("SUPPLIER", options=fornecedores + ["Outro"], index=0)
            if supplier == "Outro":
                supplier = st.text_input("Novo SUPPLIER")
            supplier2 = st.text_input("SUPPLIER II")
            sold = st.number_input("SOLD (€)", min_value=0.0)
        with c2:
            buyer = st.selectbox("BUYER", options=compradores + ["Outro"], index=0)
            if buyer == "Outro":
                buyer = st.text_input("Novo BUYER")
            buyer2 = st.text_input("BUYER II")
            closed = st.selectbox("CLOSED", options=["Yes", "No"])
            inv1 = st.text_input("INV I")
            inv2 = st.text_input("INV II")
            plate = st.text_input("PLATE Nº")

        # Cálculo automático do lucro
        profit = sold  # Ajuste futuro: subtrair custos se forem adicionados

        if st.form_submit_button("Salvar Fatura"):
            nova_linha = [[job_no, str(date), customer, kind, supplier, supplier2, sold, buyer, buyer2, profit, closed, inv1, inv2, plate]]
            spread.df_to_sheet(pd.DataFrame(nova_linha), index=False, header=False, start='A' + str(len(df_real) + 2))
            st.success("✅ Fatura salva com sucesso!")
            st.rerun()

st.divider()

# Painel de somatório
st.subheader("📊 Painel de Somatório")
if not df_real.empty:
    total_sold = pd.to_numeric(df_real["SOLD"], errors='coerce').sum()
    total_profit = pd.to_numeric(df_real["PROFIT"], errors='coerce').sum()
else:
    total_sold, total_profit = 0, 0

col1, col2 = st.columns(2)
col1.metric("Total Vendido", f"€ {total_sold:,.2f}")
col2.metric("Lucro Total", f"€ {total_profit:,.2f}")

st.divider()

# Tabela de faturas
st.subheader("📁 Faturas Registradas")
if not df_real.empty:
    st.dataframe(df_real, use_container_width=True, hide_index=True)
else:
    st.info("📭 Nenhuma fatura registrada ainda.")
