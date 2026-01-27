import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

# 2. CSS Ultra-específico para forçar as cores (Ignora o tema do sistema)
st.markdown("""
    <style>
    /* Estilização dos Cards */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Forçar cores dos rótulos e valores para não sumirem no tema escuro */
    div[data-testid="stMetricLabel"] > div { color: #666666 !important; font-size: 16px !important; }
    div[data-testid="stMetricValue"] > div { font-size: 32px !important; font-weight: bold !important; }

    /* Bordas e cores dos valores específicos */
    div[data-testid="stMetric"]:nth-of-type(1) { border-left: 6px solid #28a745 !important; }
    div[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricValue"] > div { color: #28a745 !important; }
    
    div[data-testid="stMetric"]:nth-of-type(2) { border-left: 6px solid #dc3545 !important; }
    div[data-testid="stMetric"]:nth-of-type(2) [data-testid="stMetricValue"] > div { color: #dc3545 !important; }
    
    div[data-testid="stMetric"]:nth-of-type(3) { border-left: 6px solid #6c5ce7 !important; }
    div[data-testid="stMetric"]:nth-of-type(3) [data-testid="stMetricValue"] > div { color: #6c5ce7 !important; }
    
    /* Botão Adicionar */
    .stButton>button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("Controle de Faturas")
st.caption(f"Usuário: Admin | BoggioSpeed Management")

# --- PAINEL DE SOMATÓRIO ---
st.subheader("Painel de Somatório")
col1, col2, col3 = st.columns(3)

# Iniciando com zero, como deve ser antes da carga de dados
with col1:
    st.metric("Total de Entradas", "€ 0,00")
with col2:
    st.metric("Total de Saídas", "€ 0,00")
with col3:
    st.metric("Saldo Líquido", "€ 0,00")

st.divider()

# --- ÁREA DA TABELA ---
col_title, col_btn = st.columns([0.8, 0.2])
with col_title:
    st.subheader("Faturas Registradas")
with col_btn:
    st.button("＋ Adicionar Fatura", use_container_width=True)

# Tabela vazia com o cabeçalho correto (removi as notas 137 e 138)
columns = ["Nº NOTA", "CLIENTE", "ENTRADA (€)", "FORNECEDOR 1", "SAÍDA F1 (€)", "FORNECEDOR 2", "SAÍDA F2 (€)", "AÇÕES"]
df_empty = pd.DataFrame(columns=columns)
st.dataframe(df_empty, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Histórico de Ações")
st.info("Aguardando novas operações...")
