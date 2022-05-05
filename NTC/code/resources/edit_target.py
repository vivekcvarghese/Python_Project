from models.target_table import TargetModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.dropdown_table import DropdownModel
from models.employee import EmployeeModel
from db import db

class SingleTarget(Resource):
    @jwt_required()
    def get(self,id):

        res = TargetModel.GetSingleTarget(id)
        return TargetModel.setOutputFormat(res)

    @jwt_required()
    def put(self,id):

        data = request.get_json()
        try:
            res=db.session.query(TargetModel).filter(TargetModel.id == id).first()

            res.Time = data["Time"]
            res.band1 = data["band1"]
            res.band2 = data["band2"]
            res.band3 = data["band3"]
            res.price = data["price"]
            res.save_to_db()
            return {"response":"Success"}

        except:
            return {"response":"Error"}


    @jwt_required()
    def delete(self,id):
        # try:
            res=db.session.query(TargetModel).filter(TargetModel.id == id).first()
            emp = db.session.query(EmployeeModel).filter(EmployeeModel.client == res.Client, EmployeeModel.TASK == res.Task,\
                EmployeeModel.process == res.Process, EmployeeModel.state == res.State, EmployeeModel.county == res.County).first()
            if emp:
                return {"response":"Employee with this target value exists"}
            res.delete()

            chk = db.session.query(TargetModel).filter(TargetModel.Client == res.Client, TargetModel.Task == res.Task, TargetModel.Process == res.Process).first()
            if chk:
                return {"response":"Success"}

            #fetch array from dropdown table
            title = res.Client+res.Task
            dp = db.session.query(DropdownModel).filter(DropdownModel.title == title).first()
            arr = (dp.value).split(",")
            filtered = filter(lambda i: i != res.Process, arr)
            filtered= list(filtered)

            if len(filtered) == 0:
                dp.remove()
                dp1 = db.session.query(DropdownModel).filter(DropdownModel.title == res.Client).first()
                arr1 = (dp1.value).split(",")
                filtered1 = filter(lambda i: i != res.Task, arr1)
                filtered1= list(filtered1)
                if len(filtered1) == 0:
                    dp1.remove()
                    dp2 = db.session.query(DropdownModel).filter(DropdownModel.title == "Client").first()
                    arr2 = (dp2.value).split(",")
                    filtered2 = filter(lambda i: i != res.Client, arr2)
                    filtered2= list(filtered2)
                    dp2.value = ",".join(filtered2)
                    dp2.save()

                else:
                    dp1.value = ",".join(filtered1)
                    dp1.save()

            else:
                dp.value = ",".join(filtered)
                dp.save()

        
            return {"response":"Success"}


        # except:
        #     return {"response":"Failed"}


    @jwt_required()
    def post(self):
        data = request.get_json()
        #check data already exists
        check = db.session.query(TargetModel).filter(TargetModel.State == data["State"], TargetModel.County == data["County"], TargetModel.Client == data["Client"], TargetModel.Task == data["Task"], TargetModel.Process == data["Process"]).first()
        if check:
            return {"response":"Data already exists!"}
        
        target = TargetModel(data["Client"], data["Task"], data["Process"],data["State"], data["County"], data["Time"], data["band1"], data["band2"], data["band3"], data["price"])
        target.save_to_db()

        #insert to dropdown table\
        client = db.session.query(DropdownModel).filter(DropdownModel.title == "Client").first()
        client_arr = client.value.split(",")
        if data["Client"] in client_arr:
            task = db.session.query(DropdownModel).filter(DropdownModel.title == data["Client"]).first()
            task_arr = task.value.split(",")
            if data["Task"] in task_arr:
                tmp = data["Client"]+data["Task"]
                process = db.session.query(DropdownModel).filter(DropdownModel.title == tmp).first()
                process_arr = process.value.split(",")
                if data["Process"] not in process_arr:
        
                    process_arr.append(data["Process"])
                    process.value = ",".join(process_arr)
                    process.save()

            else:
                task_arr.append(data["Task"])
                task.value =",".join(task_arr)
                task.save()
                tmp = data["Client"]+data["Task"]
                new_rcrd = DropdownModel(tmp,data["Process"])
                new_rcrd.save()
        else:
            client_arr.append(data["Client"])
            client.value = ",".join(client_arr)
            client.save()
            new_rcrd = DropdownModel(data["Client"],data["Task"])
            tmp = data["Client"]+data["Task"]
            new_rcrd1 = DropdownModel(tmp,data["Process"])
            new_rcrd.save()
            new_rcrd1.save()


        return {"response":"Success"}
       



class TargetFilter(Resource):
    @jwt_required()
    def get(self,client):

        res = TargetModel.GetTargetTable(client)
        return TargetModel.setOutputFormat(res)

    @jwt_required()
    def post(self):

        data = request.get_json()["inputs"]
        condition = [TargetModel.Client == data["client"],TargetModel.Task == data["task"],TargetModel.Process == data["process"]]
        state=[]
        county=[]
        if data["state"] == "":
            res = db.session.query(TargetModel.State).filter(*condition).all()
            state = [i.State for i in res]
            

            result = {
                "state":list(set(state))    
            }
           
        else:
            res1 = db.session.query(TargetModel.State).filter(*condition).all()
            state = [i.State for i in res1]
            res = db.session.query(TargetModel.County).filter(*condition, TargetModel.State == data["state"]).all()
            county = [i.County for i in res]
            result = {
                "state":list(set(state)) ,
                "county":list(set(county))    
            }

        return result
            