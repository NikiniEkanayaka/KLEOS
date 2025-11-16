from KLEOS_Recommender.components.stage_00_data_ingestion import DataIngestion
from KLEOS_Recommender.components.stage_01_data_validation import DataValidation
# from KLEOS_Recommender.components.stage_02_data_transformation import DataTransformation
# from KLEOS_Recommender.components.stage_03_model_trainer import ModelTrainer

from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.exception.exception_handler import AppException
import sys


class TrainingPipeline:

    def __init__(self):
        try:
            logging.info("Initializing TrainingPipeline...")

            self.data_ingestion = DataIngestion()
            self.data_validation = DataValidation()
            # self.data_transformation = DataTransformation()
            # self.model_trainer = ModelTrainer()

            logging.info("TrainingPipeline initialization complete.")

        except Exception as e:
            raise AppException(e, sys) from e

    def start_training_pipeline(self):
        """
        Runs the full model training pipeline in order.
        """
        try:
            logging.info("====== Training Pipeline Started ======")

            # 1️⃣ Data Ingestion
            logging.info("Starting: Data Ingestion...")
            ingestion_output = self.data_ingestion.initiate_data_ingestion()

            # 2️⃣ Data Validation
            logging.info("Starting: Data Validation...")
            validation_output = self.data_validation.initiate_data_validation()

            # # 3️⃣ Data Transformation
            # logging.info("Starting: Data Transformation...")
            # transformation_output = self.data_transformation.initiate_data_transformation()

            # # 4️⃣ Model Training
            # logging.info("Starting: Model Training...")
            # model_output = self.model_trainer.initiate_model_trainer()

            logging.info("====== Training Pipeline Completed Successfully ======")

            return {
                "ingestion": ingestion_output,
                "validation": validation_output,
                # "transformation": transformation_output,
                # "model": model_output
            }

        except Exception as e:
            logging.error("Training Pipeline FAILED.")
            raise AppException(e, sys) from e
