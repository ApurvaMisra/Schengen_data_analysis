import numpy as numpy
import json
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import pickle
#import gmplot

pd.options.mode.chained_assignment = None

mydb= mysql.connector.connect(host="127.0.0.1", user="root", passwd="csg", database="atlasmeasure")

pickle_file=open('pickle_measurement1', 'ab')
df1= pd.read_sql("SELECT * FROM measurement_complete1", con=mydb)
print(df1.describe())
print(df1.dtypes)
print(df1.head(1000))
print("length of df1", df1.shape)
hel=df1.country.value_counts()
print(df1['timestamp'].dt.month)
befor_df=df1.loc[df1['timestamp'].dt.month == 3]
print(befor_df.head())
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot()
print(world.dtypes)
print(world.head())
lon_lat={}
df1['country']= df1['country'].str.lower()
print(df1.head())
df1["long"]=""
df1["lat"]=""
with open('countrycode-latlong.json') as json_file:
    lon_lat=json.load(json_file)

print("length",df1.shape)

train = pd.DataFrame.from_dict(lon_lat, orient='index')
train.reset_index(level=0, inplace=True)
print("train", train.head())


df1.country=df1.country.astype('category')
print("length of unique countries", df1.country.unique())
uni_count=df1.country.unique()
for ev_row in range(df1.shape[0]):
    for ev_count in uni_count:
        #print("indexloc",df1.iloc[[ev_row],[2]])
        #print("keys", ev_count)
        #print("json", lon_lat[ev_count])
        #print("longitude value",lon_lat[ev_count]['long'])
        #print("ev_count",ev_count)
        if(df1.iloc[[ev_row],[2]].values[0]=='oo'):
            df1["long"].iloc[[ev_row]]=0
            df1["lat"].iloc[[ev_row]]=0
            break
        elif(df1.iloc[[ev_row],[2]].values[0]==ev_count):
            df1["long"].iloc[[ev_row]]=lon_lat[ev_count]['long']
            df1["lat"].iloc[[ev_row]]=lon_lat[ev_count]['lat']
            break

    print(ev_row)
       
    #print(df1)
#print(df1.head())
pickle.dump(df1, pickle_file)
pickle_file.close()





#plt.pie(hel.values,  labels=hel.index) #In one year of data collection which countries does the package travel through the most 

#plt.axis('equal')
plt.show()

