import streamlit as st
import pandas as pd

# 1. Configuração da página e tema forçado
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

# --- ESTILIZAÇÃO PARA FORÇAR TEMA CLARO E CORES ---
st.markdown("""
    <style>
    /* Força o fundo da página para um cinza muito claro/branco */
    .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* Títulos em azul escuro para contraste */
    h1, h2, h3, span, label {
        color: #1e3d59 !important;
    }

    /* Estilização Individual dos Cards de Somatório */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    /* Cores das Bordas e dos Números (Verde, Vermelho, Roxo) */
    /* Card 1: Entradas */
    div[data-testid="stMetric"]:nth-of-type(1) { border-left: 8px solid #28a745 !important; }
    div[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricValue"] > div { color: #28a745 !important; }
    
    /* Card 2: Saídas */
    div[data-testid="stMetric"]:nth-of-type(2) { border-left: 8px solid #dc3545 !important; }
    div[data-testid="stMetric"]:nth-of-type(2) [data-testid="stMetricValue"] > div { color: #dc3545 !important; }
    
    /* Card 3: Saldo */
    div[data-testid="stMetric"]:nth-of-type(3) { border-left: 8px solid #6c5ce7 !important; }
    div[data-testid="stMetric"]:nth-of-type(3) [data-testid="stMetricValue"] > div { color: #6c5ce7 !important; }

    /* Botão "Adicionar Fatura" em Roxo para destaque */
    div.stButton > button:first-child {
        background-color: #6c5ce7 !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO COM LOGO ---
# Se o arquivo 'logo.png' estiver no seu GitHub, ele lerá aqui. 
# Se não, ele apenas exibirá o título.
try:
    st.image("logo.png", width=250) # Certifique-se que o nome do arquivo no GitHub é exatamente logo.png
except:
    st.markdown("# 🚚 BOGIOSPEED") 

st.title("Controle de Faturas")
st.caption("Acesso Administrativo")

# --- PAINEL DE SOMATÓRIO ---
st.subheader("Painel de Somatório")
c1, c2, c3 = st.columns(3)
with c1: st.metric("Total de Entradas", "€ 0,00")
with c2: st.metric("Total de Saídas", "€ 0,00")
with c3: st.metric("Saldo Líquido", "€ 0,00")
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
