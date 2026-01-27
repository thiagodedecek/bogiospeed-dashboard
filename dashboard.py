# --- PAINEL DE SOMATÓRIO (COM CORES FORÇADAS INDIVIDUALMENTE) ---
st.subheader("Painel de Somatório")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <style>
        /* Card 1 - Verde */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] {
            border-left: 8px solid #28a745 !important;
        }
        [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetricValue"] > div {
            color: #28a745 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.metric("Total de Entradas", "€ 0,00")

with col2:
    st.markdown("""
        <style>
        /* Card 2 - Vermelho */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] {
            border-left: 8px solid #dc3545 !important;
        }
        [data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetricValue"] > div {
            color: #dc3545 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.metric("Total de Saídas", "€ 0,00")

with col3:
    st.markdown("""
        <style>
        /* Card 3 - Roxo */
        [data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] {
            border-left: 8px solid #6c5ce7 !important;
        }
        [data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetricValue"] > div {
            color: #6c5ce7 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.metric("Saldo Líquido", "€ 0,00")
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
