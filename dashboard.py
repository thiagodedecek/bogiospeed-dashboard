import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

# 2. CSS Corrigido para os Cards Coloridos (Igual à sua imagem 32621c)
st.markdown("""
    <style>
    /* Estilização dos Cards de Somatório */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Cores das bordas laterais */
    div[data-testid="stMetric"]:nth-of-type(1) { border-left: 5px solid #28a745; } /* Verde */
    div[data-testid="stMetric"]:nth-of-type(2) { border-left: 5px solid #dc3545; } /* Vermelho */
    div[data-testid="stMetric"]:nth-of-type(3) { border-left: 5px solid #6c5ce7; } /* Roxo */
    
    [data-testid="stMetricValue"] { font-size: 26px; font-weight: bold; }
    
    /* Ajuste de botões */
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("Controle de Faturas")
# Puxando o email dos secrets ou apenas um texto padrão
st.caption("Usuário: Admin | BoggioSpeed Management")

# --- PAINEL DE SOMATÓRIO (VALORES PARA TESTE VISUAL) ---
st.subheader("Painel de Somatório")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Entradas", "€ 1.200,00")
with col2:
    st.metric("Total de Saídas", "€ 450,00")
with col3:
    st.metric("Saldo Líquido", "€ 750,00")

st.divider()

# --- ÁREA DA TABELA ---
col_title, col_btn = st.columns([0.8, 0.2])
with col_title:
    st.subheader("Faturas Registradas")
with col_btn:
    # Botão azul como no protótipo
    st.button("＋ Adicionar Fatura", type="primary", use_container_width=True)

# Exemplo de visualização da tabela (Fatos operacionais)
data_exemplo = {
    "Nº NOTA": ["137", "138"],
    "CLIENTE": ["CHIMICAL", "LOGISTIC S.A"],
    "ENTRADA (€)": ["€ 1.000,00", "€ 200,00"],
    "FORNECEDOR 1": ["ALA", "FUEL CO"],
    "SAÍDA F1 (€)": ["€ 400,00", "€ 50,00"],
    "FORNECEDOR 2": ["-", "-"],
    "SAÍDA F2 (€)": ["€ 0,00", "€ 0,00"],
    "AÇÕES": ["📝 | 🗑️", "📝 | 🗑️"]
}
df_visual = pd.DataFrame(data_exemplo)
st.dataframe(df_visual, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Histórico de Ações")
st.info("Aguardando novas operações...")
