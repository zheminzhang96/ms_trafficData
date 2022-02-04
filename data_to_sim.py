import datetime as dt
import pandas as pd
import numpy as np
from datetime import *
import string
import random
from random import seed
from random import randint
import itertools

# *******CLEANING AND FORMATTING DATA**********
data = pd.read_csv('TrafficCountBook.csv')
# print(data.to_string())
# data_clean = data.drop(["Unamed: 15", "Unamed: 15", "Unamed: 15", "Unamed: 16", "Unamed: 17"], axis=1)
# data_clean = data.dropna()
data_clean = data.drop(labels=range(1378, 1998), axis=0)
# print(data_clean.shape)
data_clean = data_clean.drop(columns=data_clean.columns[11:23], axis=1)
data_clean = data_clean.dropna()
data_clean = data_clean.reset_index(drop=True)
data_clean['Date'] = pd.to_datetime(data_clean['Date'])
data_clean['AM Hour'] = pd.to_datetime(data_clean['AM Hour']).dt.time
data_clean['PM Hour'] = pd.to_datetime(data_clean['PM Hour']).dt.time
# print(data_clean.shape)
# print(data_clean.to_string())
df = pd.DataFrame(data_clean)
df = df.rename(columns={'Site ID': 'SiteID', 'On Road': 'OnRoad', 'Ref Road': 'RefRoad', 'AM Hour': 'AM_Hour',
                        'AM Volume': 'AM_Volume', 'PM Hour': 'PM_Hour', 'PM Volume': 'PM_Volume'})
dayofweek_array = df['Date'].dt.dayofweek
weekofyear_array = df['Date'].dt.isocalendar().week
# df.assign(dayofweek=df['Date'].dt.dayofweek)
#df.insert(loc=2, column='weekofyear', value=weekofyear_array)
#df.insert(loc=3, column='dayofweek', value=dayofweek_array)
#print(len(df))
#maricopa_sample = pd.DataFrame()
# df.to_csv(r'C:\#Classes\CSE599\TrafficData\traffic_data_export.csv')   #export new .csv file

# ns_group = df[df['Direction'].isin(['N', 'S'])]
# ns_group_arr = ns_group['OnRoad'].value_counts().index.tolist()[:18]
# #ns_group_arr = ns_group.OnRoad.unique()
# ew_group = df[df['Direction'].isin(['E', 'W'])]
# #ew_group_arr = ew_group.OnRoad.unique()
# ew_group_arr = ew_group['OnRoad'].value_counts().index.tolist()[:30]
ns_group_arr = ['355th Ave', 'Jackrabbit Tr', 'El Mirage', '107th Ave', '99th Ave']
ew_group_arr = ['Thunderbird Blvd', 'Peoria Ave', 'Camelback Rd', 'Indian School Rd', 'Van Buren St',
                'Buckeye Rd', 'Lower Buckeye Rd', 'MC 85', 'Broadway Rd', 'Southern Ave', 'Baseline Rd',
                'Dobbins Rd', 'Elliot Rd']
print("Roads in N/S direction ", ns_group_arr)
print("Roads in E/W direction ", ew_group_arr)
group_select = df[(df['OnRoad'].isin(ns_group_arr) & df['RefRoad'].isin(ew_group_arr)) |
                  (df['OnRoad'].isin(ew_group_arr) & df['RefRoad'].isin(ns_group_arr))]
group = group_select.reset_index()
print(group.to_string())

for i in range(0, len(group)):
    #print(group.iloc[i]['AM_Hour'])
    group.at[i, 'AM_Hour'] = group.iloc[i]['AM_Hour'].hour + group.iloc[i]['AM_Hour'].minute/60
    group.at[i, 'PM_Hour'] = group.iloc[i]['PM_Hour'].hour + group.iloc[i]['PM_Hour'].minute / 60
#print(group.to_string())

road_pair_ns = list(itertools.product(ns_group_arr, ew_group_arr))
road_pair_ew = list(itertools.product(ew_group_arr, ns_group_arr))
ns_len = len(road_pair_ns)
ew_len = len(road_pair_ew)
for i in range(ns_len):
    road_pair_ns[i] = road_pair_ns[i] + ('N',)
    #print(road_pair_ns[i])
