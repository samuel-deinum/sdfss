from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify

import pandas as pd
from pandas import DataFrame
import datetime
from dateutil.parser import parse

from SDFSS import sdfss

app = Flask(__name__)
api = Api(app)

class sdfssAPI(Resource):
    def get(self,mTemp):

        t = mTemp - 273.15
        date = datetime.datetime.now()
        res = sdfss(t, date.year, date.month, date.day, date.hour, 'B')

        elec = res[0]

        if elec>1:
            system = "E"
        else:
            system = "NG"


            
        return system

class mainAPI(Resource):
    def post(self,id):
        #ADD ID to DATABASE
        print(id)
        return id

api.add_resource(sdfssAPI, '/SDFSS/<float:mTemp>')
api.add_resource(mainAPI, '/MAIN/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

