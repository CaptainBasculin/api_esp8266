#This will store data and serve whenever needed.

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import csv
import requests
import datetime
import random
import json

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
            

class RGBset(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        
        rawRGB = str(request.args['input'])
        #find two spaces
        counter = 0
        for i in rawRGB:
            if i == ' ':
                counter = counter + 1
            else: 
                if counter == 0:




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
            
        #return {'data': new_data.to_dict()}, 200
   
class sensorUpdate(Resource):
    def get(self):
        key = request.args['key']
        if key == verif_key:
            temp = request.args.get('temp')
            co2 = request.args.get('co')
            ldr = request.args.get('ldr')
            psure = request.args.get('psure')

            data = pd.read_csv(bucket)
            data = data.to_dict()

            if temp == None:
                req_form = "http://api.weatherapi.com/v1/current.json?key=66f1a059a7b24189b3701909222006&q=Istanbul&aqi=no"
                data['temperature'] = requests.get(req_form).json()['current']['temp_c'] + round(((random.random()*2)*2-1),2)
            else:
                data['temperature'] = temp
            
            if (int(co2)<35):
                data['monoxide'] = "Normal (" + str(co2) + " ppm)"
            elif (int(co2) < 100):
                data['monoxide'] = "Risky (" + str(co2) + " ppm)"
            else:
                data['monoxide'] = "Dangerous (" + str(co2) + " ppm)"
            
            if (str(ldr) == 0):
                sugDim = False
            else:
                sugDim = True
            
            if psure == None:
                data['pressure'] = random.randint(98,102)

            update = datetime.datetime.now()
            new_data = pd.DataFrame({
            'temperature': data['temperature'],
            'monoxide': data['monoxide'],
            'red': data['red'],
            'green': data['green'],
            'blue': data['blue'],
            'status': data['status'],
            'pressure': data['pressure']})

            if (sugDim and sugEnable):
                new_data = pd.DataFrame({
            'temperature': data['temperature'],
            'monoxide': data['monoxide'],
            'red': int(data['red'][0])/3,
            'green': int(data['green'][0])/3,
            'blue': int(data['blue'][0])/3,
            'status': data['status'],
            'pressure': data['pressure']})

            new_data.to_csv(bucket, index = False)
            new_data= pd.DataFrame({
            'temperature': data['temperature'],
            'monoxide': data['monoxide'],
            'red': data['red'],
            'green': data['green'],
            'blue': data['blue'],
            'status': data['status'],
            'pressure': data['pressure'], 'update': update})
            new_data.to_csv('log.csv',mode='a', index=False, header=False)
            return{'red' : int(data['red'][0]),'blue': int(data['blue'][0]) ,'green': int(data['green'][0])}, 200
        else:
            return{'message': 'unverified, fuck off'}, 401

class dim_on(Resource):
    def get(self):
        sugEnable = True
        return{
        "toast": "LDR based dimming is on"
        }

class dim_off(Resource):
    def get(self):
        sugEnable = False
        return{
        "toast": "LDR based dimming is off"
        }

class state(Resource):
    def get(self):
        
        return{ 
        "refresh": True
        }, 200
class refresh(Resource):
    def get(self):
        
        return{ 
        "refresh": True
        }, 200
        




class commands(Resource):
    def get(self):
        data = pd.read_csv(bucket)
        data = data.to_dict()
        stss = ("Temperature: "+ str(data['temperature']) + "\n"
        "Temperature: "+ str(data['temperature']) + "\n"
        "Monoxide: "+ str(data['monoxide']) + "\n"
        "Pressure: "+ str(data['pressure']) + "\n"
        "Temperature: "+ str(data['temperature']) + "\n")
        
        return(
{
  "commands": {
    "dim_on": {
      "title": "LDR Dim On",
      "summary": "Enables LDR Dim",
      "icon": "lamp",
      "mode": "action"
    },
    "dim_off": {
      "title": "LDR Dim Off",
      "summary": "Disables LDR Dim",
      "icon": "lamp",
      "mode": "action"
    },
    "status":{
      "title": "Temperature",
      "summary": str(data['temperature'][0]) + " Degrees",
      "icon": "thermometer",
      "mode": "none"
    },
    "status2":{
      "title": "Monoxide",
      "summary": str(data['monoxide'][0]) + "",
      "icon": "gauge",
      "mode": "none"
    },
    "status3":{
      "title": "Pressure",
      "summary": str(data['pressure'][0]) + " kPa",
      "icon": "gauge",
      "mode": "none"
    },
    "setRGB": {
      "title": "RGB LED Adjuster",
      "summary": "Changes color of LED",
      "icon": "schwibbogen",
      "mode": "input"
    },
    "refresh": {
      "title": "Refresh",
      "summary": "Refreshes data",
      "icon": "raspberry pi",
      "mode": "action"
    }


  }
}, 200
)


api.add_resource(AllData, '/alldata')
#api.add_resource(RGBset, '/rgb')
api.add_resource(dim_on, '/dim_on')
api.add_resource(dim_off, '/dim_off')
api.add_resource(commands, '/commands')
api.add_resource(state, '/status')
api.add_resource(refresh, '/refresh')
api.add_resource(sensorUpdate, '/sensorUpdate')


if __name__ == '__main__':
    app.run(host="10.200.81.243", port=727)  # run our Flask app