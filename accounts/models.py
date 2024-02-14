from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LoanSchemeForFarmers(models.Model):
    loan_id=models.AutoField
    info=models.TextField()
    scheme_name=models.CharField(max_length=200)
    def __str__(self):
        return self.scheme_name

class CropInfo(models.Model):
    crop_id=models.AutoField
    crop_name=models.CharField(max_length=200)
    crop_info=models.TextField()
    img=models.ImageField(upload_to="accounts/images")
    def __str__(self):
        return self.crop_name
    
class ContactUs(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000) 
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def _str_(self):
        return 'Message from ' + self.name + ' -  ' + self.email


# class ContactUs(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name




class extendeduser(models.Model):
    phone=models.CharField(max_length=12)
    cat=models.CharField(max_length=10)
    town=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class MarketPrices(models.Model):
    town=models.CharField(max_length=10)
    market=models.CharField(max_length=20)
    crop=models.CharField(max_length=20)
    date=models.DateField()
    price=models.IntegerField()
    def __str__(self):
        return self.town

class WillPlant(models.Model):
    user=models.CharField(max_length=20)
    crop=models.CharField(max_length=20)
    town=models.CharField(max_length=20)
    def __str__(self):
        return self.town

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import operator
import csv
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
import joblib

today = datetime.today()
datem = datetime.now().month

from sklearn.preprocessing import OneHotEncoder


