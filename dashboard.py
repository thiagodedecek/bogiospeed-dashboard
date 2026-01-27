import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. Configuração de Estilo e Página (Fiel ao Protótipo HTML)
st.set_page_config(page_title="BoggioSpeed Invoice", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f9fafb; }
    /* Estilização dos Cards */
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 800; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; background-color: #2563eb; color: white; border: none; padding: 0.5rem; }
    .stButton>button:hover { background-color: #1e40af; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com Google Sheets (Usando sua regra de aspas triplas nos Secrets)
def get_gsheet_connection():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        # Puxa as credenciais dos Secrets do Streamlit Cloud
        creds_info = st.secrets["gcp_service_account_dashboard"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        # Nome da sua planilha v2
        return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

# 3. Lógica Principal
sheet = get_gsheet_connection()

if sheet:
    # Carregar dados
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    # --- SIDEBAR: FORMULÁRIO DE CADASTRO ---
    with st.sidebar:
        st.header("➕ Add New Invoice")
        st.info("Preencha os dados operacionais abaixo.")
        
        with st.form("invoice_form", clear_on_submit=True):
            fatura_interna = st.text_input("N° Fatura Interna / Job Nº")
            tipo_servico = st.selectbox("Tipo de Serviço", ["Delivery", "Logistics", "Maintenance", "Consultancy"])
            cliente_nome = st.text_input("Cliente (Per Ricevere)")
            data_vencimento = st.date_input("Data de Vencimento", datetime.now())
            
            st.divider()
            valor_receber = st.number_input("Valore Cliente (€) - A Receber", min_value=0.0, step=0.01)
            valor_pagar_1 = st.number_input("Valore Fornitore 1 (€) - A Pagar", min_value=0.0, step=0.01)
            
            submit = st.form_submit_button("ADICIONAR FATURA")

            if submit:
                if fatura_interna and cliente_nome:
                    # Formata a linha conforme as colunas da sua planilha v2
                    # DATE | KIND | CUSTOMER | SOLD | BUYER | BUYER II | JOB Nº
                    new_row = [
                        data_vencimento.strftime("%d/%m/%Y"),
                        tipo_servico,
                        cliente_nome,
                        valor_receber,
                        valor_pagar_1,
                        0, # Valor fixo para Buyer II inicial
                        fatura_interna
                    ]
                    sheet.append_row(new_row)
                    st.success("Fatura registrada com sucesso!")
                    st.rerun()
                else:
                    st.warning("Por favor, preencha o número da fatura e o cliente.")

    # --- PAINEL PRINCIPAL: DASHBOARD ---
    st.title("BoggioSpeed Invoice 📄")
    st.caption("Controle Operacional de Contas a Receber e Pagar")

    if not df.empty:
        # Cálculos de Saldo (Fatos Operacionais)
        total_receber = pd.to_numeric(df['SOLD'], errors='coerce').sum()
        total_pagar = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER II'], errors='coerce').sum()
        saldo_liquido = total_receber - total_pagar

        # Layout de 3 Colunas (Igual ao Protótipo)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("A RECEBER TOTAL")
            st.metric(label="", value=f"€ {total_receber:,.2f}")
            st.markdown('<div style="height:4px; background-color:#22c55e;"></div>', unsafe_allow_html=True)
            
        with col2:
            st.subheader("A PAGAR TOTAL")
            st.metric(label="", value=f"€ {total_pagar:,.2f}")
            st.markdown('<div style="height:4px; background-color:#ef4444;"></div>', unsafe_allow_html=True)
            
        with col3:
            st.subheader("SALDO LÍQUIDO")
            st.metric(label="", value=f"€ {saldo_liquido:,.2f}")
            st.markdown('<div style="height:4px; background-color:#3b82f6;"></div>', unsafe_allow_html=True)

        st.divider()

        # Tabela de Histórico
        st.subheader("Histórico de Faturas")
        # Filtro de busca simples
        search = st.text_input("🔍 Buscar por Cliente ou Job Nº")
        
        # Preparar dataframe para exibição
        display_df = df[['DATE', 'KIND', 'CUSTOMER', 'SOLD', 'JOB Nº']].copy()
        display_df.columns = ['Vencimento', 'Tipo', 'Cliente', 'Valor (€)', 'Job Nº']
        
        if search:
            display_df = display_df[display_df['Cliente'].str.contains(search, case=False) | 
                                    display_df['Job Nº'].astype(str).str.contains(search)]

        st.dataframe(display_df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum dado encontrado na planilha.")
