import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.config.configuration import AppConfiguration
from KLEOS_Recommender.exception.exception_handler import AppException


class ModelTrainer:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def train(self):
        try:
            # Loading pivot data
            pivot_file = self.model_trainer_config.transformed_data_file_dir


            logging.info(f"Loading pivot data from: {pivot_file}")

            book_pivot = pickle.load(open(pivot_file, 'rb'))
            book_sparse = csr_matrix(book_pivot)

            # Training model
            model = NearestNeighbors(metric='cosine', algorithm='brute')
            model.fit(book_sparse)

            # Saving model object
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            model_file = os.path.join(
                self.model_trainer_config.trained_model_dir,
                self.model_trainer_config.trained_model_name
            )

            pickle.dump(model, open(model_file, 'wb'))
            logging.info(f"Saved trained model to: {model_file}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_model_trainer(self):
        try:
            logging.info(f"{'='*20} Model Trainer log started. {'='*20}")
            self.train()
            logging.info(f"{'='*20} Model Trainer log completed. {'='*20}\n\n")
        except Exception as e:
            raise AppException(e, sys) from e
