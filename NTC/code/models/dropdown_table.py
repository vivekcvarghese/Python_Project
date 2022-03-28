from sqlalchemy import func
from db import db

# test
class DropdownModel(db.Model):
    __tablename__="task_dropdown"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    value=db.Column(db.String(1000))

    def __init__(self,title,value):
        self.title = title
        self.value = value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def getAll(cls):
        return db.session.query(DropdownModel).all()