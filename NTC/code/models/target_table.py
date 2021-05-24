from sqlalchemy import func
from db import db

class TargetModel(db.Model):
    __tablename__="target_table"
    id=db.Column(db.Integer,primary_key=True)
    Client=db.Column(db.String(100))
    Task=db.Column(db.String(100))
    Process=db.Column(db.String(100))
    Time=db.Column(db.Float)
    band1=db.Column(db.Integer)
    band2=db.Column(db.Integer)
    band3=db.Column(db.Integer)
    price=db.Column(db.Float)
    

    @classmethod
    def GetBandValue(cls, process):

        return db.session.query(TargetModel.band1, TargetModel.price).filter(TargetModel.Process == process).first()