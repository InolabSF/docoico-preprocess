import pandas as pd
import numpy as np
import os
import urllib.request
import json


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
        # by destination address component
        # https://developers.google.com/places/supported_types#table2
address_components = {}
total_address_components = {}
for index, row in df_destination.iterrows():
    address_components[row['administrative_area_level_1']] = []
for key, value in address_components.items():
    total_address_components[key] = 0
for index, row in df_destination.iterrows():
    for key, value in total_address_components.items():
        if row['administrative_area_level_1'] == key:
            total_address_components[key] = total_address_components[key] + 1
destination_lists = df_user_destination['Destination [User destinations]'].values
for destination_list in destination_lists:
    value = {}
    for key, v in address_components.items():
        value[key] = 0
    for index, row in df_destination.iterrows():
        if row['Id'] in destination_list:
            value[row['administrative_area_level_1']] = value[row['administrative_area_level_1']] + 1
    for key, v in address_components.items():
        #address_components[key].append(value[key] / total_address_components[key])
        address_components[key].append(value[key])
for key, value in address_components.items():
    #df_user_destination["Probability [Destination %s] (total: %s)" % (key, total_address_components[key])] = pd.Series(address_components[key]).values
    df_user_destination["Destination [%s] (total: %s)" % (key, total_address_components[key])] = pd.Series(address_components[key]).values
        # by Os name, Browser name, Device name
fields = ['Os name', 'Browser name', 'Device name']
for field in fields:
    lists = {}
    columns = []
    full_names = df_user[field].values
    for full_name in full_names:
        name = full_name.split('#')
        if name not in columns:
            columns.append(name[0])
    for column in columns:
        lists[column] = []
        for full_name in full_names:
            value = 0
            if full_name.startswith(column):
                value = 1
            lists[column].append(value)
    for column in columns:
        df_user["%s %s" % (field, column)] = pd.Series(lists[column]).values
    # join
df_user = pd.merge(df_user, df_user_destination_offset, on='User', how='outer')
df_user = pd.merge(df_user, df_user_destination, on='User', how='outer')
    # clean
for destination_id in destination_ids:
    df_user["Destination %s" % destination_id] = df_user["Destination %s" % destination_id].fillna(0).astype(int)
columns = ['Offset index [User destination offset]', 'Round [User destination offset]', 'Start [User destination offset]', 'Offset [User destination offset]']
for column in columns:
    df_user[column] = df_user[column].replace(' - ', np.nan).fillna(0).astype(int)
columns = ['User agent', 'Browser name', 'Device name', 'Os name']
for column in columns:
    df_user[column] = df_user[column].replace(' - ', '')
columns = ['Destination [User destinations]', 'Created at [User destinations]', 'Updated at [User destinations]']
for column in columns:
    df_user[column] = df_user[column].fillna('[]')
for key, value in address_components.items():
    #k = "Probability [Destination %s] (total: %s)" % (key, total_address_components[key])
    #df_user[k] = df_user[k].fillna(0).astype(float)
    k = "Destination [%s] (total: %s)" % (key, total_address_components[key])
    df_user[k] = df_user[k].fillna(0).astype(int)
    # expand columns by gcloud vision api detect-labels
    # https://cloud.google.com/vision/docs/labels
detect_labels  = {}
lists = {}
for key in df_destination:
    if key.startswith('Gcloud detect-labels '):
        detect_labels[key] = {}
        lists[key] = []
for index, row in df_destination.iterrows():
    for key, value in detect_labels.items():
        value = 0
        if row[key] > 0:
            value = 1
        detect_labels[key][row['Id']] = value
total_detect_labels = {}
for key, value in detect_labels.items():
    total_detect_labels[key] = 0
    for destination_id, flag in value.items():
        if flag > 0:
            total_detect_labels[key] = total_detect_labels[key] + 1
for index, row in df_user.iterrows():
    values = {}
    for key, value in detect_labels.items():
        values[key] = 0
    for destination_id in destination_ids:
        if row["Destination %s" % destination_id] == 0:
            continue
        for key, value in detect_labels.items():
            if value[destination_id] > 0:
                values[key] = values[key] + 1
    for key, value in values.items():
        #lists[key].append(value / total_detect_labels[key])
        lists[key].append(value)
for key, value in lists.items():
    #df_user["Probability [%s] (total: %s)" % (key, total_detect_labels[key])] = pd.Series(value).values
    k = "%s (total: %s)" % (key, total_detect_labels[key])
    df_user[k] = pd.Series(value).values
    df_user[k] = df_user[k].fillna(0).astype(int)
    # save
df_user.to_csv('./datas/user.csv', encoding='utf-8', index=False)