for i in range(ns_len):
    new_tuple = (road_pair_ns[i][0], road_pair_ns[i][1], 'S')
    #print(new_tuple)
    road_pair_ns.append(new_tuple)
#print(len(road_pair_ns))
for i in range(ew_len):
    road_pair_ew[i] = road_pair_ew[i] + ('E',)
    #print(road_pair_ns[i])
for i in range(ew_len):
    new_tuple = (road_pair_ew[i][0], road_pair_ew[i][1], 'W')
    #print(new_tuple)
    road_pair_ew.append(new_tuple)
road_pair = road_pair_ns + road_pair_ew
#print(road_pair)
def road_pattern(selection, start_t, end_t):
    #print(selection[0])
    new_record = {}
    rand_time = random.uniform(start_t, end_t)
    #Roads runs E/W directions
    if selection[0] == "Thunderbird Blvd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 70) + 50 + (rand_time * 5))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 1400) + 250 + (rand_time - 5) * 250)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 1400) + 1000 + (rand_time - 8) * -150)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(400, 900))
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(300, 900) + 600 + (rand_time - 14) * 250)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 400) + 1000 + (rand_time - 17) * -300)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 300) + 700 + (rand_time - 19) * -200)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 70) + 400 + (rand_time - 21) * -120)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Peoria Ave":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 0 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 100) + 100 + (rand_time - 5) * 100)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 100) + 400 + (rand_time - 8) * -100)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 12) * -150)
        elif start_t >= 14 and end_t <= 17:
            est_volume = int(randint(300, 900) + 600 + (rand_time - 14) * 250)
        elif start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 400) + 1000 + (rand_time - 17) * -300)
        elif start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 300) + 700 + (rand_time - 19) * -200)
        elif start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 50) + 400 + (rand_time - 21) * -125)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Camelback Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 800) + 100 + (rand_time - 5) * 100)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 200) + 400 + (rand_time - 8) * -100)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(400, 900))
        elif start_t >= 14 and end_t <= 17:
            est_volume = int(randint(300, 900) + 600 + (rand_time - 14) * 250)
        elif start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 400) + 1000 + (rand_time - 17) * -300)
        elif start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 300) + 700 + (rand_time - 19) * -200)
        elif start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 50) + 400 + (rand_time - 21) * -125)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Indian School Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 500) + 500 + (rand_time - 5) * 400)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 500) + 500 + (rand_time - 5) * 400)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 100) + 80 + (rand_time - 5) * 20)
            else:
                est_volume = int(randint(0, 100) + 80 + (rand_time - 5) * 20)
        elif start_t >= 8 and end_t <= 12:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 500) + 1700 + (rand_time - 8) * -300)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 500) + 1700 + (rand_time - 8) * -300)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 100) + 140 + (rand_time - 8) * -30)
            else:
                est_volume = int(randint(0, 100) + 80 + (rand_time - 5) * 20)
        elif start_t >= 12 and end_t <= 14:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 500) + 700 + (rand_time - 12) * 200)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 500) + 700 + (rand_time - 12) * 200)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 100) + 80 + (rand_time - 12) * 20)
            else:
                est_volume = int(randint(0, 100) + 80 + (rand_time - 12) * 20)
        elif start_t >= 14 and end_t <= 17:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 500) + 1000 + (rand_time - 14) * 400)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 500) + 1000 + (rand_time - 14) * 400)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 100) + 80 + (rand_time - 14) * 20)
            else:
                est_volume = int(randint(0, 100) + 80 + (rand_time - 14) * 20)
        elif start_t >= 17 and end_t <= 19:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 600) + 1500 + (rand_time - 17) * -300)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 500) + 1400 + (rand_time - 17) * -300)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 50) + 100 + (rand_time - 17) * -25)
            else:
                est_volume = int(randint(0, 50) + 100 + (rand_time - 17) * -25)
        elif start_t >= 19 and end_t <= 21:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 300) + 1000 + (rand_time - 19) * -200)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 300) + 1000 + (rand_time - 19) * -200)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 20) + 70 + (rand_time - 19) * -15)
            else:
                est_volume = int(randint(0, 20) + 70 + (rand_time - 19) * -15)
        elif start_t >= 21 and end_t <= 24:
            if selection[1] == "99th Ave":
                est_volume = int(randint(0, 150) + 900 + (rand_time - 21) * -250)
            if selection[1] == "107th Ave":
                est_volume = int(randint(0, 150) + 900 + (rand_time - 21) * -250)
            if selection[1] == "355th Ave":
                est_volume = int(randint(0, 20) + 40 + (rand_time - 21) * -10)
            else:
                est_volume = int(randint(0, 20) + 40 + (rand_time - 21) * -10)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Van Buren St":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 0 + (rand_time * 4))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 50) + 10 + (rand_time - 5) * 10)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 50) + 40 + (rand_time - 8) * -10)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 30) + 20 + (rand_time - 12) * 5)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(20, 50) + 30 + (rand_time - 14) * 10)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 30) + 70 + (rand_time - 17) * -15)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 30) + 50 + (rand_time - 19) * -10)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(5, 40) + 50 + (rand_time - 21) * -15)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Buckeye Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 10 + (rand_time * 10))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 100) + 50 + (rand_time - 5) * 30)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 50) + 140 + (rand_time - 8) * -20)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 50) + 40 + (rand_time - 12) * 10)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(20, 50) + 40 + (rand_time - 14) * 20)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 30) + 100 + (rand_time - 17) * -30)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 30) + 60 + (rand_time - 19) * -15)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 30) + 60 + (rand_time - 21) * -20)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Lower Buckeye Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 0 + (rand_time * 5))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 40) + 0 + (rand_time - 5) * 10)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 100) + 30 + (rand_time - 8) * -5)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 50) + 60 + (rand_time - 8) * 10)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(0, 80) + 50 + (rand_time - 14) * 30)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 60) + 100 + (rand_time - 17) * -35)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 30) + 50 + (rand_time - 19) * -10)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 30) + 40 + (rand_time - 21) * -15)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "MC 85":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 50) + 30 + (rand_time * 10))
            #print("first if")
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 500) + 150 + (rand_time - 5) * 150)
            #print(est_volume)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 500) + 600 + (rand_time - 8) * -110)
            #print("second if")
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 300) + 200 + (rand_time - 8) * 100)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(20, 650) + 400 + (rand_time - 14) * 200)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 300) + 1000 + (rand_time - 17) * -300)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 300) + 500 + (rand_time - 19) * -100)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(5, 100) + 450 + (rand_time - 21) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Broadway Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 0 + (rand_time * 5))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 30) + 0 + (rand_time - 5) * 10)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 20) + 30 + (rand_time - 8) * -5)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 20) + 30 + (rand_time - 8) * 5)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(0, 30) + 30 + (rand_time - 14) * 10)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 30) + 60 + (rand_time - 17) * -15)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 20) + 30 + (rand_time - 19) * -5)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(0, 15) + 20 + (rand_time - 21) * -6)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Southern Ave":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 30) + 5 + (rand_time * 10))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 150) + 50 + (rand_time - 5) * 100)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 50) + 350 + (rand_time - 8) * -80)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 12) * -150)
        if start_t >= 14 and end_t <= 17:
            est_volume = int(randint(20, 50) + 30 + (rand_time - 14) * 10)
        if start_t >= 17 and end_t <= 19:
            est_volume = int(randint(0, 30) + 70 + (rand_time - 17) * -15)
        if start_t >= 19 and end_t <= 21:
            est_volume = int(randint(0, 30) + 50 + (rand_time - 19) * -10)
        if start_t >= 21 and end_t <= 24:
            est_volume = int(randint(5, 40) + 50 + (rand_time - 21) * -15)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Baseline Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 30) + 5 + (rand_time * 15))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 100) + 140 + (rand_time - 5) * 400)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 300) + 1300 + (rand_time - 8) * -300)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Dobbins Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 70) + 30 + (rand_time - 5) * 20)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 80) + 110 + (rand_time - 8) * -20)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Elliot Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 50) + 30 + (rand_time - 5) * 20)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 50) + 90 + (rand_time - 8) * -10)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}

    #Roads run N/S direction
    if selection[0] == "99th Ave":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 500) + 120 + (rand_time - 5) * 150)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 350) + 550 + (rand_time - 8) * -50)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "107th Ave":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 100) + 20 + (rand_time * 20))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 1100) + 500 + (rand_time - 5) * 500)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 200) + 800 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Dysart Rd":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 70) + 10 + (rand_time * 15))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 500) + 300 + (rand_time - 5) * 150)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 100) + 850 + (rand_time - 8) * -200)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "El Mirage":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 100) + 50 + (rand_time - 5) * 50)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 100) + 200 + (rand_time - 8) * -40)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "Jackrabbit Tr":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 5 + (rand_time * 10))
        elif start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 150) + 150 + (rand_time - 5) * 100)
        elif start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 100) + 450 + (rand_time - 8) * -90)
        elif start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    if selection[0] == "355th Ave":
        est_volume = 0
        if start_t >= 0 and end_t <= 5:
            est_volume = int(randint(0, 20) + 0 + (rand_time * 4))
        if start_t >= 5 and end_t <= 8:
            est_volume = int(randint(0, 70) + 20 + (rand_time - 5) * 10)
        if start_t >= 8 and end_t <= 12:
            est_volume = int(randint(0, 80) + 50 + (rand_time - 8) * -10)
        if start_t >= 12 and end_t <= 14:
            est_volume = int(randint(0, 1000) + 1000 + (rand_time - 8) * -150)
        new_record = {'OnRoad': selection[0], 'RefRoad': selection[1], 'Direction': selection[2],
                      'Hour': rand_time, 'Volume': est_volume}
    return new_record

