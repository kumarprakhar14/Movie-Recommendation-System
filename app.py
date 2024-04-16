import streamlit as st 
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    respose = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a064a33edebdcef4a268f39bf54b2ee2&language=en-US'.format(movie_id))
    data = respose.json()
    return "https://image.tmdb.org/t/p/original/" +  data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]                   # calculate the cosine distance of the passed movie with every movie
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]   # find the list of 5 movie index having least distance and most similarity

    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would  like to be contacted?',
    movies['title'])

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0], use_column_width='auto', caption=names[0])
    with col2:
        st.image(posters[1], use_column_width='auto', caption=names[1])
    with col3:
        st.image(posters[2], use_column_width='auto', caption=names[2])
    with col4:
        st.image(posters[3], use_column_width='auto', caption=names[3])
    with col5:
        st.image(posters[4], use_column_width='auto', caption=names[4])
    

