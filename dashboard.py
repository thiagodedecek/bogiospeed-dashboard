import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="BogioSpeed Management Portal", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: #012e67 !important; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        text-align: left; border-left: 5px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-income { border-left-color: #28a745; }
    .card-expense { border-left-color: #dc3545; }
    .card-profit { border-left-color: #007bff; }
    .metric-card h2 { margin: 0; font-size: 28px; }
    .metric-card p { margin: 0; font-size: 14px; color: #6c757d !important; font-weight: bold; }
    .stButton>button { background-color: #f1c40f; color: #012e67; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO ---
def connect():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account_dashboard"] 
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)

lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Other / Altro"]
lista_fornecedores = ["None / Nessuno", "NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Other / Altro"]

sheet = connect()
# Lógica de segurança para planilha vazia
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except:
    df = pd.DataFrame(columns=['JOB Nº', 'DATE', 'CUSTOMER', 'KIND', 'SUPPLIER', 'SUPPLIER II', 'SOLD', 'BUYER', 'BUYER II', 'PRIFIT', 'CLOSED', 'INV I', 'INV II', 'PLATE Nº'])

# --- 3. HEADER & DASHBOARD ---
st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=350)
st.title("Invoices Control & Management")

if not df.empty:
    total_in = pd.to_numeric(df['SOLD'], errors='coerce').sum()
    total_out = pd.to_numeric(df['BUYER'], errors='coerce').sum() + pd.to_numeric(df['BUYER II'], errors='coerce').sum()
    net_balance = pd.to_numeric(df['PRIFIT'], errors='coerce').sum()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card card-income"><p>Total Income</p><h2 style="color:#28a745;">€ {total_in:,.2f}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card card-expense"><p>Total Expenses</p><h2 style="color:#dc3545;">€ {total_out:,.2f}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card card-profit"><p>Net Balance</p><h2 style="color:#007bff;">€ {net_balance:,.2f}</h2></div>', unsafe_allow_html=True)
else:
    st.info("The database is currently empty. Please add records to start.")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. FORMULÁRIO (ADD NEW) ---
with st.expander("➕ ADD NEW INVOICE", expanded=True):
    with st.form("new_entry", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_job = st.text_input("JOB Nº *")
            f_date = st.date_input("Date *", date.today())
            f_client = st.selectbox("Customer *", lista_clientes)
        with c2:
            f_sold = st.number_input("Sold Value (€) *", min_value=0.0, format="%.2f")
            f_plate = st.text_input("Plate Nº / Targa *")
            f_kind = st.text_input("Kind of Service", value="Rodoviário")
        with c3:
            f_closed = st.date_input("Job Closed Date", date.today())

        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**Supplier 1**")
            f_supp1 = st.selectbox("Supplier 1", lista_fornecedores[1:])
            f_pay1 = st.number_input("Buyer I Cost (€)", min_value=0.0, format="%.2f")
            f_inv1 = st.text_input("Invoice Nº I")
        with col_s2:
            st.markdown("**Supplier 2**")
            f_supp2 = st.selectbox("Supplier 2", lista_fornecedores)
            f_pay2 = st.number_input("Buyer II Cost (€)", min_value=0.0, format="%.2f")
            f_inv2 = st.text_input("Invoice Nº II")

        if st.form_submit_button("SAVE DATA"):
            f_profit = f_sold - f_pay1 - f_pay2
            new_row = [f_job, str(f_date), f_client, f_kind, f_supp1, f_supp2, f_sold, f_pay1, f_pay2, f_profit, str(f_closed), f_inv1, f_inv2, f_plate]
            sheet.append_row(new_row)
            st.success("Invoice Saved!")
            st.rerun()

# --- 5. HISTÓRICO & EDIÇÃO ---
st.markdown("---")
if not df.empty:
    st.subheader("Registered Invoices")
    st.dataframe(df[['JOB Nº', 'DATE', 'CUSTOMER', 'SOLD', 'PROFIT', 'PLATE Nº']].tail(15), use_container_width=True)

    with st.expander("📝 EDIT / UPDATE EXISTING JOB"):
        job_list = df['JOB Nº'].astype(str).unique().tolist()
        job_to_edit = st.selectbox("Search JOB Nº", [""] + job_list)
        if job_to_edit:
            row_idx = df[df['JOB Nº'].astype(str) == job_to_edit].index[0]
            google_row_idx = row_idx + 2
            curr = df.iloc[row_idx]
            with st.form("edit_job_form"):
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    e_sold = st.number_input("Update Sold (€)", value=float(curr['SOLD']))
                    e_plate = st.text_input("Update Plate Nº", value=str(curr['PLATE Nº']))
                with e_col2:
                    e_buyer1 = st.number_input("Update Buyer I (€)", value=float(curr['BUYER']))
                    e_buyer2 = st.number_input("Update Buyer II (€)", value=float(curr['BUYER II']))
                if st.form_submit_button("UPDATE RECORD"):
                    e_profit = e_sold - e_buyer1 - e_buyer2
                    sheet.update_cell(google_row_idx, 7, e_sold)
                    sheet.update_cell(google_row_idx, 8, e_buyer1)
                    sheet.update_cell(google_row_idx, 9, e_buyer2)
                    sheet.update_cell(google_row_idx, 10, e_profit)
                    sheet.update_cell(google_row_idx, 14, e_plate)
                    st.success(f"Job {job_to_edit} updated!")
                    st.rerun()
