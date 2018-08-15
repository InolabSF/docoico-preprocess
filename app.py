import pandas as pd
import numpy as np
import urllib.request
import json


## expand columns
#    # by ip
#df = pd.read_csv('./tables/user.csv', sep=',')
#columns = ['Current sign in ip', 'Last sign in ip']
#fields = [
#    'country_code',
#    'country_name',
#    'city',
#    'postal',
#    'latitude',
#    'longitude',
#    'state'
#]
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


# destination
df = pd.read_csv('./tables/destination.csv', sep=',')
columns = df.columns.drop(['Subtitle', 'Desc', 'Category'])
df_destination = df[columns]
    # save
df_destination.to_csv('./datas/destination.csv', encoding='utf-8', index=False)


# user
    # user
df = pd.read_csv('./tables/user.csv', sep=',')
columns = df.columns.drop(['Email', 'Reset password sent at', 'Remember created at', 'Admin', 'Line', 'Name', 'Access token', 'Refresh token'])
df_user = df.query('Admin != "t"')[columns]
df_user = df_user.rename(columns={'Id': 'User'})
    # user destination offset
df = pd.read_csv('./tables/user_destination_offset.csv', sep=',')
columns = df.columns.drop(['Id'])
new_names = {}
for column in columns:
    new_name = "%s" % column
    if new_name.startswith('Offset.1'):
        new_name = new_name.replace('Offset.1', 'Offset [User destination offset]')
    elif new_name.startswith('Offset'):
        new_name = new_name.replace('Offset', 'Offset index [User destination offset]')
    elif new_name.startswith('User') == False:
        new_name = "%s [User destination offset]" % column
    new_names[column] = new_name
df_user_destination_offset = df[columns]
df_user_destination_offset = df_user_destination_offset.rename(columns=new_names)
    # user destination
df_user_destination = pd.DataFrame({'User' : []})
df = pd.read_csv('./tables/user_destination.csv', sep=',')
columns = df.columns.drop(['Id', 'User result', 'Value'])
df = df.query('Value > 0')[columns]
new_names = {}
for column in columns:
    if column.startswith('User'):
        continue
    sf = df.groupby(['User'])[column].apply(list)
    new_df = pd.DataFrame({'User': sf.index, column: sf.values})
    if df_user_destination.empty:
        df_user_destination = new_df
    else:
        df_user_destination = pd.merge(df_user_destination, new_df, on='User', how='outer')
    new_names[column] = "%s [User destinations]" % column
df_user_destination = df_user_destination.rename(columns=new_names)
        # expand columns
        # by destination id
lists = {}
destination_ids = df_destination['Id'].values
for destination_id in destination_ids:
    lists[destination_id] = []
destination_lists = df_user_destination['Destination [User destinations]'].values
for destination_list in destination_lists:
    for destination_id in destination_ids:
        value = 0
        if destination_id in destination_list:
            value = 1
        lists[destination_id].append(value)
for destination_id in destination_ids:
    df_user_destination["Destination %s" % destination_id] = pd.Series(lists[destination_id]).values
    # join
df_user = pd.merge(df_user, df_user_destination_offset, on='User', how='outer')
df_user = pd.merge(df_user, df_user_destination, on='User', how='outer')
    # save
df_user.to_csv('./datas/user.csv', encoding='utf-8', index=False)
