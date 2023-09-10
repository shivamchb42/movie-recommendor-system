import pickle
import streamlit as st
import requests
import subprocess

def run_script(filename):
    try:
        # Run the process_data.py script
        subprocess.run(["python", filename], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error running script: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

run_script("content_based_rec.py")

st.header('Movie Recommender System')
movies = pickle.load(open('model\movie_list.pkl','rb'))
similarity = pickle.load(open('model\similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox( "Type or select a movie from the dropdown", movie_list)

if st.button('Search'):
    movt = st.experimental_get_query_params().get("mov")
    if movt is None:
        movt = selected_movie
    else:
        movt = movt[0]
    st.experimental_set_query_params(mov=movt)
    recommended_movie_names,recommended_movie_posters = recommend(movt)
    tdf = movies[movies['title'] == selected_movie].reset_index()
    st.image(fetch_poster(tdf.loc[0, 'movie_id']))
    st.text("Title: "+tdf.loc[0, 'title'])
    st.text("Overview: "+" ".join(tdf.loc[0, 'overview']))
    st.text("Genres: "+" ".join(tdf.loc[0, 'genres']))
    st.text("Cast: "+" ".join(tdf.loc[0, 'cast']))
    st.text("Director: "+" ".join(tdf.loc[0, 'crew']))
    st.text('Similar Movies')
    col1, col2, col3, col4, col5 = st.columns(5)
    # Iterate through recommended movies
    with col1:
        st.image(recommended_movie_posters[0])
        if(st.button(recommended_movie_names[0], key="movie0")):
            movt = recommended_movie_names[0]
    with col2:
        st.image(recommended_movie_posters[1])
        if(st.button(recommended_movie_names[1], key="movie1")):
            movt = recommended_movie_names[1]
    with col3:
        st.image(recommended_movie_posters[2])
        if(st.button(recommended_movie_names[2], key="movie2")):
            movt = recommended_movie_names[2]
    with col4:
        st.image(recommended_movie_posters[3])
        if(st.button(recommended_movie_names[3], key="movie3")):
            movt = recommended_movie_names[3]
    with col5:
        st.image(recommended_movie_posters[4])
        if(st.button(recommended_movie_names[4], key="movie4")):
            movt = recommended_movie_names[4]

                

else:
    # Number of images per page
    images_per_page = 16
    images_per_row = 4
    images_per_column = 4
    movie_ids = movies['movie_id'].values

    # Get the current page number from the URL
    page_number = st.experimental_get_query_params().get("page")

    # If page_number is None, default to 1
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number[0])

    # Calculate the range of images to display on the current page
    start_idx = (page_number - 1) * images_per_page
    end_idx = page_number * images_per_page

    # Slice the image URLs to get the images for the current page
    current_page_images = []
    for i in range(images_per_page):
        current_page_images.append(fetch_poster(movie_ids[i+start_idx]))

    # Create a grid of images
    for i in range(images_per_column):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(current_page_images[i * images_per_row])
        with col2:
            st.image(current_page_images[i * images_per_row +1])
        with col3:
            st.image(current_page_images[i * images_per_row +2])
        with col4:
            st.image(current_page_images[i * images_per_row +3])

    # Create pagination controls
    if len(movie_ids) > images_per_page:
        st.write("Page:", page_number)
        previous_page, next_page = st.columns(2)
        
        if previous_page.button("Previous Page", key="prev"):
            page_number = max(page_number - 1, 1)
        if next_page.button("Next Page", key="next"):
            page_number = min(page_number + 1, (len(movie_ids) - 1) // images_per_page + 1)
        
        # Set the URL query parameter to change the page
        st.experimental_set_query_params(page=page_number)