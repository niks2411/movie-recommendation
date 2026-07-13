import streamlit as st
import pickle
import requests

# 1. Page Configuration (Wide Layout)
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# 2. Inject Custom CSS with black header and compact spacing
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
/* Reduce Streamlit's default top padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0rem !important;
}

/* Gradient Title */
.main-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    text-align: center;
    background: linear-gradient(45deg, #FF4B4B, #FF8E53);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
}

/* Movie Card Container */
.movie-card {
    background-color: #131722;
    border: 1px solid #232733;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(255, 75, 75, 0.25);
    border-color: #FF4B4B;
}

/* Movie Poster Image */
.movie-poster {
    border-radius: 10px;
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    margin-bottom: 10px;
}

/* Movie Title Text */
.movie-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.0rem;
    font-weight: 600;
    color: #ffffff;
    margin: 0;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 2.6rem;
}

/* Button Styling Override */
div.stButton > button {
    background: linear-gradient(45deg, #FF4B4B, #FF8E53);
    color: white !important;
    border-radius: 20px;
    border: none;
    padding: 8px 30px;
    font-size: 1.05rem;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    transition: all 0.3s ease-in-out;
    width: 100%;
    margin-top: 5px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(255, 75, 75, 0.45);
    background: linear-gradient(45deg, #FF8E53, #FF4B4B);
}

/* Section Header (Black color for light backgrounds) */
.section-header {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #000000;
    margin-top: 1.2rem;
    margin-bottom: 1.0rem;
    border-left: 4px solid #FF4B4B;
    padding-left: 10px;
}
</style>
""")

# 3. Header section (Only Title, Subtitle removed)
st.html('<div class="main-title">🎬 English Movie Recommender System</div>')

# 4. Fetch Poster Helper function
def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=97fdca069e8bfd3db83a06696352721d&language=en-US'.format(movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception:
        return "https://placehold.co/500x750.png?text=No+Poster"

# 5. Recommendation Logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# 6. Load Data
movies = pickle.load(open('movie remcommendation/movies.pkl', 'rb'))
similarity = pickle.load(open('movie remcommendation/similarity.pkl', 'rb'))

movies_list = movies['title'].values

# 7. Selectbox UI (centered)
col_left, col_mid, col_right = st.columns([1.2, 1.6, 1.2])
with col_mid:
    selected_movie = st.selectbox(
        'Select a movie you like:',
        movies_list
    )
    btn_clicked = st.button('Recommend')

# 8. Render Results on Button Click
if btn_clicked:
    names, posters = recommend(selected_movie)
    
    st.html(f'<div class="section-header">Movies similar to: {selected_movie}</div>')
    
    # 5-column layout for movies
    cols = st.columns(5)
    for index in range(5):
        with cols[index]:
            st.html(f"""
            <div class="movie-card">
                <img class="movie-poster" src="{posters[index]}" />
                <p class="movie-name">{names[index]}</p>
            </div>
            """)
