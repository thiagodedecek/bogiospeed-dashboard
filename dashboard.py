import streamlit as st
import pandas as pd

# 1. Configuração base
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

# 2. CSS Profissional para forçar o layout da imagem 32621c
st.markdown("""
    <style>
    /* Forçar fundo claro */
    .stApp { background-color: #f8f9fa !important; }
    
    /* Estilo Geral dos Cards */
    div[data-testid="column"] div[data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }

    /* CARD 1: ENTRADAS (VERDE) */
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] { border-left: 8px solid #28a745 !important; }
    div[data-testid="column"]:nth-of-type(1) [data-testid="stMetricValue"] > div { color: #28a745 !important; }

    /* CARD 2: SAÍDAS (VERMELHO) */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] { border-left: 8px solid #dc3545 !important; }
    div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricValue"] > div { color: #dc3545 !important; }

    /* CARD 3: SALDO (ROXO) */
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] { border-left: 8px solid #6c5ce7 !important; }
    div[data-testid="column"]:nth-of-type(3) [data-testid="stMetricValue"] > div { color: #6c5ce7 !important; }

    /* Ajuste de cor dos títulos */
    h1, h2, h3, p { color: #1e3d59 !important; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
# Tentativa de carregar a logo. Se falhar, exibe o texto.
try:
    st.image("logo.png", width=220)
except:
    st.header("🚚 BOGIOSPEED")

st.title("Controle de Faturas")
st.caption("Acesso Administrativo")

# --- PAINEL DE SOMATÓRIO ---
st.subheader("Painel de Somatório")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total de Entradas", "€ 1.000,00")
with c2:
    st.metric("Total de Saídas", "€ 500,00")
with c3:
    st.metric("Saldo Líquido", "€ 500,00")

st.divider()

# --- TABELA ---
st.subheader("Faturas Registradas")
# Criando as colunas vazias como você pediu (sem as notas 137/138)
cols = ["Nº NOTA", "CLIENTE", "ENTRADA (€)", "FORNECEDOR 1", "SAÍDA F1 (€)", "FORNECEDOR 2", "SAÍDA F2 (€)", "AÇÕES"]
st.dataframe(pd.DataFrame(columns=cols), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Histórico de Ações")
st.info("Sistema pronto para operação.")
