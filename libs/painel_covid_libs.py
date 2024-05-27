from dotenv import load_dotenv, find_dotenv
from storage.minio.minio_pc import minio
import pandas as pd
import os

load_dotenv(find_dotenv(".env"))


default_bucket_name = os.environ.get("DEFAULT_BUCKET")

def save_data(data:pd.DataFrame, file_name:str, source_type:str, bucket_name:str=None) -> None:
  
    if source_type == "minio":
        minio.put_object(data, file_name, source_type, default_bucket_name)
    elif source_type == "oci":
        pass
    else:
        pass
    
    
def read_data(file_name:str, source_type:str) -> pd.DataFrame:
    if source_type == "minio":
        minio.read_object(file_name, source_type)
    elif source_type == "oci":
        pass
    else:
        pass