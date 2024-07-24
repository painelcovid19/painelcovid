import pandas as pd

class PainelCovidStorage:
    def __init__(self, acess_key:str=None, secret_key:str= None, default_bocket:str="painelcovid", endpont:str=None) -> None:
        self._ACESS_KEY = acess_key
        self._SECRET_KEY = secret_key
        self._ENDPOINT = endpont
        self._DEFAULT_BUCKET = default_bocket
    
    def __connect(self) -> object:
       pass
    
    def _get_base_path(self, source: str, bucket_name:str)-> str:
        default_source_data = ""
        
        if source == "local":
            default_source_data = "./data"
        elif source == "minio":
            default_source_data = f"s3://{bucket_name}/data" 
        else:
            default_source_data = f"oci://{bucket_name}/data"
            
        return default_source_data
    def create_bucket(self):
        pass
    
    def list_buckets(self):
        pass
    
    def put_object(self, data:pd.DataFrame, file_name:str, source_data:str, bucket_name:str=None) -> None:
        pass
    
    def read_object(self, file_name:str, source_data:str, bucket_name:str=None):
        pass