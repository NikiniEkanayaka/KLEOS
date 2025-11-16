import os
import sys
import urllib.request
import zipfile

from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.exception.exception_handler import AppException
from KLEOS_Recommender.config.configuration import AppConfiguration


class DataIngestion:

    def __init__(self, app_config=AppConfiguration()):
        """
        DataIngestion Initialization
        """
        try:
            logging.info(f"{'='*20} Data Ingestion log started. {'='*20}")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def download_data(self):
        """
        Fetch the data from the URL
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(zip_download_dir, exist_ok=True)

            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)

            logging.info(f"Downloading data from {dataset_url} to {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Successfully downloaded {zip_file_path}")

            return zip_file_path

        except Exception as e:
            raise AppException(e, sys) from e

    def extract_zip_file(self, zip_file_path: str):
        """
        Extracts ZIP file into the ingestion folder
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(ingested_dir)

            logging.info(f"Extracted {zip_file_path} to {ingested_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path)
            logging.info(f"{'='*20} Data Ingestion Completed {'='*20}\n")

        except Exception as e:
            raise AppException(e, sys) from e
