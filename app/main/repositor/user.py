from app.main.supabase import supabase
from datetime import datetime
import json

class UserRepositor():
    
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        pass
    def insert(self, name:str, email:str, password:str):
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        response = supabase.table(self.table_name).insert(user).execute()
        return response.data

    
    def select_all(self) -> list[dict]:
        response  = supabase.table(self.table_name).select("*").execute()
        return response.data
    
    def select_by_id(self, id) -> list[dict]:
        response = supabase.table(self.table_name).select("*").eq("id", f"{id}").execute()
        return response.data
    
    def select_by_email(self, email):
        response = supabase.table(self.table_name).select("*").eq("email", f"{email}").execute()
        return response.data
    
    def delete(self, id):
        response = supabase.table(self.table_name).delete().eq("id", id).execute()
        return response
        
    
    def update(self, id, data:dict):
        # data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        # data = json.dumps(data)
        response = supabase.table(self.table_name).update(data).eq("id",id).execute()
        return response
    
    