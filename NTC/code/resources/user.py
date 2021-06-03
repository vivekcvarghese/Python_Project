import json

from flask import request
from flask_restful import Resource
from ldap3 import *

class User(Resource):

    def post(self):
        
        jdata = request.get_json()
        username = jdata['username']
        pswd = jdata['password']
        

        if (username == "admin" and pswd =="admin"):
            return {"login":"success", 
                    "name":"ASHWINI KUMARI",
                    "account_name":"ES086", 
                    "description": "Admin",
                    "cn":"cn"}
        elif (username == "employee" and pswd =="employee"):
            return {"login":"success", 
                    "name":"KUKUTLA SRAVAN",
                    "account_name":"ER327", 
                    "description": "",
                    "cn":"cn"}
        else:
            return {"login":"invalid credentials"}


        try:
            AccountName = username.split("\\")[1]
            server = Server('ntcbpohyd.com')
            conn = Connection(server, user=username, password=pswd, auto_bind=True)
            conn.search('dc=ntcbpohyd,dc=com','(&(objectclass=person)(sAMAccountName ='+AccountName+'))', attributes=['displayName', 'description','distinguishedName'])
        
        except:

            return {"login":"invalid credentials"}
        
        Name = str(conn.entries[0].displayName)
        description = str(conn.entries[0].description)
        if (description == '[]'):
            description = ""

        data = conn.entries[0].entry_dn
        cn = data.split(',')[1].split('=')[1]
        
        return {"login":"success", 
                    "name":Name,
                    "account_name":AccountName, 
                    "description": description,
                    "cn":cn}