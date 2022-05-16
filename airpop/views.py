from django.contrib import messages
from django.shortcuts import render,redirect
import requests
from django.contrib.auth import logout
import datetime, pytz
from django.conf import settings
from zmq import Message
from .forms import Datasetform
from .functions.functions import handle_uploaded_file
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional
from sklearn.preprocessing import LabelEncoder
def dashboard(request):
    return render(request,'index.html')
def index(request):
    city = request.GET.get('city')
    filename = request.session['filename']
    if filename==None or filename == "":  
        # filename = "vyttila32.csv"
         filename = "tvm1.csv"      
    print(filename)
    if city == 'kochi':
        city = 'cochin'
    if (city == None):
        url = f'https://api.waqi.info/feed/here/?token=3b6b9aa20ffe9593451db9733193ac71573f07b4'
    else:
        url=f'https://api.waqi.info/feed/{city}/?token=3b6b9aa20ffe9593451db9733193ac71573f07b4'
    response = requests.request("GET", url)
    content = response.json()
    datachk=content.get('status')
    prediction_tomorrow=""
    prediction_dayaftertomorrow=""
    prediction_3rdday=""
    prediction_4thday=""
    prediction_5thday=""
    if datachk != "ok":
        messages.error(request,"Entered Place is Unknown")
    else:      
        # print(content.get('data'))
        x=content.get('data')
        # print(x.get('forecast'))
        y=x.get('forecast')
        # print(y.get('daily'))
        z=y.get('daily')
        o3=''
        o3=z.get('o3')
        value_of_o3= []
        for i in o3:
            value=i['max']
            value_of_o3.append(value)
        o3_of_today=value_of_o3[2]
        # print(value_of_o3)
        o3_of_tomorrow=value_of_o3[3]
        o3_of_dayaftertomorrow=value_of_o3[4]
        o3_of_3rdday = value_of_o3[5]
        o3_of_4thday = value_of_o3[6]
        o3_of_5thday = value_of_o3[7]
        # print('4th day',o3_of_5thday)
        pm10=z.get('pm10')
        value_of_pm10=[]
        for i in pm10:
            value=i['max']
            value_of_pm10.append(value)
        # print(value_of_pm10)
        pm10_of_today=value_of_pm10[2]
        # print(pm10_of_today)
        pm10_of_tomorrow=value_of_pm10[3]
        pm10_of_dayaftertomorrow=value_of_pm10[4]
        pm10_of_3rdday = value_of_pm10[5]
        pm10_of_4thday = value_of_pm10[6]
        pm10_of_5thday = value_of_pm10[7]
        value_of_pm25=[]
        pm25=z.get('pm25')
        for i in pm25:
            value=i['max']
            value_of_pm25.append(value)
        # print(value_of_pm10)
        pm25_of_today=value_of_pm25[2]
        # print(pm10_of_today)
        pm25_of_tomorrow=value_of_pm25[3]
        print("aaa",pm25_of_tomorrow)
        pm25_of_dayaftertomorrow=value_of_pm25[4]
        pm25_of_3rdday = value_of_pm25[5]
        pm25_of_4thday = value_of_pm25[6]
        pm25_of_5thday = value_of_pm25[7]
        # print(pm10_of_4thday)
        data_path=f'airpop/static/upload/{filename}'
        data=pd.read_csv(data_path)
        objectlist_train = data.select_dtypes(include = "object").columns
        # Then Label Encoding for object to numeric conversion
        le = LabelEncoder()
        for feature in objectlist_train:
            data[feature] = le.fit_transform(data[feature].astype(str))

        # print (data.head())
        x=data.drop(['date','pm25','no2','so2','co'],axis=1)
        x1=data.drop(['date','no2','so2','co'],axis=1)
        x2=data.drop(['date','no2','so2'],axis=1)
        # x2=data.drop(['date','so2','co'],axis=1)
        y=data['pm25']
        y1=data['co']
        y2=data['no2']
        # print(y.shape)


        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
        x1_train,x1_test,y1_train,y1_test=train_test_split(x1,y1,test_size=0.2,random_state=0)
        x2_train,x2_test,y2_train,y2_test=train_test_split(x2,y2,test_size=0.2,random_state=0)
        # print(x_test)
        model=DecisionTreeClassifier()
        model1=DecisionTreeClassifier()
        model2=DecisionTreeClassifier()
        modal = Sequential()
        modal.add(Bidirectional(LSTM(64)))
        model.fit(x_train,y_train)
        model1.fit(x1_train,y1_train)
        model2.fit(x2_train,y2_train)
        pm25_prediction_tomorrow=int(model.predict([[pm10_of_tomorrow,o3_of_tomorrow]]))
        pm25_prediction_dayaftertomorrow=int(model.predict([[pm10_of_dayaftertomorrow,o3_of_dayaftertomorrow]]))
        pm25_prediction_3rdday = int(model.predict([[pm10_of_3rdday, o3_of_3rdday]]))
        pm25_prediction_4thday = int(model.predict([[pm10_of_4thday, o3_of_4thday]]))
        pm25_prediction_5thday = int(model.predict([[pm10_of_5thday, o3_of_5thday]]))
        co_prediction_tomorrow=int(model1.predict([[pm25_prediction_tomorrow,pm10_of_tomorrow,o3_of_tomorrow]]))
        co_prediction_dayaftertomorrow=int(model1.predict([[pm25_prediction_dayaftertomorrow,pm10_of_dayaftertomorrow,o3_of_dayaftertomorrow]]))
        co_prediction_3rdday = int(model1.predict([[pm25_prediction_3rdday,pm10_of_3rdday, o3_of_3rdday]]))
        co_prediction_4thday = int(model1.predict([[pm25_prediction_4thday,pm10_of_4thday, o3_of_4thday]]))
        co_prediction_5thday = int(model1.predict([[pm25_prediction_5thday,pm10_of_5thday, o3_of_5thday]]))
        no2_prediction_tomorrow=int(model2.predict([[pm25_prediction_tomorrow,pm10_of_tomorrow,o3_of_tomorrow,co_prediction_tomorrow]]))
        no2_prediction_dayaftertomorrow=int(model2.predict([[pm25_prediction_dayaftertomorrow,pm10_of_dayaftertomorrow,o3_of_dayaftertomorrow,co_prediction_dayaftertomorrow]]))
        no2_prediction_3rdday = int(model2.predict([[pm25_prediction_3rdday,pm10_of_3rdday, o3_of_3rdday,co_prediction_3rdday]]))
        no2_prediction_4thday = int(model2.predict([[pm25_prediction_4thday,pm10_of_4thday, o3_of_4thday,co_prediction_4thday]]))
        no2_prediction_5thday = int(model2.predict([[pm25_prediction_5thday,pm10_of_5thday, o3_of_5thday,co_prediction_5thday]]))
        prediction_tomorrow=max(pm25_prediction_tomorrow,pm10_of_tomorrow,o3_of_tomorrow,co_prediction_tomorrow,no2_prediction_tomorrow)
        prediction_dayaftertomorrow=max(pm25_prediction_dayaftertomorrow,pm10_of_dayaftertomorrow,o3_of_dayaftertomorrow,co_prediction_dayaftertomorrow,no2_prediction_dayaftertomorrow)
        prediction_3rdday=max(pm25_prediction_3rdday,pm10_of_3rdday,o3_of_3rdday,co_prediction_3rdday,no2_prediction_3rdday)
        prediction_4thday=max(pm25_prediction_4thday,pm10_of_4thday,o3_of_4thday,co_prediction_4thday,no2_prediction_4thday)
        prediction_5thday=max(pm25_prediction_5thday,pm10_of_5thday,o3_of_5thday,co_prediction_5thday,no2_prediction_5thday)

    # print(prediction_today,prediction_tomorrow,prediction_dayaftertomorrow,prediction_3rdday,prediction_4thday,prediction_5thday)
    # print(accuracy_score(prediction,y_test))

    # print(forcast_data)
    return render(request,'home.html',{'data':content,'prediction_tomorrow':prediction_tomorrow,'prediction_dayaftertomorrow':prediction_dayaftertomorrow,'prediction_3rdday':prediction_3rdday,'prediction_4thday':prediction_4thday,'prediction_5thday':prediction_5thday})

def admin(request):
    # output_number = random.randrange(1,100)
    # output_id=str(output_number)
    # print(output_number)
    name=''
    info=''
    if request.method == 'POST':
        dataset = Datasetform(request.POST, request.FILES)
        if dataset.is_valid():
            handle_uploaded_file(request.FILES['file'])
            info="File uploaded successfuly"
        else:
            info="Oops Something went Wrong!"
    else:
        dataset = Datasetform()
    fileinfo=os.listdir('airpop/static/upload/')
    filename = request.GET.get('filename')
    request.session['filename'] = filename
    return render(request,'admin.html',{'data':dataset,'info':info,'fileinfo':fileinfo})
def exituser(request):
    logout(request)
    return redirect('/')