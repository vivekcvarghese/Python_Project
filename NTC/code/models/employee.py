from db import db
import json
import datetime

class EmployeeModel(db.Model):
    __tablename__="employee_details"
    id=db.Column(db.Integer,primary_key=True)
    empcode =db.Column(db.String(100))
    name=db.Column(db.String(100))
    doj=db.Column(db.Date)
    search=db.Column(db.String(100))
    client=db.Column(db.String(100))
    TASK=db.Column(db.String(100))
    created_on=db.Column(db.DateTime)
    created_by=db.Column(db.String(100))
    updated_on=db.Column(db.DateTime)
    updated_by=db.Column(db.String(100))
    deleted=db.Column(db.Boolean, default=False)

    def __init__(self,empcode,name,doj,search,client,TASK,created_on,created_by,updated_on,updated_by,deleted):
        self.empcode = empcode
        self.name = name
        self.doj = doj
        self.search = search
        self.client = client
        self.TASK = TASK
        self.created_on = created_on
        self.created_by = created_by
        self.updated_on = updated_on
        self.updated_by = updated_by
        self.deleted = deleted

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getAllEmployees(cls):
        return db.session.query(EmployeeModel).filter(EmployeeModel.deleted == 0).all() 

    @classmethod
    def getSingleEmployee(cls, empid):
        return db.session.query(EmployeeModel).filter(EmployeeModel.id == empid).all()

    @classmethod
    def setOutputFormat(cls, data):

        output = []
        for i in data:
            final = {}
            final["empcode"] = i.empcode
            final["name"] = i.name
            if i.doj == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i.doj.strftime("%Y-%m-%d")
            final["search"] = i.search
            final["client"] = i.client
            final["task"] = i.TASK
            final["id"] = i.id

            output.append(final)
            # print(output)
    
        output = json.dumps(output, indent = 4)   
        return output

    
       