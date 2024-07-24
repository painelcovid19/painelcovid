from app.database.connection import DBConnectionHandler
from app.main.models.user import User
from sqlalchemy.orm.exc import NoResultFound
from app.main._supabase import supabase

class UserRepositor:
    
    def __init__(self, table_name) -> None:
        self.__TABLE_NAME= table_name
    
    def create(self, email, password, full_name, username):
       supabase.table(self.__TABLE_NAME).insert({
           "full_name": full_name,
           "email": email,
           "username": username,
           "password": password
       }).execute()
            
    def select(self):
        response = supabase.table(self.__TABLE_NAME).select("*").execute()
        return response.data

    def select_by_id(self, id:int):
        user_response = supabase.table(self.__TABLE_NAME).select("*").eq("id", id).execute()
        return user_response.data
        
    def select_by_email(self, email):
        user_response = supabase.table(self.__TABLE_NAME).select("*").eq("email", email).execute()
        return user_response.data
        
    def select_by_username(self, username):
        with DBConnectionHandler() as db:
            try:
                user_response = supabase.table(self.__TABLE_NAME).select("*").eq("username", username).execute()
                print(user_response.data)
                print(type(user_response.data))
                return user_response.data
            except NoResultFound:
                return None
            except Exception as ex:
                db.session.rollback()
                raise ex
                
    def update(self, id:int, data:dict):
        with DBConnectionHandler() as db:
            try:
                user_response = supabase.table(self.__TABLE_NAME).update(data).eq("id", id).execute()
                return user_response.data
            except Exception as ex:
                db.session.rollback()
                raise ex
            
    def delete(self, id:int):
        with DBConnectionHandler() as db:
            try:
                user_response = supabase.table(self.__TABLE_NAME).delete().eq("id", id).execute()
                return user_response.data
            except Exception as ex:
                db.session.rollback()
                raise ex
    def delete_by_username(self, username:str):
        with DBConnectionHandler() as db:
            try:
                user_response = supabase.table(self.__TABLE_NAME).delete().eq("username", username).execute()
                return user_response
            except Exception as ex:
                db.session.rollback()
                raise ex    
    