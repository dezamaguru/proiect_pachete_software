import streamlit as st

def show_console_page(df_sales):
    st.header("Vânzările Consolelor Nintendo pe Ani")
    st.dataframe(df_sales)

    sales_years = [col for col in df_sales.columns if col.isdigit()]

    if "Console" in df_sales.columns:
        console_options = df_sales["Console"].dropna().unique()
        if console_options.size > 0:
            console_selection = st.sidebar.selectbox("Selectați consola pentru analiza vânzărilor:", console_options)

            if sales_years:
                sales_trend = df_sales[df_sales["Console"] == console_selection][sales_years].T
                sales_trend.columns = ["Vânzări"]
                sales_trend.index = sales_trend.index.astype(int)

                st.line_chart(sales_trend)
                st.write(f"Evoluția vânzărilor pentru: {console_selection}")
            else:
                st.warning("Nu s-au găsit coloane cu ani în datele despre vânzări.")
        else:
            st.warning("Nu există date despre vânzări pentru console.")
    else:
        st.warning("Coloana 'Console' nu există în datele încărcate.")
