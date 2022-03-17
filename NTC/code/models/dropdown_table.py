from sqlalchemy import func
from db import db

# test
class DropdownModel(db.Model):
    __tablename__="task_dropdown"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    value=db.Column(db.String(1000))
    
    @classmethod
    def getAll(cls):
        return db.session.query(DropdownModel).all()