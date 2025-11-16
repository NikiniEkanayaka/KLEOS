import os
import sys
from KLEOS_Recommender.utils.util import read_yaml_file
from KLEOS_Recommender.exception.exception_handler import AppException
from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelRecommendationConfig
)
from KLEOS_Recommender.constant import *


class AppConfiguration:

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    # -------------------------------------------------------
    # DATA INGESTION CONFIG
    # -------------------------------------------------------
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            cfg = self.configs_info['data_ingestion_config']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            dataset_dir = cfg['dataset_dir']

            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, cfg['raw_data_dir'])
            ingested_dir = os.path.join(artifacts_dir, dataset_dir, cfg['ingested_dir'])

            response = DataIngestionConfig(
                dataset_download_url=cfg['dataset_download_url'],
                raw_data_dir=raw_data_dir,
                ingested_dir=ingested_dir
            )
            logging.info(f"Data Ingestion Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    # -------------------------------------------------------
    # DATA VALIDATION CONFIG
    # -------------------------------------------------------
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            vcfg = self.configs_info['data_validation_config']
            icfg = self.get_data_ingestion_config()

            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']

            books_csv_file = os.path.join(icfg.ingested_dir, vcfg['books_csv_file'])
            ratings_csv_file = os.path.join(icfg.ingested_dir, vcfg['ratings_csv_file'])
            clean_data_dir = os.path.join(artifacts_dir, vcfg['clean_data_dir'])
            serialized_objects_dir = os.path.join(artifacts_dir, vcfg['serialized_objects_dir'])

            response = DataValidationConfig(
                clean_data_dir=clean_data_dir,
                books_csv_file=books_csv_file,
                ratings_csv_file=ratings_csv_file,
                serialized_objects_dir=serialized_objects_dir
            )
            logging.info(f"Data Validation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    # -------------------------------------------------------
    # DATA TRANSFORMATION CONFIG
    # -------------------------------------------------------
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            tcfg = self.configs_info['data_transformation_config']
            vcfg = self.get_data_validation_config()

            clean_data_file = os.path.join(vcfg.clean_data_dir, "clean_data.csv")
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            transformed_data_dir = os.path.join(artifacts_dir, tcfg['transformed_data_dir'])

            response = DataTransformationConfig(
                clean_data_file_path=clean_data_file,
                transformed_data_dir=transformed_data_dir
            )
            logging.info(f"Data Transformation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    # -------------------------------------------------------
    # MODEL TRAINER CONFIG
    # -------------------------------------------------------
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            mcfg = self.configs_info['model_trainer_config']
            tcfg = self.get_data_transformation_config()
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']

            transformed_data_file_dir = os.path.join(
                tcfg.transformed_data_dir,
                "transformed_data.pkl"
            )
            trained_model_dir = os.path.join(artifacts_dir, mcfg['trained_model_dir'])

            response = ModelTrainerConfig(
                transformed_data_file_dir=transformed_data_file_dir,
                trained_model_dir=trained_model_dir,
                trained_model_name=mcfg['trained_model_name']
            )
            
            logging.info(f"Model Trainer Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    # -------------------------------------------------------
    # RECOMMENDATION CONFIG
    # -------------------------------------------------------
    def get_recommendation_config(self) -> ModelRecommendationConfig:
        try:
            vcfg = self.get_data_validation_config()
            mcfg = self.get_model_trainer_config()

            serialized_dir = vcfg.serialized_objects_dir

            response = ModelRecommendationConfig(
                book_name_serialized_objects=os.path.join(serialized_dir, "book_names.pkl"),
                book_pivot_serialized_objects=os.path.join(serialized_dir, "book_pivot.pkl"),
                final_rating_serialized_objects=os.path.join(serialized_dir, "final_rating.pkl"),
                trained_model_path=os.path.join(
                    mcfg.trained_model_dir,
                    mcfg.trained_model_name
                )
            )
            logging.info(f"Model Recommendation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
