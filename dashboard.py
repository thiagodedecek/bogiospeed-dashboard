import streamlit as st
import pandas as pd
from gspread_pandas import Spread
import os

# 1. Configuração Visual
st.set_page_config(page_title="BogioSpeed Management", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #f8f9fa !important; }

/* Cards */
div[data-testid="column"] div[data-testid="stMetric"] {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
}

/* Cores dos Cards */
div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
    border-left: 8px solid #28a745 !important;
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
    border-left: 8px solid #dc3545 !important;
}
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
    border-left: 8px solid #6c5ce7 !important;
}
div[data-testid="column"] [data-testid="stMetricValue"] > div {
    font-size: 24px !important;
    font-weight: bold !important;
}

/* Botão Salvar */
div.stButton > button {
    background-color: #ffc107 !important;
    color: #000 !important;
    font-weight: bold !important;
    border: none !important;
}

/* Títulos */
h1, h2, h3, p {
    color: #1e3d59 !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Conexão com Google Sheets
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

# 3. Cabeçalho
logo_path = "BOGIO-SPEED-Logo-1-1536x217.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
else:
    st.header("🚚 BOGIOSPEED SYSTEM")

st.title("Controle de Faturas")

# 4. Formulário de Inserção
with st.expander("➕ Adicionar Fatura", expanded=False):
    with st.form("invoice_form"):
        c1, c2 = st.columns(2)
        with c1:
            job_no = st.text_input("Nº Nota")
            customer = st.text_input("Cliente")
            sold_val = st.number_input("Entrada (R$)", min_value=0.0)
        with c2:
            cost1 = st.number_input("Saída F1 (R$)", min_value=0.0)
            cost2 = st.number_input("Saída F2 (R$)", min_value=0.0)
            plate = st.text_input("Placa")

        if st.form_submit_button("Salvar Fatura"):
            nova_linha = [[job_no, customer, sold_val, cost1, cost2, plate]]
            spread.df_to_sheet(pd.DataFrame(nova_linha), index=False, header=False, start='A' + str(len(df_real) + 2))
            st.success("✅ Fatura salva com sucesso!")
            st.rerun()

st.divider()

# 5. Painel de Somatório
st.subheader("📊 Painel de Somatório")
if not df_real.empty:
    total_in = pd.to_numeric(df_real.iloc[:, 2], errors='coerce').sum()
    total_out = pd.to_numeric(df_real.iloc[:, 3], errors='coerce').sum() + pd.to_numeric(df_real.iloc[:, 4], errors='coerce').sum()
    saldo = total_in - total_out
else:
    total_in, total_out, saldo = 0, 0, 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Entradas", f"R$ {total_in:,.2f}")
col2.metric("Total de Saídas", f"R$ {total_out:,.2f}")
col3.metric("Saldo Líquido", f"R$ {saldo:,.2f}")

st.divider()

# 6. Tabela de Faturas
st.subheader("📁 Faturas Registradas")
if not df_real.empty:
    df_real.columns = ["Nº Nota", "Cliente", "Entrada (R$)", "Saída F1 (R$)", "Saída F2 (R$)", "Placa"]
    st.dataframe(df_real, use_container_width=True, hide_index=True)
else:
    st.info("📭 Nenhuma fatura registrada ainda.")
