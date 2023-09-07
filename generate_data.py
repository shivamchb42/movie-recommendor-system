import numpy as np
import pandas as pd
import ast  # for converting string indices to int

class MovieDataset:
    def __init__(self):
        self.movies = None

    def load_dataset(self, movies_csv_path, credits_csv_path):
        # Load and merge the dataset
        movies = pd.read_csv(movies_csv_path)
        credits = pd.read_csv(credits_csv_path)
        self.movies = movies.merge(credits, on='title')
        self.movies = self.movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        self.movies.dropna(inplace=True)

    @staticmethod
    def convert(text):
        L = []
        for i in ast.literal_eval(text):
            L.append(i['name'])
        return L

    @staticmethod
    def fetch_director(text):
        L = []
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L

    def preprocess_dataset(self):
        if self.movies is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        # Apply data preprocessing steps
        self.movies['genres'] = self.movies['genres'].apply(self.convert)
        self.movies['keywords'] = self.movies['keywords'].apply(self.convert)
        self.movies['cast'] = self.movies['cast'].apply(self.convert)
        self.movies['cast'] = self.movies['cast'].apply(lambda x: x[0:3])
        self.movies['crew'] = self.movies['crew'].apply(self.fetch_director)
        return self.movies

    def get_processed_dataset(self):
        if self.movies is None:
            raise ValueError("Dataset not loaded and preprocessed. Call load_dataset() and preprocess_dataset() first.")
        else:
            self.movies['overview'] = self.movies['overview'].apply(lambda x: x.split())
            self.movies['cast'] = self.movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
            self.movies['crew'] = self.movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
            self.movies['genres'] = self.movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
            self.movies['keywords'] = self.movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
            return self.movies


# Example usage:
if __name__ == "__main__":
    dataset = MovieDataset()
    dataset.load_dataset('model/data/tmdb_5000_movies.csv', 'model/data/tmdb_5000_credits.csv')
    dataset.preprocess_dataset()
    movies_data = dataset.get_processed_dataset()