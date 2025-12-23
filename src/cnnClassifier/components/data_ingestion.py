import os
import requests
import zipfile
from src.cnnClassifier import logger
from src.cnnClassifier.utils.common import get_size
from src.cnnClassifier.entity.config_entity import DataIngestionConfig 
from pathlib import Path 
import urllib3


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                logger.info(f"Downloading file from {self.config.source_URL}")
                response = requests.get(self.config.source_URL, stream=True, verify=True)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                # Save the file
                with open(self.config.local_data_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"File downloaded successfully: {self.config.local_data_file}")
                logger.info(f"File size: {get_size(Path(self.config.local_data_file))}")
                
            except requests.exceptions.SSLError as e:
                logger.warning(f"SSL Certificate verification failed. Retrying with verification disabled: {e}")
                try:
                    # Disable SSL warnings
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    
                    # Retry with SSL verification disabled
                    response = requests.get(self.config.source_URL, stream=True, verify=False)
                    response.raise_for_status()
                    
                    # Save the file
                    with open(self.config.local_data_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    logger.info(f"File downloaded successfully with SSL verification disabled: {self.config.local_data_file}")
                    logger.info(f"File size: {get_size(Path(self.config.local_data_file))}")
                except Exception as e2:
                    logger.error(f"Failed to download file even with SSL verification disabled: {e2}")
                    raise e2
                    
            except Exception as e:
                logger.error(f"Failed to download file: {e}")
                raise e
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  


    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
