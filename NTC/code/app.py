from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from getdata import GetData
from flask_cors import CORS

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
CORS(app)
api.add_resource(GetData, '/getfile')

if __name__ == '__main__':
    app.run(debug=True)  