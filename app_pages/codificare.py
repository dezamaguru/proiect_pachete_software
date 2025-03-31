import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

def show_codificare_page(_):
    st.title("Codificare Categorii")

    try:
        df = pd.read_excel("./dataOUT/games_cleaned.xlsx")
        st.info("Datele au fost preluate din 'games_cleaned.xlsx'.")
    except FileNotFoundError:
        st.error("Fișierul 'games_cleaned.xlsx' nu a fost găsit.")
        return

    df = df.copy()
    st.subheader("Date Inițiale")
    st.dataframe(df.head())

    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not categorical_cols:
        st.warning("⚠️ Nu există coloane categorice în setul de date.")
        return

    selected_cat = st.selectbox("🔽 Selectează o coloană categorică:", categorical_cols)

    st.markdown("## Alege metoda de codificare aplicabilă")
    available_methods = ["One-Hot Encoding", "Label Encoding", "Frequency Encoding"]
    if "Price" in df.columns:
        available_methods.append("Target Encoding")

    method = st.radio("Metoda de codificare:", available_methods)

    df_result = pd.DataFrame()

    if method == "One-Hot Encoding":
        if df[selected_cat].nunique() > 20:
            st.warning("Coloana selectată are prea multe categorii pentru one-hot encoding.")
        else:
            df_result = pd.get_dummies(df[[selected_cat]], columns=[selected_cat], drop_first=True)
            st.success("One-Hot Encoding aplicat cu succes.")
            st.dataframe(df_result)

    elif method == "Label Encoding":
        le = LabelEncoder()
        df_result = df[[selected_cat]].copy()
        df_result[selected_cat + "_label"] = le.fit_transform(df_result[selected_cat])
        st.success("Label Encoding aplicat.")
        st.dataframe(df_result)

    elif method == "Frequency Encoding":
        freq_encoding = df[selected_cat].value_counts(normalize=True)
        df_result = df[[selected_cat]].copy()
        df_result[selected_cat + "_freq"] = df[selected_cat].map(freq_encoding)
        st.success("Frequency Encoding aplicat.")
        st.dataframe(df_result)

    elif method == "Target Encoding":
        target_col = st.selectbox("Selectează coloana țintă:", numeric_cols)
        target_mean = df.groupby(selected_cat)[target_col].mean()
        df_result = df[[selected_cat]].copy()
        df_result[selected_cat + "_target"] = df[selected_cat].map(target_mean)
        st.success("Target Encoding aplicat.")
        st.dataframe(df_result)

    st.markdown("## 📊 Vizualizare distribuție")
    if st.checkbox("Afișează countplot pentru variabilă"):
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(x=selected_cat, data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.markdown("## 💾 Salvare rezultat")
    if not df_result.empty and st.button("Salvează rezultatul encoding"):
        df_result.to_excel(f"./dataOUT/{selected_cat}_{method.replace(' ', '_').lower()}.xlsx", index=False)
        st.success("Rezultatul a fost salvat cu succes.")
