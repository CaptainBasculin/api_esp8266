#This will store data and serve whenever needed.

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import csv
import requests
import datetime

bucket = 'data.csv'
app = Flask(__name__)
api = Api(app)
sugDim = False
sugEnable = True
dim = False

verif_key = "eBk6RcZ8DC33aFR81kwe"

class AllData(Resource):
    def get(self):
        key = request.args['key']
        data = pd.read_csv(bucket)
        data = data.to_dict()
        if key == verif_key:
            return {'data': data}, 200
        else:
            return{'message': 'unverified, fuck off'}, 401

    
class sensorUpdate(Resource):
    def get(self):
        key = request.args['key']
        if key == verif_key:
            temp = request.args.get('temp')
            co2 = request.args.get('co')
            ldr = request.args.get('ldr')
            psure = reqıests.args.get('psure')

            data = pd.read_csv(bucket)
            data = data.to_dict()

            if temp == None:
                req_form = "http://api.weatherapi.com/v1/current.json?key=66f1a059a7b24189b3701909222006&q=Istanbul&aqi=no"
                data['temperature'] = requests.get(req_form)['current']['temp_c']
            else:
                data['temperature'] = temp
            
            if (int(co)<35):
                data['monoxide'] = "Normal (" + str(co) + " ppm)"
            else if (int(co) < 100):
                data['monoxide'] = "Risky (" + str(co) + " ppm)"
            else:
                data['monoxide'] = "Dangerous (" + str(co) + " ppm)"
            
            if (str(ldr) == "HIGH"):
                sugDim = False
            else:
                sugDim = True
            
            if psure == None:
                data['pressure'] = random.randint(98,102)

            update = datetime.datetime.strptime(init_time, "%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame({
            'temperature': data['temperature'],
            'monoxide': data['monoxide'],
            'red': data['red'],
            'green': data['green'],
            'blue': data['blue'],
            'status': data['status'],
            'pressure': data['pressure']})

            new_data.to_csv(bucket, index = False)
            new_data.append('update': update)
            new_data.to_csv('',mode='a', index=False, header=False)
        else:
            return{'message': 'unverified, fuck off'}, 401
class commands(Resource):
    def get(self):




            
        
        
class RGBset(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        
        r = request.args['r']
        b = request.args['b']
        g = request.args['g']
        
        data = pd.read_csv(bucket)
        data = data.to_dict()
        print(data)
        print(data['red'])
        data['red'][0] = r
        data['blue'][0] = b
        data['green'][0] = g
        print(data)
        
        #temperature,monoxide,red,green,blue,status
        new_data = pd.DataFrame({
            'temperature': data['temperature'],
            'monoxide': data['monoxide'],
            'red': data['red'],
            'green': data['green'],
            'blue': data['blue'],
            'status': data['status'],
            'pressure': data['pressure']})
        
        new_data.to_csv(bucket, index = False)
            
        return {'data': new_data.to_dict()}, 200
        


api.add_resource(AllData, '/alldata')
api.add_resource(RGBset, '/rgb')

if __name__ == '__main__':
    app.run(host="10.200.81.243", port=727)  # run our Flask app