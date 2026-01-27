import streamlit as st
import pandas as pd
from gspread_pandas import Spread

# 1. Configuração e Layout (Mantendo o que funcionou na image_316abc.png)
st.set_page_config(page_title="BoggioSpeed Management", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    div[data-testid="column"] div[data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] { border-left: 8px solid #28a745 !important; }
    div[data-testid="column"]:nth-of-type(1) [data-testid="stMetricValue"] > div { color: #28a745 !important; }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] { border-left: 8px solid #dc3545 !important; }
    div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricValue"] > div { color: #dc3545 !important; }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] { border-left: 8px solid #6c5ce7 !important; }
    div[data-testid="column"]:nth-of-type(3) [data-testid="stMetricValue"] > div { color: #6c5ce7 !important; }
    h1, h2, h3 { color: #1e3d59 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Função de Conexão com a Planilha
@st.cache_resource
def conectar_planilha():
    try:
        # Usa o segredo que configuramos com aspas triplas
        creds = st.secrets["gcp_service_account"]
        spread = Spread('Gestao_BogioSpeed_v2', config=creds)
        return spread
    except Exception as e:
        st.error(f"Erro na conexão com a planilha: {e}")
        return None

# Carregar dados
spread = conectar_planilha()

if spread:
    df_real = spread.sheet_to_df(index=None)
    
    # 3. Sidebar: Inserção de Dados (Botão e Formulário)
    with st.sidebar:
        st.title("🚚 Operações")
        st.subheader("Inserir Nova Invoice")
        with st.form("form_novo_registro", clear_on_submit=True):
            f_nota = st.text_input("Nº NOTA")
            f_cliente = st.text_input("CLIENTE")
            f_entrada = st.number_input("ENTRADA (€)", min_value=0.0, step=0.01)
            f_forn1 = st.text_input("FORNECEDOR 1")
            f_saida1 = st.number_input("SAÍDA F1 (€)", min_value=0.0, step=0.01)
            f_forn2 = st.text_input("FORNECEDOR 2", value="-")
            f_saida2 = st.number_input("SAÍDA F2 (€)", min_value=0.0, step=0.01)
            
            submit = st.form_submit_button("GRAVAR DADOS", use_container_width=True)
            
            if submit:
                # Prepara a linha para a planilha
                nova_linha = [[f_nota, f_cliente, f_entrada, f_forn1, f_saida1, f_forn2, f_saida2]]
                # Envia para a próxima linha disponível
                spread.df_to_sheet(pd.DataFrame(nova_linha), index=False, header=False, start='A' + str(len(df_real) + 2))
                st.success("Gravado com sucesso!")
                st.rerun()

    # 4. Painel Principal (Cálculos Dinâmicos)
    st.title("Invoices Control & Management")
    
    # Convertendo para numerico para evitar erros de cálculo
    df_real['ENTRADA (€)'] = pd.to_numeric(df_real['ENTRADA (€)'], errors='coerce').fillna(0)
    df_real['SAÍDA F1 (€)'] = pd.to_numeric(df_real['SAÍDA F1 (€)'], errors='coerce').fillna(0)
    df_real['SAÍDA F2 (€)'] = pd.to_numeric(df_real['SAÍDA F2 (€)'], errors='coerce').fillna(0)

    total_in = df_real['ENTRADA (€)'].sum()
    total_out = df_real['SAÍDA F1 (€)'].sum() + df_real['SAÍDA F2 (€)'].sum()
    saldo = total_in - total_out

    st.subheader("Painel de Somatório")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Total de Entradas", f"€ {total_in:,.2f}")
    with c2: st.metric("Total de Saídas", f"€ {total_out:,.2f}")
    with c3: st.metric("Saldo Líquido", f"€ {saldo:,.2f}")

    st.divider()
    
    st.subheader("Faturas Registradas")
    if not df_real.empty:
        st.dataframe(df_real, use_container_width=True, hide_index=True)
    else:
        st.info("A planilha está vazia no momento.")

else:
    st.warning("Aguardando conexão com o Google Sheets...")
