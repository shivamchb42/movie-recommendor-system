import numpy as np
import pandas as pd
import ast #for converting string indices to int
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle
import os
import pickle
from generate_data import MovieDataset

def main():
    # Check if the .pkl files already exist
    if not (os.path.exists('model/movie_list.pkl') and os.path.exists('model/similarity.pkl')):
        # Create an instance of the MovieDataset class
        dataset = MovieDataset()

        # Load and preprocess the dataset
        dataset.load_dataset('model/data/tmdb_5000_movies.csv', 'model/data/tmdb_5000_credits.csv')
        mv = dataset.preprocess_dataset()

        # Access the processed dataset
        movies = dataset.get_processed_dataset()
        pickle.dump(mv, open('model/movie_list.pkl', 'wb'))
        movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
        new_df = movies[['movie_id', 'title', 'tags']]
        new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
        ps = PorterStemmer()

        # Define the stem function here
        def stem(text):
            y = []
            for i in text.split():
                y.append(ps.stem(i))
            return " ".join(y)

        new_df['tags'] = new_df['tags'].apply(stem)
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vector = cv.fit_transform(new_df['tags']).toarray()
        similarity = cosine_similarity(vector)

        # Save the data to pickle files
        pickle.dump(similarity, open('model/similarity.pkl', 'wb'))

if __name__ == "__main__":
    main()