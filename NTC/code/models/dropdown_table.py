from sqlalchemy import func
from db import db

class DropdownModel(db.Model):
    __tablename__="task_dropdown"
    Client=db.Column(db.String(100))
    ASK=db.Column(db.String(100))
    DT=db.Column(db.String(100))
    Sp=db.Column(db.String(100))
    TW=db.Column(db.String(100))
    NonProd=db.Column(db.String(100))
    ASKOE=db.Column(db.String(100))
    ASKTax=db.Column(db.String(100))
    ASKTyping=db.Column(db.String(100))
    ASKSearch=db.Column(db.String(100))
    ASKExam=db.Column(db.String(100))
    DTBilling=db.Column(db.String(100))
    DTDecorating=db.Column(db.String(100))
    DTExam=db.Column(db.String(100))
    DTTXExceptions=db.Column(db.String(100))
    DTHOA=db.Column(db.String(100))
    DTSearch=db.Column(db.String(100))
    SpSearch=db.Column(db.String(100))
    DTTyping=db.Column(db.String(100))
    DTVMQC=db.Column(db.String(100))
    TWSearch=db.Column(db.String(100))
    TWTyping=db.Column(db.String(100))
    Status=db.Column(db.String(100))
    States=db.Column(db.String(100),primary_key=True)

    @classmethod
    def getTitles(cls):
        title = []
        for column in DropdownModel.__table__.columns:
            title.append(column.key)
        return title

    @classmethod
    def getAll(cls):
        return db.session.query(DropdownModel).all()