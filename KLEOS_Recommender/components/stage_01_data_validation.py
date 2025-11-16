import os
import sys
import pandas as pd
import pickle
from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.config.configuration import AppConfiguration
from KLEOS_Recommender.exception.exception_handler import AppException


class DataValidation:
    def __init__(self, app_config: AppConfiguration = AppConfiguration()):
        """
        Initialize the DataValidation component
        """
        try:
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def preprocess_data(self):
        """
        Preprocess the ratings and books datasets:
        - Keep only necessary columns
        - Rename columns for consistency
        - Filter users and books by thresholds
        - Merge ratings with books
        - Save cleaned CSV and pickled objects
        """
        try:
            # Read CSV files safely
            ratings = pd.read_csv(
                self.data_validation_config.ratings_csv_file,
                sep=";",
                on_bad_lines='skip',
                encoding='latin-1'
            )
            books = pd.read_csv(
                self.data_validation_config.books_csv_file,
                sep=";",
                on_bad_lines='skip',
                encoding='latin-1',
                dtype={"Year-Of-Publication": str}
            )


            logging.info(f"Ratings shape: {ratings.shape}")
            logging.info(f"Books shape: {books.shape}")

            # Keep necessary columns and rename
            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            books.rename(columns={
                'Book-Title': 'title',
                'Book-Author': 'author',
                'Year-Of-Publication': 'year',
                'Publisher': 'publisher',
                'Image-URL-L': 'image_url'
            }, inplace=True)

            ratings.rename(columns={
                'User-ID': 'user_id',
                'Book-Rating': 'rating'
            }, inplace=True)

            # Filter users with more than 200 ratings
            active_users = ratings['user_id'].value_counts() > 200
            active_user_ids = active_users[active_users].index
            ratings = ratings[ratings['user_id'].isin(active_user_ids)]

            # Merge ratings with books
            ratings_with_books = ratings.merge(books, on='ISBN', how='inner')

            # Compute number of ratings per book
            num_ratings = ratings_with_books.groupby('title')['rating'].count().reset_index()
            num_ratings.rename(columns={'rating': 'num_of_rating'}, inplace=True)
            final_rating = ratings_with_books.merge(num_ratings, on='title', how='inner')

            # Keep books with at least 50 ratings
            final_rating = final_rating[final_rating['num_of_rating'] >= 50]

            # Drop duplicates
            final_rating.drop_duplicates(subset=['user_id', 'title'], inplace=True, ignore_index=True)

            logging.info(f"Final cleaned data shape: {final_rating.shape}")

            # Save cleaned CSV
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_csv_path = os.path.join(self.data_validation_config.clean_data_dir, 'clean_data.csv')
            final_rating.to_csv(final_csv_path, index=False)
            logging.info(f"Saved cleaned data CSV to: {final_csv_path}")

            # Save pickled objects for web app / recommendation
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            final_rating_pickle_path = os.path.join(self.data_validation_config.serialized_objects_dir, "final_rating.pkl")
            with open(final_rating_pickle_path, 'wb') as f:
                pickle.dump(final_rating, f)
            logging.info(f"Saved pickled final_rating to: {final_rating_pickle_path}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_validation(self):
        """
        Initiates the data validation process
        """
        try:
            logging.info(f"{'='*20} Data Validation log started {'='*20}")
            self.preprocess_data()
            logging.info(f"{'='*20} Data Validation log completed {'='*20}\n\n")
        except Exception as e:
            raise AppException(e, sys) from e
