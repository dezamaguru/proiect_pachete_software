import streamlit as st
import pandas as pd
import numpy as np
from pandas import read_excel
import matplotlib.pyplot as plt
import seaborn as sns

def show_grupari_page(df_games):
    st.header("Grupări și Agregări")

    st.info(
        """
        **Această secțiune îți permite să analizezi datele Nintendo prin metode statistice.**  
        Poți grupa datele după anumite atribute și să aplici agregări precum:
        - **Media** unei variabile numerice.
        - **Minimul și maximul** pentru diverse atribute.
        - **Distribuția valorilor pe categorii.**
        """
    )

    df_cleaned = read_excel("./dataOUT/outliers.xlsx")
    df_games = pd.DataFrame(df_cleaned, columns=df_games.columns)
    df_games["Price"] = pd.to_numeric(df_games["Price"], errors='coerce')

    # Alegem o coloană pentru grupare
    group_by_column = st.selectbox("Selectați coloana după care se face gruparea:", df_games.columns)

    # Alegem metoda de agregare
    agg_method = st.selectbox(
        "Alege metoda de agregare:",
        ["Media", "Minim și Maxim", "Distribuție Categorică"]
    )

    df_grouped = df_games.copy()

    if agg_method == "Media":
        numeric_cols = df_games.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols.remove("Year")  # Excludem Year pentru că nu are sens media anilor
        selected_col = st.selectbox("Selectează o coloană numerică pentru medie:", numeric_cols)

        df_grouped = df_games.groupby(group_by_column)[selected_col].mean().reset_index()
        df_grouped.rename(columns={selected_col: f"Media {selected_col}"}, inplace=True)


    elif agg_method == "Minim și Maxim":
        numeric_cols = df_games.select_dtypes(include=[np.number]).columns.tolist()
        selected_col = st.selectbox("Selectează o coloană numerică:", numeric_cols)
        min_or_max = st.radio("Alege tipul de agregare:", ["Minim", "Maxim"])
        df_grouped = df_games.groupby(group_by_column)[selected_col].agg(["min", "max"]).reset_index()
        if min_or_max == "Minim":
            df_grouped = df_grouped[[group_by_column, "min"]].rename(columns={"min": f"Minim {selected_col}"})
        elif min_or_max == "Maxim":
            df_grouped = df_grouped[[group_by_column, "max"]].rename(columns={"max": f"Maxim {selected_col}"})
        st.subheader(f"Rezultatele pentru {min_or_max} {selected_col}:")
        st.dataframe(df_grouped)


    elif agg_method == "Distribuție Categorică":
        categorical_cols = df_games.select_dtypes(include=["object"]).columns.tolist()
        selected_col = st.selectbox("Selectează o coloană categorică:", categorical_cols)

        df_grouped = df_games[selected_col].value_counts().reset_index()
        df_grouped.columns = [selected_col, "Frecvență"]

        # 🔹 Afișăm un grafic pentru distribuția categorică
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=df_grouped[selected_col], y=df_grouped["Frecvență"], palette="viridis", ax=ax)
        plt.xticks(rotation=45)
        plt.title(f"Distribuția categorică a {selected_col}")
        plt.xlabel(selected_col)
        plt.ylabel("Frecvență")
        st.pyplot(fig)

    # Afișăm rezultatul
    st.subheader("Rezultatele grupării și agregării:")
    st.dataframe(df_grouped)