def maricopa_pattern(start_t, end_t):
    #df_sample = group[group['AM_Hour'].between(start_t, end_t)]
    #df_sample = df_sample[['OnRoad', 'RefRoad', 'Direction', 'AM_Hour', 'AM_Volume', 'PM_Hour', 'PM_Volume']]
    #print(df_sample.to_string())
    #random.shuffle(road_pair)
    generated_data = pd.DataFrame(columns=['OnRoad', 'RefRoad', 'Direction', 'Hour', 'Volume'])
    #print(generated_data.to_string())
    for i in range(len(road_pair)):
        new_record = road_pattern(road_pair[i], start_t, end_t)
        generated_data = generated_data.append(new_record, ignore_index=True)
        generated_data = generated_data.sort_values(by=['OnRoad', 'RefRoad'])
        #maricopa_sample = df_sample
    #print(generated_data.to_string())
    #print(maricopa_sample.shape)
    return generated_data
    #df_sample1.to_json('sample10_11.json', orient="records")

def sim_pattern(start_time, end_time):
    maricopa_sample = maricopa_pattern(start_time, end_time)
    print(maricopa_sample.to_string())
    sim_df = maricopa_sample.copy()
    #print(sim_df)
    #N/S direction
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['355th Ave'], '1st St')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['355th Ave'], '1st St')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Jackrabbit Tr'], '2nd St')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Jackrabbit Tr'], '2nd St')
    #sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Dysart Rd'], '3rd St')
    #sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Dysart Rd'], '3rd St')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['El Mirage'], '3rd St')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['El Mirage'], '3rd St')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['107th Ave'], '4th St')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['107th Ave'], '4th St')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['99th Ave'], '5th St')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['99th Ave'], '5th St')
    #E/W direction
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Thunderbird Blvd'], '1st Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Thunderbird Blvd'], '1st Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Peoria Ave'], '2nd Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Peoria Ave'], '2nd Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Camelback Rd'], '3rd Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Camelback Rd'], '3rd Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Indian School Rd'], '4th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Indian School Rd'], '4th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Van Buren St'], 'Hwy B')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Van Buren St'], 'Hwy B')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Buckeye Rd'], 'Hwy B')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Buckeye Rd'], 'Hwy B')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Lower Buckeye Rd'], '5th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Lower Buckeye Rd'], '5th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['MC 85'], '6th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['MC 85'], '6th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Broadway Rd'], '7th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Broadway Rd'], '7th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Southern Ave'], '8th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Southern Ave'], '8th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Baseline Rd'], '9th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Baseline Rd'], '9th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Dobbins Rd'], '10th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Dobbins Rd'], '10th Ave')
    sim_df['OnRoad'] = sim_df['OnRoad'].replace(['Elliot Rd'], '11th Ave')
    sim_df['RefRoad'] = sim_df['RefRoad'].replace(['Elliot Rd'], '11th Ave')
    sim_df = sim_df[['OnRoad', 'RefRoad', 'Direction', 'Volume']]
    sim_df = sim_df.sort_values(by=['OnRoad', 'RefRoad'], ignore_index=True)
    sim_df['Volume'] = sim_df['Volume']/100
    for i in range(len(sim_df)):
        scale = sim_df.at[i, 'Volume']
        #print(scale)
        if 1 >= scale >= 0:
            sim_df.at[i, "Volume"] = 0
        elif 2 >= scale > 1:
            sim_df.at[i, 'Volume'] = 1
        elif 3 >= scale > 2:
            sim_df.at[i, 'Volume'] = 2
        elif 5 >= scale > 3:
            sim_df.at[i, 'Volume'] = 3
        elif 7 >= scale > 5:
            sim_df.at[i, 'Volume'] = 4
        elif 9 >= scale > 7:
            sim_df.at[i, 'Volume'] = 5
        elif 12 >= scale > 9:
            sim_df.at[i, 'Volume'] = 6
        elif 15 >= scale > 12:
            sim_df.at[i, 'Volume'] = 7
        elif 17 >= scale > 15:
            sim_df.at[i, 'Volume'] = 8
        elif 20 >= scale > 17:
            sim_df.at[i, 'Volume'] = 9
        elif 30 >= scale > 20:
            sim_df.at[i, 'Volume'] = 10
    #print(sim_df.to_string())
    return sim_df

