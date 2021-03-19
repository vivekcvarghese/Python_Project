import MySQLdb
import json

from connection import connect_db
from flask import request
from flask_restful import Resource
from ldap3 import *




class User(Resource):

    def post(self):
        return {"login":"success", 
                    "name":"Vivek C Varghese", 
                    "description":""}
        jdata = request.get_json()
        username = jdata['username']
        pswd = jdata['password']
        AccountName = username.split("\\")[1]

        try:
            
            server = Server('ntcbpohyd.com')
            conn = Connection(server, user=username, password=pswd, auto_bind=True)
            conn.search('dc=ntcbpohyd,dc=com','(&(objectclass=person)(sAMAccountName ='+AccountName+'))', attributes=['displayName', 'description'])
            Name = str(conn.entries[0].displayName)
            description = str(conn.entries[0].description)
            
            return {"login":"success", 
                    "name":Name, 
                    "description":description}
        
        except:

            return {"login":"invalid credentials"}
        

