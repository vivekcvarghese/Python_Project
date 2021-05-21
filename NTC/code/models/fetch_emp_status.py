import json
import datetime

from sqlalchemy import func
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
    created_date=db.Column(db.DateTime)

    def __init__(self,username,account_name,date_dt,order_number,client,task,process,state,startTime,endTime,totalTime,status,TargetTime,DayWiseBand,Revenue):
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
        
            final["emp_code"] = i.empcode
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
                print(result)
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




