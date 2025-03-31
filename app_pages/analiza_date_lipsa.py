import streamlit as st
import pandas as pd
import numpy as np
import os

def show_data_analysis_page(df_games):
    st.header("Analiza și Tratarea Valorilor Lipsă")

    st.info(
        """
        Valorile lipsă pot afecta acuratețea modelelor de analiză și predicție.  
        În această secțiune poți identifica rapid valorile lipsă, înțelege impactul lor și le poți trata prin mai multe metode disponibile.
        """
    )

    # Identificare valori lipsă
    missing_values = df_games.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        st.subheader("Statistici despre valorile lipsă")

        missing_percent = (missing_values / len(df_games)) * 100
        missing_df = pd.DataFrame({
            "Număr de valori lipsă": missing_values,
            "% Valori lipsă": missing_percent.round(2)
        }).sort_values(by="% Valori lipsă", ascending=False)

        st.dataframe(missing_df)

        st.subheader("Vizualizare: procentaj valori lipsă")
        st.bar_chart(missing_df["% Valori lipsă"])

        # Alertă dacă unele coloane au valori lipsă în proporție mare
        if (missing_percent > 50).any():
            st.warning("Unele coloane au peste 50% valori lipsă. Poate fi mai bine să le elimini complet.")

        # Ghid pentru alegerea metodei
        with st.expander("Recomandări pentru alegerea metodei de tratare"):
            st.markdown("""
            - **Numerice**: Media / Mediana (atenție la outlieri).
            - **Categorice**: Moda.
            - **Forward Fill**: Util pentru date ordonate sau temporale.
            - **Ștergere**: Eficientă când ai puține rânduri afectate (sub 5%).
            """)

            # Rânduri afectate
        if st.checkbox("Afișează rândurile care conțin valori lipsă"):
            st.dataframe(df_games[df_games.isnull().any(axis=1)])

        st.subheader("🔧 Alege metoda de tratare:")
        method = st.radio("Metoda:",
            ["Ștergere rânduri", "Înlocuire cu Media", "Înlocuire cu Moda", "Înlocuire cu Mediana", "Înlocuire cu valori similare"])

        df_cleaned = df_games.copy()

        # Tratare
        if method == "Ștergere rânduri":
            df_cleaned = df_cleaned.dropna()
            st.success("Toate rândurile cu valori lipsă au fost eliminate.")

        elif method in ["Înlocuire cu Media", "Înlocuire cu Moda", "Înlocuire cu Mediana"]:
            for col in missing_df.index:
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    if method == "Înlocuire cu Media":
                        df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
                    elif method == "Înlocuire cu Mediana":
                        df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                    elif method == "Înlocuire cu Moda":
                        st.warning(f"Coloana `{col}` este numerică – moda poate să nu fie relevantă.")
                        df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
                else:
                    if method == "Înlocuire cu Moda":
                        df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
                    elif method in ["Înlocuire cu Media", "Înlocuire cu Mediana"]:
                        st.warning(f"Coloana `{col}` este categorică – metoda aleasă ({method}) nu este recomandată.")

            st.success("Valorile lipsă au fost tratate conform metodei selectate.")

        elif method == "Înlocuire cu valori similare":
            df_cleaned.fillna(method="ffill", inplace=True)
            st.success("Valorile lipsă au fost completate prin forward fill.")

        # Dataset final curățat
        st.subheader("Setul de date după tratarea valorilor lipsă:")
        st.dataframe(df_cleaned)

        if not os.path.exists("./dataOUT"):
            os.makedirs("./dataOUT")

        if st.button("Salvează setul de date prelucrat"):
            df_cleaned.to_excel("./dataOUT/games_cleaned.xlsx", index=False)
            st.success("Setul de date curățat a fost salvat cu succes!")

    else:
        st.success("Nu există valori lipsă în dataset!")
