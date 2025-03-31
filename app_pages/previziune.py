import streamlit as st
import pandas as pd
from pandas import read_excel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def show_previziune_page(df_games):
    st.header("Predicția Prețului unui Joc Nou")

    df_cleaned = read_excel("./dataOUT/outliers.xlsx")
    df_games = pd.DataFrame(df_cleaned, columns=df_games.columns)
    df_games["Price"] = pd.to_numeric(df_games["Price"], errors='coerce')

    # Selectăm doar coloanele relevante
    features = ["Year", "Genre", "Developer", "Console"]
    df_games = df_games.dropna(subset=["Price"])  # Eliminăm rândurile fără preț
    df_features = df_games[features]
    df_target = df_games["Price"]

    # One-Hot Encoding pentru coloanele categorice
    df_encoded = pd.get_dummies(df_features, drop_first=True)

    # Separăm datele în antrenare și testare
    X_train, X_test, y_train, y_test = train_test_split(df_encoded, df_target, test_size=0.2, random_state=42)

    # Antrenăm modelul
    model = LinearRegression()
    model.fit(X_train, y_train)
    st.subheader("Introduceți detaliile jocului nou:")

    # Introducerea datelor de către utilizator
    year = st.number_input("Anul lansării:", min_value=1980, max_value=2030, value=2024, step=1)
    genre = st.selectbox("Genul jocului:", df_games["Genre"].dropna().unique())
    developer = st.selectbox("Dezvoltator:", df_games["Developer"].dropna().unique())
    console = st.selectbox("Consola:", df_games["Console"].dropna().unique())

    # Crearea unui DataFrame pentru predicție
    input_data = pd.DataFrame([[year, genre, developer, console]], columns=features)

    # Aplicăm One-Hot Encoding pe input
    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(columns=df_encoded.columns, fill_value=0)  # Asigurăm aceleași coloane
    # Realizăm predicția
    predicted_price = model.predict(input_encoded)[0]

    st.success(f"Prețul estimat pentru jocul introdus este: **${predicted_price:.2f}**")