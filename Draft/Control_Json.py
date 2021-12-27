import mysql.connector
from mysql.connector import Error, connect
import json
import requests
from datetime import *
import time
from tkinter import messagebox

def getLoginInfo(filename):
    data = take_data_from_json(filename)
    data=data['login']
    return data

def add_new_user(username,password,filename):
    new_data={"username":username,"password":password}

    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["login"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
    return

def update_data_from_api():

    api_key = requests.get("https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate")
    data = api_key.text
    data=json.loads(data)
    data=data['results']
    headers={"api_key":data}

    exchange_rate = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/ctg",headers)
    data = exchange_rate.text
    data=json.loads(data)
    today = date.today()
    name_database = today.strftime("%d-%m-%Y")

    with open("Data/"+name_database+".json", "w") as outfile:
        json.dump(data, outfile ,indent=4)
        
    return data

def take_data_from_json(filename):
    try:
        f=open("Data/"+filename)
        data = json.load(f)
        return data
    except:
        print("can't open file")
        return False

def alarm():
    while True:
        update_data_from_api()
        time.sleep(1800)