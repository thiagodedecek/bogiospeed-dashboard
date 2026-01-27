import streamlit as st
import pandas as pd

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

# Estilização CSS para os cards (idêntico à imagem 32621c)
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #28a745;
    }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    /* Estilo específico para cada card */
    div[data-testid="stMetric"]:nth-child(1) { border-left-color: #28a745; } /* Verde */
    div[data-testid="stMetric"]:nth-child(2) { border-left-color: #dc3545; } /* Vermelho */
    div[data-testid="stMetric"]:nth-child(3) { border-left-color: #6c5ce7; } /* Roxo */
    </style>
    """, unsafe_allow_stdio=True)

st.title("Controle de Faturas")
st.caption(f"Usuário ID: {st.experimental_user.get('email', 'Admin')}")

# --- PAINEL DE SOMATÓRIO ---
st.subheader("Painel de Somatório")
col1, col2, col3 = st.columns(3)

# Valores fictícios para teste visual (serão conectados à planilha na próxima etapa)
with col1:
    st.metric("Total de Entradas", "R$ 1.000,00")
with col2:
    st.metric("Total de Saídas", "R$ 500,00")
with col3:
    st.metric("Saldo Líquido", "R$ 500,00")

st.divider()

# --- TABELA DE FATURAS ---
col_tab, col_btn = st.columns([0.85, 0.15])
with col_tab:
    st.subheader("Faturas Registradas")
with col_btn:
    st.button("＋ Adicionar Fatura", type="primary", use_container_width=True)

# Exemplo de como a tabela aparecerá
data = {
    "Nº NOTA": ["250"],
    "CLIENTE": ["CHIMICAL"],
    "ENTRADA (R$)": ["R$ 1.000,00"],
    "FORNECEDOR 1": ["ALA"],
    "SAÍDA F1 (R$)": ["R$ 500,00"],
    "FORNECEDOR 2": ["-"],
    "SAÍDA F2 (R$)": ["R$ 0,00"],
    "AÇÕES": ["Editar | Excluir"]
}
df_visual = pd.DataFrame(data)
st.table(df_visual)

st.subheader("Histórico de Ações")
# Aqui entrará a tabela de logs simplificada
