from db import db
from sqlalchemy import func, desc

class DataModel(db.Model):
        __tablename__="data"
        id=db.Column(db.Integer,primary_key=True)
        Order_Number=db.Column(db.String(100))
        State=db.Column(db.String(100))
        Task_Name=db.Column(db.String(100))
        Task_Status=db.Column(db.String(100))
        SLAExpiration=db.Column(db.Date)
        created_date=db.Column(db.DateTime)


        def __init__(self,Order_Number,State,Task_Name,Task_Status,SLAExpiration,created_date):
                self.Order_Number = Order_Number
                self.State = State
                self.Task_Name = Task_Name
                self.Task_Status = Task_Status
                self.SLAExpiration = SLAExpiration
                self.created_date = created_date

        def save_to_db(self):
                
                db.session.add(self)
                db.session.commit()   

        @classmethod
        def RdData(cls, filters = [], dates = ""):
                date_conditions = []
                getTimelist = []
                time = []
                sla_conditions = []
                
                if dates == "":
                        date_conditions.append(DataModel.created_date == (db.session.query(func.max(DataModel.created_date))))
                        date_conditions.append(func.DATE(DataModel.created_date) == func.current_date())                
                else:
                        date_conditions.append(DataModel.created_date == (db.session.query(func.max(DataModel.created_date)).filter(func.DATE(DataModel.created_date) == dates)))

                if len(filters) != 0:
                        sla_conditions.append(DataModel.SLAExpiration.in_(filters))

                result = db.session.query(func.distinct(DataModel.Task_Name)).filter(DataModel.Task_Status == 'Available', *date_conditions, *sla_conditions).order_by(DataModel.Task_Name).all()
        

                query = db.session.query(func.distinct(func.time(DataModel.created_date))).filter(func.DATE(DataModel.created_date) == dates).order_by(desc(DataModel.created_date)).all()
                for i in query:
                        time.append(str(i[0]))
                tasks = []
                output = []
                dates = []

                for row in result:
                        tasks.append(row[0])
               
                result = db.session.query(func.distinct(DataModel.SLAExpiration)).filter(DataModel.Task_Status == 'Available', *date_conditions).all()  
                
                for row in result:
                        dt1 = row[0].strftime("%Y/%m/%d")
                        dates.append(dt1)

                for i in tasks:
                        result = db.session.query(DataModel.State, func.count(DataModel.State)).filter(DataModel.Task_Name == i, DataModel.Task_Status == 'Available', *date_conditions, *sla_conditions).group_by(DataModel.State).order_by(DataModel.State).all()
                        
                        state = {}
                        state["Task_Name"] = i
                        total_count = 0
                        for row in result:
                                total_count += row[1]
                                state[row[0]] = row[1]

                        state['Grand_total'] = total_count
                        output.append(state)
                
                dt = {}
                dt["SLAExpiration"]  = dates  
                dt["time"]  = time
                output.append(dt)
        
                return output