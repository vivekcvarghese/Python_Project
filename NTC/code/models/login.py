
from db import db
from sqlalchemy import func, desc

class LoginModel(db.Model):
        __tablename__="login"
        id=db.Column(db.Integer,primary_key=True)
        username=db.Column(db.String(100))
        password=db.Column(db.String(100))
        description=db.Column(db.String(100))
        name=db.Column(db.String(100))
        
        @classmethod
        def getcredentials(cls,username,password):

            res = db.session.query(LoginModel).filter(LoginModel.username == username, LoginModel.password == password).first()

            return res

