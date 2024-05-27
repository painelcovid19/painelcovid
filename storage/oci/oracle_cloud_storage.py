import oci
from oci.object_storage import ObjectStorageClient
from oci.object_storage.models.create_bucket_details import CreateBucketDetails
from dotenv import load_dotenv, find_dotenv
import os
from storage.storage import PainelCovidStorage
import pandas as pd

class PainelCovidStorageOCI(PainelCovidStorage):
    def __init__(self, acess_key: str, secret_key: str, default_bocket: str, endpont: str) -> None:
        super().__init__(acess_key, secret_key, default_bocket, endpont)
    
    def __connect(self) -> object:
        
       connection = oci.config.from_file()
    
    def create_bucket(self):
        pass
    
    def list_buckets(self):
        return ""
    
    def put_object(self, data:pd.DataFrame, file_name:str, source_data:str, bucket_name:str=None) -> None:
        
        bucket = ""
        if bucket_name:
            bucket = bucket_name 
        else:
            bucket = self.__DEFAULT_BUCKET
        
        base_path = self._get_base_path(source_data, bucket)
        data.to_csv(
            f"{base_path}/{file_name}",
            storage_options={
                "config": "~/.oci/config"
            },
            index=False
        )
    
    def read_object(self, file_name:str, source_data:str, bucket_name:str=None):
        
        bucket = ""
        if bucket_name:
            bucket = bucket_name 
        else:
            bucket = self.__DEFAULT_BUCKET
        
        base_path = self._get_base_path(source_data, bucket)
        
        df = pd.read_csv(
        f"{base_path}/{file_name}",
        storage_options={
           "config": "~/.oci/config"
                }
            )
        return df 
    
    
if __name__ == "__main__":
    
    load_dotenv(find_dotenv())

    config = oci.config.from_file()

    identity = oci.identity.IdentityClient(config)
    user = identity.get_user(config["user"])

    # configurating object storage

    s3 = ObjectStorageClient(config)

    # print(s3.get_namespace().data)
    # print(user.data)

    namesapec = os.environ.get("OCI_NAMESPACE")
    compartment_id = os.environ.get("OCI_COMPARTMENT_ID")

    all_buckets = s3.list_buckets(namesapec, compartment_id)

    result = s3.create_bucket(
        namespace_name=namesapec,
        create_bucket_details=CreateBucketDetails(
            name="new_bucket",
            compartment_id=compartment_id
        )
    )

    print(all_buckets.data)
    print(result)

    s3.put_object()

