
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def find_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_df = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return lower_bound, upper_bound, outliers_df

def show_outliers_page(_):
    st.header("Analiza Outlierilor cu metoda IQR")

    try:
        df_games = pd.read_excel("./dataOUT/games_cleaned.xlsx")
        st.info("Datele au fost preluate din 'games_cleaned.xlsx'.")
    except FileNotFoundError:
        st.error("Fișierul 'games_cleaned.xlsx' nu a fost găsit.")
        return

    df_games["Price"] = pd.to_numeric(df_games["Price"], errors="coerce")
    numeric_cols = df_games.select_dtypes(include=[np.number]).columns.tolist()
    relevant_cols = st.multiselect("Selectează coloanele pentru analiză outlieri:", numeric_cols, default=["Price"])

    all_outliers = pd.DataFrame()

    for col in relevant_cols:
        if col in df_games.columns:
            lower, upper, outliers_df = find_outliers_iqr(df_games, col)

            st.subheader(f"📊 Coloana: {col}")
            st.write(f"Limita inferioară: **{lower:.2f}**, Limita superioară: **{upper:.2f}**")
            st.write(f"Număr de outlieri: **{len(outliers_df)}**")
            st.dataframe(outliers_df)

            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(x=df_games[col], ax=ax)
            plt.title(f"Boxplot pentru '{col}'")
            plt.tight_layout()
            st.pyplot(fig)

            all_outliers = pd.concat([all_outliers, outliers_df])

    st.markdown("---")
    st.subheader("🎯 Metodă de tratare pentru o coloană:")
    selected_col = st.selectbox("Coloană pentru tratare:", numeric_cols)
    lower, upper, outliers = find_outliers_iqr(df_games, selected_col)

    treat_method = st.radio("Alege metoda de tratare:", ["Păstrează", "Elimină", "Transformare logaritmică", "Capping (Winsorization)"])
    df_cleaned = df_games.copy()

    if treat_method == "Elimină":
        outlier_indexes = set()
        for col in relevant_cols:
            if col in df_cleaned.columns:
                _, _, outliers_df = find_outliers_iqr(df_cleaned, col)
                outlier_indexes.update(outliers_df.index)
        df_cleaned = df_cleaned[~df_cleaned.index.isin(outlier_indexes)]
        st.success("Outlierii au fost eliminați.")

    elif treat_method == "Transformare logaritmică":
        df_cleaned[selected_col + "_log"] = np.log1p(df_cleaned[selected_col])
        st.success("Transformarea logaritmică a fost aplicată.")

    elif treat_method == "Capping (Winsorization)":
        lower_perc = df_cleaned[selected_col].quantile(0.01)
        upper_perc = df_cleaned[selected_col].quantile(0.99)
        df_cleaned[selected_col + "_winsor"] = np.where(
            df_cleaned[selected_col] < lower_perc, lower_perc,
            np.where(df_cleaned[selected_col] > upper_perc, upper_perc, df_cleaned[selected_col])
        )
        st.success("Capping-ul (Winsorization) a fost aplicat.")

    else:
        st.info("Nu a fost aplicată nicio modificare asupra outlierilor.")

    st.markdown("## Setul de date după tratare")
    st.dataframe(df_cleaned)

    if st.button("💾 Salvează dataset-ul curățat"):
        df_cleaned.to_excel("./dataOUT/outliers.xlsx", index=False)
        st.success("Datele au fost salvate cu succes în 'dataOUT/outliers.xlsx'")
