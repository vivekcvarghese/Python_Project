import json
from db import db
from sqlalchemy import func, desc

class RoleModel(db.Model):
        __tablename__="role"
        id=db.Column(db.Integer,primary_key=True)
        role=db.Column(db.String(100))
        resources=db.Column(db.String(500))
        created_on=db.Column(db.DateTime)
        created_by=db.Column(db.String(100))
        updated_on=db.Column(db.DateTime)
        updated_by=db.Column(db.String(100))
        deleted=db.Column(db.Boolean, default=False)

        def __init__(self,role,resources,created_on,created_by,updated_on,updated_by,deleted):
            self.role = role
            self.resources = resources
            self.created_on = created_on
            self.created_by = created_by
            self.updated_on = updated_on
            self.updated_by = updated_by
            self.deleted = deleted

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()   
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def getrolelist(cls):
            res = db.session.query(RoleModel.id, RoleModel.role, RoleModel.resources).all()
            output = []
            for i in res:
            
                final = {}
                final["id"] = i[0]
                final["role"] = i[1]
                final["resources"] = i[2].split(",")
                output.append(final)
            
    
            output = json.dumps(output, indent = 4)   
            return output

        

