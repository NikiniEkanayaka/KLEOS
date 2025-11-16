import os
import sys
import pickle
import pandas as pd
from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.config.configuration import AppConfiguration
from KLEOS_Recommender.exception.exception_handler import AppException


class DataTransformation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformer(self):
        try:
            df = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            
            # Create a pivot table: rows=title, columns=user_id, values=rating
            book_pivot = df.pivot_table(index='title', columns='user_id', values='rating')
            logging.info(f"Shape of book pivot table: {book_pivot.shape}")
            book_pivot.fillna(0, inplace=True)

            # Save pivot table
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            transformed_data_path = os.path.join(self.data_transformation_config.transformed_data_dir, "transformed_data.pkl")
            with open(transformed_data_path, 'wb') as f:
                pickle.dump(book_pivot, f)
            logging.info(f"Saved pivot table data to {transformed_data_path}")

            # Save book names for web app
            book_names = book_pivot.index
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)

            book_names_path = os.path.join(self.data_validation_config.serialized_objects_dir, "book_names.pkl")
            with open(book_names_path, 'wb') as f:
                pickle.dump(book_names, f)
            logging.info(f"Saved book names object to {book_names_path}")

            # Save book pivot for web app
            book_pivot_path = os.path.join(self.data_validation_config.serialized_objects_dir, "book_pivot.pkl")
            with open(book_pivot_path, 'wb') as f:
                pickle.dump(book_pivot, f)
            logging.info(f"Saved book pivot object to {book_pivot_path}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20} Data Transformation log started {'='*20}")
            self.get_data_transformer()
            logging.info(f"{'='*20} Data Transformation log completed {'='*20}\n\n")
        except Exception as e:
            raise AppException(e, sys) from e
