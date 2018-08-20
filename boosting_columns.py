import pandas as pd
import numpy as np
import os
import urllib.request
import json


#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
#
#
## expand columns by ip
#df = pd.read_csv('./tables/user.csv', sep=',')
#columns = ['Current sign in ip', 'Last sign in ip']
#fields = ['country_code', 'country_name', 'city', 'postal', 'latitude', 'longitude', 'state']
#for column in columns:
#    lists = {}
#    for field in fields:
#        lists[field] = []
#    for ip in df[column][::-1]:
#        with urllib.request.urlopen("https://geoip-db.com/jsonp/%s" % ip) as url:
#            data = json.loads(url.read().decode().split("(")[1].strip(")"))
#            for field in fields:
#                lists[field].append(data[field])
#    for field in fields:
#        df["%s [%s]" % (field, column)] = pd.Series(lists[field]).values
#df.to_csv('./tables/user.csv', encoding='utf-8', index=False)
#
#
## expand columns by lat lng
#df = pd.read_csv('./tables/destination.csv', sep=',')
#addresses = []
#for index, row in df.iterrows():
#    list = {}
#    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s" % (row['Lat'], row['Lng'], GOOGLE_API_KEY)) as url:
#        data = json.loads(url.read().decode())
#        if data['status'] != 'OK':
#            continue
#        address_components = data['results'][0]['address_components']
#        for address_component in address_components:
#            types = address_component['types']
#            for type in types:
#                list[type] = address_component['long_name']
#        addresses.append(list)
#lists = {}
#for address in addresses:
#    for key, value in address.items():
#        if (key in lists) == False:
#            lists[key] = []
#for address in addresses:
#    for key, value in lists.items():
#        if key in address:
#            value.append(address[key])
#        else:
#            value.append('')
#for key, value in lists.items():
#    df[key] = pd.Series(value).values
#df.to_csv('./tables/destination.csv', encoding='utf-8', index=False)


#lists = []
#descriptions = []
#df = pd.read_csv('./tables/destination.csv', sep=',')
#for index, row in df.iterrows():
#    description = {}
#    command = "gcloud ml vision detect-labels %s" % row['Image']
#    try:
#        response = os.popen(command).read()
#        data = json.loads(response)
#        for response in data['responses']:
#            for labelAnnotation in response['labelAnnotations']:
#                desc = labelAnnotation['description']
#                description[desc] = labelAnnotation['score']
#                if (desc in lists) == False:
#                    lists.append(desc)
#    except:
#        print("Failed: %s" % command)
#    descriptions.append(description)
#for description in descriptions:
#    for key in lists:
#        if (key in description) == False:
#            description[key] = 0.0
#fileds = lists
#lists = {}
#for filed in fileds:
#    lists[filed] = []
#for description in descriptions:
#    for key, value in description.items():
#        lists[key].append(value)
#for key, value in lists.items():
#    df["Gcloud detect-labels %s" % key] = pd.Series(value).values
#df.to_csv('./tables/destination.csv', encoding='utf-8', index=False)
