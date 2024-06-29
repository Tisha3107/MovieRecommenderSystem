import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movie_posters

# Load data
st.title('Movie Recommender System')
st.markdown("### Find your next favorite movie based on your current preferences!")
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie)

    st.markdown("## Recommended Movies")
    st.write("Here are some movies you might like:")

    # Display recommendations in columns
    cols = st.columns(5)
    for col, movie, poster in zip(cols, recommended_movies, recommended_movie_posters):
        with col:
            st.markdown(f"**{movie}**")
            st.image(poster)
            st.markdown("---")  # Add a horizontal line for separation

# Additional styling and layout improvements
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 16px;
    }
    .stSelectbox {
        background-color: #f0f0f0;
        border-radius: 12px;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)
