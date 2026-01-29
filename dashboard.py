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
        # Grupo 1 — JOB e DATE
        c1, c2 = st.columns(2)
        with c1:
            job_no = st.text_input("JOB NO")
        with c2:
            date = st.date_input("DATE")

        # Grupo 2 — CUSTOMER e REVENUE
        c3, c4 = st.columns(2)
        with c3:
            customer = st.selectbox("CUSTOMER", options=customer_options + ["Other"])
            if customer == "Other":
                customer = st.text_input("New CUSTOMER")
        with c4:
            revenue = st.number_input("SOLD  (€)", min_value=0.0)

        # Grupo 3 — SUPPLIERS e valores
        c5, c6 = st.columns(2)
        with c5:
            supplier = st.selectbox("SUPPLIER", options=supplier_options + ["Other"])
            if supplier == "Other":
                supplier = st.text_input("New SUPPLIER")
            supplier2 = st.text_input("SUPPLIER II")
        with c6:
            buyer = st.number_input("BUYER (€)", min_value=0.0)
            buyer2 = st.number_input("BUYER II (€)", min_value=0.0)

        # Grupo 4 — INVOICES
        c7, c8 = st.columns(2)
        with c7:
            inv1 = st.text_input("INVOICE I")
        with c8:
            inv2 = st.text_input("INVOICE II")

        # Grupo 5 — TYPE, LICENSE PLATE, CLOSED DATE
        c9, c10, c11 = st.columns(3)
        with c9:
            kind = st.text_input("TYPE")
        with c10:
            plate = st.text_input("LICENSE PLATE")
        with c11:
            closed = st.date_input("CLOSED DATE")

        # Cálculo do lucro
        profit = sold  - (buyer + buyer2)

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
                header=False,
                start='A' + str(len(df_real) + 2)
            )

            st.success("✅ Invoice saved successfully!")
            st.rerun()
