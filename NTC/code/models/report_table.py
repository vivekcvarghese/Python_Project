import json
from datetime import datetime

from sqlalchemy import func, desc
from db import db
from models.employee import EmployeeModel

class EmployeeRprtModel(db.Model):
    __tablename__="emp_report"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    account_name=db.Column(db.String(100))
    date_dt=db.Column(db.Date)
    order_number=db.Column(db.String(100))
    client=db.Column(db.String(100))
    task=db.Column(db.String(100))
    process=db.Column(db.String(100))
    state=db.Column(db.String(100))
    startTime=db.Column(db.Time)
    endTime=db.Column(db.Time)
    totalTime=db.Column(db.Integer)
    status=db.Column(db.String(100))
    TargetTime=db.Column(db.Float)
    DayWiseBand=db.Column(db.Float)
    Revenue=db.Column(db.Float)
    updated_time=db.Column(db.DateTime)
    created_date=db.Column(db.DateTime)
    
    def __init__(self,username,account_name,date_dt,order_number,client,task,process,state,startTime,endTime,totalTime,status,TargetTime,DayWiseBand,Revenue,updated_time,created_date):
                self.username = username
                self.account_name = account_name
                self.date_dt = date_dt
                self.order_number = order_number
                self.client = client
                self.task = task
                self.process = process
                self.state = state
                self.startTime = startTime
                self.endTime = endTime
                self.totalTime = totalTime
                self.status = status
                self.TargetTime = TargetTime
                self.DayWiseBand = DayWiseBand
                self.Revenue = Revenue
                self.updated_time = updated_time
                self.created_date = created_date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getDWB(cls,account_name,date):

        condition = [EmployeeRprtModel.account_name == account_name, EmployeeRprtModel.date_dt == date, EmployeeRprtModel.status == 'Completed/Submitted']
        result = db.session.query(func.sum(EmployeeRprtModel.TargetTime)).filter(*condition).first()
        
        if result[0] != None:
            dwb = (result[0]/1)*100
            dwb = round(dwb,1)
        else:
            dwb = 0

        db.session.query(EmployeeRprtModel).filter(*condition).update({EmployeeRprtModel.DayWiseBand : dwb})
        db.session.commit()

    @classmethod
    def fetchStatus(cls,date):
        date_condition = []

        if(date == 0):
            date_condition.append(EmployeeRprtModel.date_dt == func.current_date())
        else:
            date_condition.append(EmployeeRprtModel.date_dt == date)

        res = EmployeeModel.getAllEmployees()

        flag = None
        final_array = []
        for i in res:
            final = {}
            result = db.session.query(func.count(EmployeeRprtModel.order_number), func.sum(EmployeeRprtModel.TargetTime)*100, (func.sum(EmployeeRprtModel.totalTime)/480)*100, func.sum(EmployeeRprtModel.Revenue)).filter(EmployeeRprtModel.account_name == i.empcode, *date_condition).first()

            final["empcode"] = i.empcode
            final["name"] = i.name
            if i.doj == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i.doj.strftime("%d-%m-%Y")
            final["search"] = i.search
            final["client"] = i.client
            final["task"] = i.TASK
            
            if result[0] != 0:
                flag = 1
                final["order_count"] = result[0]
                final["productivity"] = float(round(result[1],1)) 
                final["utilization"] = float(round(result[2],2))
                final["revenue"] = float(round(result[3],2))
            else:
                final["order_count"] = 0
                final["productivity"] = 0
                final["utilization"] = 0
                final["revenue"] = 0
            
            final_array.append(final)

    
        if flag == None:
            final_array = []

        output = json.dumps(final_array, indent = 4)   

        return output

    @classmethod
    def myStatus(cls,date,end_date, account_name):
        date_condition = []

        date_condition.append(EmployeeRprtModel.date_dt.between(date, end_date))
        res = db.session.query(EmployeeRprtModel).filter(EmployeeRprtModel.account_name == account_name, *date_condition).order_by(desc(EmployeeRprtModel.date_dt)).all()
        return res

    @classmethod
    def singleStatus(cls, eid):

        return db.session.query(EmployeeRprtModel).filter(EmployeeRprtModel.id == eid).first()

