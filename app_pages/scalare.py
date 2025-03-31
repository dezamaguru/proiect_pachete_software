import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def show_scalare_page(_):
    st.title("Scalare")

    try:
        df = pd.read_excel("./dataOUT/outliers.xlsx")
    except FileNotFoundError:
        st.error("Fișierul 'outliers.xlsx' nu a fost găsit.")
        return

    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.header("Metode de Scalare")
    if not numeric_cols:
        st.warning("Nu există coloane numerice pentru scalare.")
    else:
        selected_scaler = st.radio("Alege metoda de scalare:", ["StandardScaler", "MinMaxScaler"])
        selected_cols = st.multiselect("Selectează coloanele de scalat:", numeric_cols)

        if selected_cols:
            if selected_scaler == "StandardScaler":
                scaler = StandardScaler()
            else:
                scaler = MinMaxScaler()

            df_scaled = df[selected_cols].copy()
            df_scaled[selected_cols] = scaler.fit_transform(df_scaled[selected_cols])

            st.success("Scalare aplicată cu succes.")
            st.dataframe(df_scaled)

            if st.button("💾 Salvează rezultatul scalat"):
                df_scaled.to_excel("./dataOUT/scalare_output.xlsx", index=False)
                st.success("Rezultatul a fost salvat în 'scalare_output.xlsx'.")
