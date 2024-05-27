
from storage.storage import PainelCovidStorage
import pandas as pd
import os


class PainelCovidStorageLocal(PainelCovidStorage):
    def __init__(self, acess_key: str, secret_key: str, default_bocket: str, endpont: str) -> None:
        super().__init__(acess_key, secret_key, default_bocket, endpont)
    
    def __connect(self) -> object:
       pass
    
    def create_bucket(self):
        pass
    
    def list_buckets(self):
        pass
    
    def put_object(self, data:pd.DataFrame, file_name:str, source_data:str, bucket_name:str=None) -> None:
        pass
        
    
    def read_object(self, file_name:str, source_data:str, bucket_name:str=None):
        pass