sim2_3 = sim_pattern(2, 3)
total_traffic2_3 = sim2_3['Volume'].sum()
#print(total_traffic2_3)
sim3_4 = sim_pattern(3, 4)
total_traffic3_4 = sim2_3['Volume'].sum()
sim4_5 = sim_pattern(4, 5)
total_traffic4_5 = sim4_5['Volume'].sum()
sim5_6 = sim_pattern(5, 6)
total_traffic5_6 = sim5_6['Volume'].sum()
sim6_7 = sim_pattern(6, 7)
total_traffic6_7 = sim6_7['Volume'].sum()
sim7_8 = sim_pattern(7, 8)
total_traffic7_8 = sim7_8['Volume'].sum()
sim8_9 = sim_pattern(8, 9)
total_traffic8_9 = sim8_9['Volume'].sum()
sim9_10 = sim_pattern(9, 10)
total_traffic9_10 = sim9_10['Volume'].sum()
sim10_11 = sim_pattern(10, 11)
total_traffic10_11 = sim10_11['Volume'].sum()
sim11_12 = sim_pattern(11, 12)
total_traffic11_12 = sim11_12['Volume'].sum()
sim12_13 = sim_pattern(12, 13)
#print(sim12_13)
#print(sim4_5.to_string())
sim3_4.to_json('sim3_4.json', orient="records")
sim4_5.to_json('sim4_5.json', orient="records")
sim5_6.to_json('sim5_6.json', orient="records")
sim6_7.to_json('sim6_7.json', orient="records")
sim7_8.to_json('sim7_8.json', orient="records")
sim8_9.to_json('sim8_9.json', orient="records")
sim9_10.to_json('sim9_10.json', orient="records")
sim10_11.to_json('sim10_11.json', orient="records")
sim11_12.to_json('sim11_12.json', orient="records")
sim12_13.to_json('sim12_13.json', orient="records")

import matplotlib.pyplot as plt
hour = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
hourly_volume = [total_traffic2_3, total_traffic3_4, total_traffic4_5, total_traffic5_6, total_traffic6_7,
                 total_traffic7_8, total_traffic8_9, total_traffic9_10, total_traffic10_11, total_traffic11_12]
print(hourly_volume)
plt.plot(hour, hourly_volume)
plt.title('Hourly Traffic vs. Hour')
plt.xlabel('Hour')
plt.ylabel('Hourly Traffic')
plt.grid(True)
plt.show()