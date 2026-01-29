import streamlit as st
import pandas as pd
from gspread_pandas import Spread
import os

st.set_page_config(page_title="BogioSpeed Management", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #f8f9fa !important; }

input, textarea, select, .stTextInput input, .stNumberInput input {
    background-color: white !important;
    color: black !important;
}

div[data-testid="column"] div[data-testid="stMetric"] {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
}

div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
    border-left: 8px solid #28a745 !important;
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
    border-left: 8px solid #dc3545 !important;
}
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
    border-left: 8px solid #6c5ce7 !important;
}

div.stButton > button {
    background-color: #ffc107 !important;
    color: #000 !important;
    font-weight: bold !important;
    border: none !important;
}

h1, h2, h3, p { color: #1e3d59 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    try:
        creds = st.secrets["gcp_service_account"]
        spread = Spread('Gestao_BogioSpeed_v2', config=creds)
        df = spread.sheet_to_df(index=None)
        return spread, df
    except Exception as e:
        st.exception(e)
        return None, pd.DataFrame()

spread, df_real = load_data()

logo_path = "BOGIO-SPEED-Logo-1-1536x217.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
else:
    st.header("🚚 BOGIOSPEED SYSTEM")

st.title("Invoice Management")

customer_options = sorted([
    "CLIENTES (CLIENTE)", "CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &",
    "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA",
    "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.",
    "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S  S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI",
    "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING",
    "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA",
    "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL",
    "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG",
    "BISELLO TECNOLOGY SYSTEM SRL"
])

supplier_options = sorted([
    "FORNECEDORES (FORNIT)", "NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA",
    "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA",
    "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO",
    "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG",
    "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT",
    "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS",
    "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA",
    "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS"
])

with st.expander("➕ Add Invoice", expanded=False):
    with st.form("invoice_form"):
        c1, c2 = st.columns(2)
        with c1:
            job_no = st.text_input("JOB NO")
        with c2:
            date = st.date_input("DATE")

        c3, c4 = st.columns(2)
        with c3:
            customer = st.selectbox("CUSTOMER", options=customer_options + ["Other"])
            if customer == "Other":
                customer = st.text_input("New CUSTOMER")
        with c4:
            sold = st.number_input("SOLD (€)", min_value=0.0)

        c5, c6 = st.columns(2)
        with c5:
            supplier = st.selectbox("SUPPLIER", options=supplier_options + ["Other"])
            if supplier == "Other":
                supplier = st.text_input("New SUPPLIER")
            supplier2 = st.text_input("SUPPLIER II")
        with c6:
            buyer = st.number_input("BUYER (€)", min_value=0.0)
            buyer2 = st.number_input("BUYER II (€)", min_value=0.0)

        c7, c8 = st.columns(2)
        with c7:
            inv1 = st.text_input("INVOICE I")
        with c8:
            inv2 = st.text_input("INVOICE II")

        c9, c10, c11 = st.columns(3)
        with c9:
            kind = st.text_input("TYPE")
        with c10:
            plate = st.text_input("LICENSE PLATE")
        with c11:
            closed = st.date_input("CLOSED DATE")

        profit = sold - (buyer + buyer2)

        if st.form_submit_button("Save Invoice"):
            nova_linha = [[
                job_no, str(date), customer, kind,
                supplier, supplier2, sold,
                buyer, buyer2, profit, str(closed),
                inv1, inv2, plate
            ]]

            spread.df_to_sheet(
                pd.DataFrame(nova_linha),
                index=False,
                sheet='Sheet1',
                replace=False
            )


            )

            st.success("✅ Invoice saved successfully!")
            st.rerun()

st.divider()
st.subheader("📊 Summary Panel")

if not df_real.empty:
    total_revenue = pd.to_numeric(df_real["SOLD"], errors='coerce').sum()
    total_expenses = pd.to_numeric(df_real["BUYER"], errors='coerce').fillna(0) + pd.to_numeric(df_real["BUYER II"], errors='coerce').fillna(0)
    total_expenses = total_expenses.sum()
    net_balance = total_revenue - total_expenses
else:
    total_revenue = total_expenses = net_balance = 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"€ {total_revenue:,.2f}")
col2.metric("Total Expenses", f"€ {total_expenses:,.2f}")
col3.metric("Net Balance", f"€ {net_balance:,.2f}")

st.divider()
st.subheader("📁 Registered Invoices")

if not df_real.empty:
    st.dataframe(df_real, use_container_width=True, hide_index=True)
else:
    st.info("📭 No invoices registered yet.")
