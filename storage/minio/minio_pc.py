from minio import Minio
from minio.error import S3Error
import os
from storage.storage import PainelCovidStorage
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class PainelCovidStorageMinio(PainelCovidStorage):
    
    def __init__(self, acess_key:str, secret_key:str, default_bocket:str, endpont:str) -> None:
        super().__init__(acess_key,secret_key, default_bocket,  endpont)
        
        
    def __connect(self) -> Minio:
        client = Minio(
            endpoint=self.__ENDPOINT,
            access_key=self.__ACESS_KEY,
            secret_key= self.__SECRET_KEY
        )
        return client
    
    def creat_bucket(self) -> None:
        pass
    
    def list_backets(self) -> None:
        pass
    
    def put_object(self, data:pd.DataFrame, file_name:str, source_data:str="minio", bucket_name:str=None) -> None:
        
        bucket = ""
        if bucket_name:
            bucket = bucket_name 
        else:
            bucket = self._DEFAULT_BUCKET
        base_path = self._get_base_path(source_data, bucket)
        data.to_csv(
            f"{base_path}/{file_name}",
            storage_options={
                "key": self._ACESS_KEY,
                "secret": self._SECRET_KEY,
                "client_kwargs": {"endpoint_url": f"{self._ENDPOINT}"}
            },
            index=False
        )
    
    def read_object(self, file_name:str, source_data:str="minio", bucket_name:str=None):
        
        bucket = ""
        if bucket_name:
            bucket = bucket_name 
        else:
            bucket = self._DEFAULT_BUCKET
            
        base_path = self._get_base_path(source_data, bucket)
        df = pd.read_csv(
        f"{base_path}/{file_name}",
        storage_options={
            "key": self._ACESS_KEY,
            "secret": self._SECRET_KEY,
            "client_kwargs": {"endpoint_url": f"{self._ENDPOINT}"}
                }
            )
        
        return df 

acesse_key = os.environ.get("MINIO_ACESS_KEY")
secret_key = os.environ.get("MINIO_SECRET_KEY")
minio = PainelCovidStorageMinio(acesse_key, secret_key, "painelcovid", "http://localhost:9000")

if __name__ == "__main__":
    from dotenv import load_dotenv
    from pyogrio import set_gdal_config_options
    import pandas as pd
    import geopandas as gpd
    load_dotenv()
    
    acesse_key = os.environ.get("MINIO_ACESS_KEY")
    secret_key = os.environ.get("MINIO_SECRET_KEY")
    minio = PainelCovidStorageMinio(acesse_key, secret_key, "painelcovid", "http://localhost:9000")
    
    # criating a sample dataframe
    data_persons = pd.DataFrame({
        "name": [
            "José Dembo", 
            "Mateus Zua",
            "Domingos Pedro",
            "Maria Chipala"
        ], 
        "age": [25, 24, 27, 28], 
        "gender": ["M", "M", "M", "F"]
    })
    
    # minio.put_object(data_persons, "persons.csv")
    
    persons_df = minio.read_object("persons.csv")
    print(persons_df.columns)
    
    
    # set_gdal_config_options(
    #         {
    #             "AWS_ACCESS_KEY_ID": acesse_key,
    #             "AWS_SECRET_ACCESS_KEY": secret_key,
    #             "AWS_NO_SIGN_REQUEST": True,
    #             "AWS_S3_ENDPOINT": "localhost:9000",
    #             "AWS_HTTPS": "NO",
    #             "AWS_VIRTUAL_HOSTING": "FALSE"
    #         }
    #     )

    # gdf = gpd.read_file('s3://painelcovid/CE_Municipios_2020.shp', engine='pyogrio')
    
    # print(gdf.comluns)