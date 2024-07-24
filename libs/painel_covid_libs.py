from dotenv import load_dotenv, find_dotenv
from storage.minio.minio_pc import minio
from storage.oci.oracle_cloud_storage import PainelCovidStorageOCI
import pandas as pd
import os

load_dotenv(find_dotenv(".env"))


default_bucket_name = os.environ.get("DEFAULT_BUCKET")

def save_data(data:pd.DataFrame, file_name:str, source_type:str, bucket_name:str=None) -> None:
  
    if source_type == "minio":
        minio.put_object(data, file_name, source_type, default_bucket_name)
    elif source_type == "oci":
        s3 = PainelCovidStorageOCI()
        s3.put_object(data, file_name, source_type, default_bucket_name)
    else:
        pass
    
    
def read_data(file_name:str, source_type:str) -> pd.DataFrame:
    if source_type == "minio":
        minio.read_object(file_name, source_type)
    elif source_type == "oci":
        oci = PainelCovidStorageOCI()
        dataframe = oci.read_object(file_name, source_type, default_bucket_name)
        return dataframe
    else:
        pass