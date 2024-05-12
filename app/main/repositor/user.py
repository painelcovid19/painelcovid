from app.database.connection import DBConnectionHandler
from app.main.models.user import User
from sqlalchemy.orm.exc import NoResultFound


class UserRepositor:
    
    def create(self, email, password, full_name, username):
        with DBConnectionHandler() as db:
            try:
                user = User(email=email, password=password, 
                             full_name=full_name, username=username)
                db.session.add(user)
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception
            
    def select(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).all()
                return data
            except Exception as ex:
                db.session.rollback()
                raise ex

    def select_by_id(self, id:int):
        with DBConnectionHandler() as db:
            try:
                user = db.session.query(User).filter(User.id==id).first()
                return user
            except NoResultFound:
                return None
            except Exception as exception:
                raise exception
        
    def select_by_email(self, email):
        with DBConnectionHandler() as db:
            try:
                user = db.session.query(User).filter(User.email==email).first()
                return user
            except NoResultFound:
                return None
            except Exception as ex:
                db.session.rollback()
                raise ex
        
    def select_by_username(self, username):
        with DBConnectionHandler() as db:
            try:
                user = db.session.query(User).filter(User.username==username).first()
                return user
            except NoResultFound:
                return None
            except Exception as ex:
                db.session.rollback()
                raise ex
                
    def update(self, id:int, full_name):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.id==id).update({
                    "full_name":full_name 
                })
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                raise ex
            
    def delete(self, id:int):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.id==id).delete()
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                raise ex
    def delete_by_username(self, username:str):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.username==username).delete()
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                raise ex    
    