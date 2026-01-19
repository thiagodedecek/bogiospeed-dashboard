import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import date

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="BogioSpeed Management Portal", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #012e67; }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: white !important; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 4px 4px 15px rgba(0,0,0,0.4);
    }
    .metric-card h2 { color: #012e67 !important; margin: 0; font-size: 30px; }
    .metric-card p { color: #555 !important; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .stButton>button { background-color: #f1c40f; color: #012e67; font-weight: bold; width: 100%; border-radius: 10px; height: 3em; }
    input, select, textarea, div[data-baseweb="select"] > div { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE CONNECTION ---
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds_dict = st.secrets["gcp_service_account_dashboard"] 
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

sheet = connect_to_sheets()

if sheet:
    # --- 3. LOAD DATA FOR DASHBOARD ---
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Header
    st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=250)
    st.title("Business Management Portal")

    # --- 4. TOP METRICS PANEL ---
    if not df.empty:
        total_income = pd.to_numeric(df['SOLD']).sum()
        total_costs = pd.to_numeric(df['BUYER']).sum() + pd.to_numeric(df['BUYER II']).sum()
        total_profit = pd.to_numeric(df['PRIFIT']).sum()

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><p>Total Income (Sold)</p><h2>€ {total_income:,.2f}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><p>Total Costs (Expenses)</p><h2>€ {total_costs:,.2f}</h2></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><p>Net Profit (Gains)</p><h2 style="color: #2ecc71 !important;">€ {total_profit:,.2f}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- 5. ENTRY FORM (The "Colab" experience) ---
    with st.form("entry_form", clear_on_submit=True):
        st.subheader("➕ Add New Job Record")
        c1, c2, c3 = st.columns(3)
        with c1:
            job_no = st.text_input("JOB Nº")
            job_date = st.date_input("DATE", date.today())
            customer = st.text_input("CUSTOMER")
        with c2:
            supplier1 = st.text_input("SUPPLIER I")
            buyer1 = st.number_input("BUYER I (Cost)", min_value=0.0, format="%.2f")
            invoice1 = st.text_input("INVOICE Nº I")
        with c3:
            supplier2 = st.text_input("SUPPLIER II (Optional)")
            buyer2 = st.number_input("BUYER II (Cost)", min_value=0.0, format="%.2f")
            sold = st.number_input("SOLD (Income)", min_value=0.0, format="%.2f")

        st.markdown(" ")
        save_btn = st.form_submit_button("SAVE RECORD & UPDATE DASHBOARD")

    # --- 6. SAVE LOGIC ---
    if save_btn:
        profit = sold - buyer1 - buyer2
        # Order: JOB Nº, DATE, CUSTOMER, KIND, SUPP1, SUPP2, SOLD, BUYER1, BUYER2, PROFIT, CLOSED, INV1, INV2, PLATE
        new_row = [job_no, str(job_date), customer, "Rodoviário", supplier1, supplier2, sold, buyer1, buyer2, profit, "", invoice1, "", ""]
        sheet.append_row(new_row)
        st.success("Record saved! Refreshing totals...")
        st.rerun() # This reloads the page to update the metrics at the top

    st.markdown("---")

    # --- 7. HISTORY TABLE ---
    st.subheader("Recent Activity History")
    if not df.empty:
        st.dataframe(df[['JOB Nº', 'DATE', 'CUSTOMER', 'SOLD', 'PRIFIT']].tail(10), use_container_width=True)
