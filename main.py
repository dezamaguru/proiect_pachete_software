import streamlit as st
import pandas as pd
from app_pages.console import show_console_page
from app_pages.jocuri import show_games_page
from app_pages.analiza_date_lipsa import show_data_analysis_page
from app_pages.outliers import show_outliers_page
from app_pages.grupari import show_grupari_page
from app_pages.previziune import show_previziune_page
from app_pages.codificare import show_codificare_page
from app_pages.scalare import show_scalare_page
@st.cache_data
def load_data():
    try:
        df_games = pd.read_excel("./dataIN/games.xlsx")
        df_sales = pd.read_excel("./dataIN/nintendo_sales.xlsx")
        return df_games, df_sales
    except FileNotFoundError as e:
        st.error(f"Eroare: Fișierul nu a fost găsit - {e}")
        return None, None

df_games, df_sales = load_data()

st.title("Nintendo Data Dashboard")

st.markdown(
    '''
    <style>
    .custom-title {
        color: #F39C12;
        font-size: 40px;
        text-align: center;
        color: red !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('<h1 class="custom-title">Nintendo Data Analysis</h1>', unsafe_allow_html=True)

section = st.sidebar.radio("Navigați la:", ["Console", "Jocuri", "Analiză date lipsă", "Identificare Outliers", "Grupări și Agregări", "Previziune", "Codificare Categorii", "Scalare și Grupare Date"])

if df_games is not None and df_sales is not None:

    # Curățăm numele coloanelor pentru a evita erori din cauza spațiilor sau tipurilor de date
    df_sales.columns = df_sales.columns.astype(str).str.strip()
    df_games["Price"] = pd.to_numeric(df_games["Price"], errors='coerce')

    if section == "Console":
        show_console_page(df_sales)

    elif section == "Jocuri":
        show_games_page(df_games)

    elif section == "Analiză date lipsă":
        show_data_analysis_page(df_games)

    elif section == "Identificare Outliers":
        show_outliers_page(df_games)

    elif section == "Grupări și Agregări":
        show_grupari_page(df_games)

    elif section == "Previziune":
        show_previziune_page(df_games)

    elif section == "Codificare Categorii":
        show_codificare_page(df_games)

    elif section == "Scalare și Grupare Date":
        show_scalare_page(df_games)

    st.markdown("---")

else:
    st.error("Eroare la încărcarea fișierelor. Verificați că fișierele Excel sunt disponibile.")
