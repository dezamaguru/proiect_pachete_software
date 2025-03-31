import streamlit as st

def show_games_page(df_games):
    st.header("Lista Jocurilor Nintendo")
    st.dataframe(df_games)

    if "Year" in df_games.columns:
        df_games = df_games.dropna(subset=["Year"])
        df_games["Year"] = df_games["Year"].astype(int)

        if df_games["Year"].nunique() > 1:
            min_year, max_year = int(df_games["Year"].min()), int(df_games["Year"].max())
            selected_year = st.sidebar.slider("Selectați anul de lansare:", min_value=min_year,
                                              max_value=max_year, value=(min_year, max_year))
            filtered_games = df_games[
                (df_games["Year"] >= selected_year[0]) & (df_games["Year"] <= selected_year[1])]
        else:
            filtered_games = df_games

        st.write("Jocuri filtrate după anul de lansare:")
        st.dataframe(filtered_games)
    else:
        st.warning("Coloana 'Year' nu există în datele încărcate.")