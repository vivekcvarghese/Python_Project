
from db import db
from sqlalchemy import func, desc
from flask_bcrypt import generate_password_hash, check_password_hash


class LoginModel(db.Model):
        __tablename__="login"
        id=db.Column(db.Integer,primary_key=True)
        username=db.Column(db.String(100))
        password=db.Column(db.String(100))
        # description=db.Column(db.String(100))
        name=db.Column(db.String(100))


        def __init__(self,username,password,name):

            self.username=username
            self.password =generate_password_hash(password).decode()
            self.name=name

        def add_user(self):
            db.session.add(self)
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def getcredentials(cls,username,password):

            res = db.session.query(LoginModel).filter(LoginModel.username == func.binary(username)).first()
            if res != None:
                login = res.check_password(password)
                if login:
                    return res
            return None

        def check_password(self, password):
            return check_password_hash(self.password, password)


        def changePassword(username, password):
            res = db.session.query(LoginModel).filter(LoginModel.username == username).first()
            res.password = generate_password_hash(password).decode()
            res.add_user()
            return