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

    def __init__(self,Client,Task,Process,Time,band1,band2,band3,price):
        self.Client = Client
        self.Task = Task
        self.Process = Process
        self.Time = Time
        self.band1 = band1
        self.band2 = band2
        self.band3 = band3
        self.price = price
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()   
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def GetBandValue(cls, process):

        return db.session.query(TargetModel.band1, TargetModel.price).filter(TargetModel.Process == process).first()


    @classmethod
    def GetTargetTable(cls, client):

        return db.session.query(TargetModel).filter(TargetModel.Client == client).all()


    @classmethod
    def GetSingleTarget(cls, id):

        return db.session.query(TargetModel).filter(TargetModel.id == id).all()


    @classmethod
    def setOutputFormat(cls, res):
        result=[
           {
               "id":i.id,
               "client":i.Client,
               "task":i.Task,
               "process":i.Process,
               "time":i.Time,
               "band1":i.band1,
               "band2":i.band2,
               "band3":i.band3,
               "price":i.price
           } for i in res
        ]

        return result