def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframes.'''
    listOfPos = list()
    result = dfObj.isin([value])
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    return listOfPos


class approvals(models.Model):
    def __init__(self):
        pass
    def predict(self,district,value):
        crop_pred_dataset = pd.read_csv('./model/crop-prod-dataset.csv')
        annual_rainfall = pd.read_csv('./model/annual-rainfall.csv')
        annual_rainfall = annual_rainfall[['DISTRICT', 'ANNUAL']]
        temp_ph = pd.read_csv('./model/temp-ph-citywise.csv')
        previous_year = pd.read_csv('./model/previous-year-prod.csv')
        d4 = previous_year
        # random = joblib.load('./model/ramdomF_model')

        dic = {'Bajra': 0.0, 'Banana': 0.0, 'Barley': 0.0, 'Bean': 0.0, 'Black pepper': 0.0, 'Blackgram': 0.0,
               'Bottle Gourd': 0.0, 'Brinjal': 0.0,
               'Cabbage': 0.0, 'Cardamom': 0.0, 'Carrot': 0.0, 'Castor seed': 0.0, 'Cauliflower': 0.0, 'Chillies': 0.0,
               'Colocosia': 0.0, 'Coriander': 0.0,
               'Cotton': 0.0, 'Cowpea': 0.0, 'Drum Stick': 0.0, 'Garlic': 0.0, 'Ginger': 0.0, 'Gram': 0.0,
               'Grapes': 0.0, 'Groundnut': 0.0, 'Gaur seed': 0.0, 'Horse-gram': 0.0,
               'Jowar': 0.0, 'Jute': 0.0, 'Khesari': 0.0, 'Lady Finger': 0.0, 'Lentil': 0.0, 'Linseed': 0.0,
               'Maize': 0.0, 'Mesta': 0.0, 'Moong': 0.0, 'Moth': 0.0, 'Onion': 0.0,
               'Orange': 0.0, 'Papaya': 0.0, 'Peas': 0.0, 'Pineapple': 0.0, 'Potato': 0.0, 'Raddish': 0.0, 'Ragi': 0.0,
               'Rice': 0.0, 'Safflower': 0.0, 'Sannhamp': 0.0, 'Sesamum': 0.0,
               'Soyabean': 0.0, 'Sugarcane': 0.0, 'Sunflower': 0.0, 'Sweet potato': 0.0, 'Tapioca': 0.0, 'Tomato': 0.0,
               'Turmeric': 0.0, 'Urad': 0.0, 'Varagu': 0.0, 'Wheat': 0.0
               }

        lis = list(dic)
        c_season = value

        inp = district.upper()

        listOfPositions = getIndexes(annual_rainfall, inp)
        rain = annual_rainfall.loc[listOfPositions[0][0]][1]

        loc = getIndexes(temp_ph, inp)
        temp = temp_ph.iloc[loc[0][0]][1]
        ph = temp_ph.iloc[loc[0][0]][2]

        predicted_crop_list = {}
        d3 = {}
        pr = {}
        val = d4.loc[d4['District_Name'] == inp]
        for i in range(0, 58):
            dic[lis[i]] = 1.0
            # Checking crops from dict one by one
            z_test = [[dic['Bajra'], dic['Banana'], dic['Barley'], dic['Bean'], dic['Black pepper'], dic['Blackgram'],
                       dic['Bottle Gourd'], dic['Brinjal'], dic['Cabbage'], dic['Cardamom'], dic['Carrot'],
                       dic['Castor seed'], dic['Cauliflower'], dic['Chillies'], dic['Colocosia'], dic['Coriander'],
                       dic['Cotton'], dic['Cowpea'], dic['Drum Stick'], dic['Garlic'], dic['Ginger'], dic['Gram'],
                       dic['Grapes'], dic['Groundnut'],
                       dic['Gaur seed'], dic['Horse-gram'], dic['Jowar'], dic['Jute'], dic['Khesari'],
                       dic['Lady Finger'], dic['Lentil'], dic['Linseed'], dic['Maize'], dic['Mesta'], dic['Moong'],
                       dic['Moth'], dic['Onion'], dic['Orange'], dic['Papaya'], dic['Peas'], dic['Pineapple'],
                       dic['Potato'], dic['Raddish'], dic['Ragi'], dic['Rice'], dic['Safflower'], dic['Sannhamp'],
                       dic['Sesamum'], dic['Soyabean'], dic['Sugarcane'],
                       dic['Sunflower'], dic['Sweet potato'], dic['Tapioca'], dic['Tomato'], dic['Turmeric'],
                       dic['Urad'], dic['Varagu'], dic['Wheat'],
                       float(rain), temp, ph]]
            # Prediction of value according to rainfall,temp,ph
            # y_pred = list(randomregressor.predict(z_test))
            # y_pred = list(random.predict(z_test))
            y_pred=[1]
            # y_pred = list(randomregressor.predict(z_test))
            dic[lis[i]] = 0.0
            predicted_crop_list[lis[i]] = y_pred
            found = val.loc[val['Crop'].str.contains(str(lis[i]))]

            if found.count()[0] != 0:

                # val=val.loc[val['Season']=='Kharif']
                if (c_season == 0 and curr_season == 'K') or c_season == 1:
                    val = val.loc[val['Season'] == 'Kharif     ']
                    curr_season = 'Kharif'
                elif (c_season == 0 and curr_season == 'R') or c_season == 2:
                    val = val.loc[val['Season'] == 'Rabi       ']
                    curr_season = "Rabi"
                elif c_season == 3:
                    val = val.loc[val['Season'] == 'Whole Year ']
                    curr_season = "Whole Year"
                val = val.loc[val['Crop'] == str(lis[i])]
                total = val['per production'].sum()
                if val.shape[0] != 0:
                    total = float(total / (val.shape[0]))
                if total / 1 == total:
                    val = list(val.Crop.unique())
                if lis[i] in val:
                    d3[lis[i]] = ((total * 100) + y_pred[0]) / 200
                z = val
                val = d4.loc[d4['District_Name'] == inp]
                dic[lis[i]] = 0.0
                prediction = sorted(d3.items(), key=lambda x: x[1], reverse=True)

        sorted_d = dict(sorted(predicted_crop_list.items(), key=operator.itemgetter(1), reverse=True))
        # for value in sorted_d.items():
        #     print(value)
        sort_orders = sorted(d3.items(), key=lambda x: x[1], reverse=True)
        return (sorted_d,sort_orders)




