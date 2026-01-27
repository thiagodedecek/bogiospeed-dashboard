import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="BogioSpeed Dashboard", layout="wide")

# 1. CONEXÃO SEGURA (Usando sua regra de aspas triplas)
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account_dashboard"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    # Abre a planilha pelo nome exato que está na sua imagem
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

try:
    sheet = connect_to_sheets()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Logotipo (usando o arquivo que está no seu GitHub)
    st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=300)
    st.title("Invoices Control & Management")

    if not df.empty:
        # 2. CÁLCULOS DOS SOMATÓRIOS (Baseado nas colunas da image_af7e3d.png)
        # Convertendo para numérico para evitar erros de soma
        total_income = pd.to_numeric(df['SOLD'], errors='coerce').sum()
        
        # Expenses é a soma de BUYER + BUYER II
        expenses_1 = pd.to_numeric(df['BUYER'], errors='coerce').sum()
        expenses_2 = pd.to_numeric(df['BUYER II'], errors='coerce').sum()
        total_expenses = expenses_1 + expenses_2
        
        net_balance = total_income - total_expenses

        # 3. PAINEL DE SOMATÓRIO (Em Inglês)
        st.subheader("Summary Panel")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Income", f"€ {total_income:,.2f}")
        with col2:
            st.metric("Total Expenses", f"€ {total_expenses:,.2f}")
        with col3:
            st.metric("Net Balance", f"€ {net_balance:,.2f}")

        st.markdown("---")

        # 4. HISTÓRICO DE AÇÕES (Action History)
        st.subheader("Action History")
        # Filtrando apenas as colunas relevantes para o histórico
        history_df = df[['DATE', 'CUSTOMER', 'JOB Nº', 'KIND']].copy()
        history_df.columns = ['Date', 'Customer', 'Job No.', 'Service Type']
        st.table(history_df.tail(10)) # Mostra as últimas 10 ações

    else:
        st.info("The spreadsheet is currently empty.")

except Exception as e:
    st.error(f"Critical Error: {e}")
