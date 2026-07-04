import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components
import html


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Pre-Flix Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ---------------- LOAD CSS FILE ----------------
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")


# ---------------- LOAD PARTICLE HTML ----------------
with open("particles.html", "r", encoding="utf-8") as f:
    components.html(f.read(), height=0)


# ---------------- POSTER FUNCTION ----------------
@st.cache_data
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f4af26913c738f35a868825fc6eb25f0&language=en-US",
            timeout=10
        )

        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/500x750.png?text=Poster+Error"


# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# ---------------- LOAD PICKLE DATA ----------------
movies_dict = pickle.load(open("movies.dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


# ---------------- RENDER JS MOVIE CARDS ----------------
def render_movie_cards(names, posters):
    with open("cards.css", "r", encoding="utf-8") as f:
        cards_css = f.read()

    with open("scripts.js", "r", encoding="utf-8") as f:
        scripts_js = f.read()

    cards_html = ""

    for name, poster in zip(names, posters):
        safe_name = html.escape(name, quote=True)
        safe_poster = html.escape(poster, quote=True)

        cards_html += f"""
        <div class="movie-card" data-title="{safe_name}" data-poster="{safe_poster}">
            <div class="poster-wrap">
                <img src="{safe_poster}" alt="{safe_name}">
            </div>

            <div class="movie-title">{safe_name}</div>

            <div class="action-row">
                <button class="action-btn fav-btn" onclick="addFavorite(this)">♡ Save</button>
                <button class="action-btn trailer-btn" onclick="openTrailer(this)">▶ Trailer</button>
                <button class="action-btn copy-btn" onclick="copyMovie(this)">📋 Copy Name</button>
            </div>
        </div>
        """

    full_html = f"""
    <style>
    {cards_css}
    </style>

    <div class="recommend-section">
        <h2 class="recommend-heading">Recommended Movies</h2>

        <div class="tool-bar">
            <button class="tool-btn" onclick="showFavorites()">⭐ Show Favorites</button>
            <button class="tool-btn" onclick="clearFavorites()">🗑 Clear Favorites</button>
        </div>

        <div id="favoriteBox" class="favorite-box">
            <h3>⭐ Your Favorite Movies</h3>
            <div id="favoriteList"></div>
        </div>

        <div class="movie-grid">
            {cards_html}
        </div>
    </div>

    <div id="toast"></div>

    <script>
    {scripts_js}
    </script>
    """

    components.html(full_html, height=760, scrolling=True)


# ---------------- MAIN UI ----------------
st.markdown(
    '<h1 class="main-title">🎬 Pre-Flix Movie Recommendation System</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Find similar movies instantly with posters, trailer search, favorite list and smooth animation.</p>',
    unsafe_allow_html=True
)


left, middle, right = st.columns([1, 2, 1])

with middle:
    selected_movie_name = st.selectbox(
        "Choose a movie:",
        movies["title"].values
    )

    recommend_button = st.button("Recommend Movies")


# ---------------- SHOW RECOMMENDED MOVIES ----------------
if recommend_button:
    names, posters = recommend(selected_movie_name)
    render_movie_cards(names, posters)


st.markdown(
    '<div class="footer">Made by prethul· Pre-Flix Movie Recommendation System</div>',
    unsafe_allow_html=True
)