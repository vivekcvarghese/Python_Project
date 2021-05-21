from db import db

class EmployeeModel(db.Model):
    __tablename__="employee"
    id=db.Column(db.Integer,primary_key=True)
    empcode =db.Column(db.String(100))
    name=db.Column(db.String(100))
    doj=db.Column(db.Date)
    search=db.Column(db.String(100))
    client=db.Column(db.String(100))
    TASK=db.Column(db.String(100))
    

    @classmethod
    def getAllEmployees(cls):

        detail = db.session.query(EmployeeModel).all()
        return detail

