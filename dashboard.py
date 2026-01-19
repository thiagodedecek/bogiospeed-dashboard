import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="BogioSpeed Dashboard", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #012e67; }
    h1, h2, h3, p, span, label, .stMarkdown { color: white !important; }
    
    /* Metric Cards Styling */
    .metric-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.4);
    }
    .metric-card h2 { color: #012e67 !important; margin: 0; font-size: 32px; }
    .metric-card p { color: #555 !important; font-weight: bold; font-size: 16px; text-transform: uppercase; margin-bottom: 5px; }
    
    /* Table Styling */
    .stDataFrame { background-color: white; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE CONNECTION ---
def connect_to_sheets():
    # Use 'gcp_service_account_dashboard' in your Streamlit Cloud Secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds_dict = st.secrets["gcp_service_account_dashboard"] 
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        # Using your new sheet name
        return client.open("Gestao_BogioSpeed_v2").get_worksheet(0)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- 3. DASHBOARD LOGIC ---
sheet = connect_to_sheets()

if sheet:
    try:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Header
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            st.image("BOGIO-SPEED-Logo-1-1536x217.png", width=220)
        with col_title:
            st.title("Business Management Portal")

        st.markdown("<br>", unsafe_allow_html=True)

        if not df.empty:
            # Metrics Calculations
            # Important: Ensure your Google Sheet has exactly these headers
            total_income = pd.to_numeric(df['SOLD']).sum()
            total_costs = pd.to_numeric(df['BUYER']).sum() + pd.to_numeric(df['BUYER II']).sum()
            total_profit = pd.to_numeric(df['PRIFIT']).sum()

            # Summary Panel (3 Cards)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-card"><p>Total Income (Sold)</p><h2>€ {total_income:,.2f}</h2></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><p>Total Costs (Expenses)</p><h2>€ {total_costs:,.2f}</h2></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><p>Net Profit (Gains)</p><h2 style="color: #2ecc71 !important;">€ {total_profit:,.2f}</h2></div>', unsafe_allow_html=True)

            st.markdown("---")

            # Data Table
            st.subheader("Recent Activity History")
            display_cols = ['JOB Nº', 'DATE', 'CUSTOMER', 'SUPPLIER', 'SOLD', 'PRIFIT']
            st.dataframe(df[display_cols].tail(20), use_container_width=True)
        else:
            st.info("The database is currently empty. Please add records to 'Gestao_BogioSpeed_v2'.")

    except Exception as e:
        st.error(f"Data Processing Error: {e}. Check if column headers in Google Sheets match exactly.")
else:
    st.info("Awaiting connection to Google Sheets...")
