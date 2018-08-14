import pandas as pd


# user
    # user
df = pd.read_csv('./tables/user.csv', sep=',')
columns = ['Id', 'Current sign in at', 'Last sign in at', 'Current sign in ip', 'Last sign in ip', 'User agent', 'Browser name', 'Device name', 'Os name']
df_user = df.query('Admin != "t"')[columns]
df_user = df_user.rename(columns={'Id': 'User'})
    # user destination offset
df = pd.read_csv('./tables/user_destination_offset.csv', sep=',')
columns = ['User', 'Offset', 'Round', 'Created at', 'Updated at', 'Start', 'Offset.1']
df_user_destination_offset = df[columns]
df_user_destination_offset = df_user_destination_offset.rename(columns={'Offset': 'Offset index [User destination offset]', 'Round': 'Round [User destination offset]', 'Created at': 'Created at [User destination offset]', 'Updated at': 'Updated at [User destination offset]', 'Start': 'Start [User destination offset]', 'Offset.1': 'Offset [User destination offset]'})
    # user destination
df_user_destination = pd.DataFrame({'User' : []})
df = pd.read_csv('./tables/user_destination.csv', sep=',')
columns = ['User', 'Destination', 'Created at', 'Updated at']
df = df.query('Value > 0')[columns]
del columns[0]
for column in columns:
    sf = df.groupby(['User'])[column].apply(list)
    new_df = pd.DataFrame({'User': sf.index, column: sf.values})
    if df_user_destination.empty:
        df_user_destination = new_df
    else:
        df_user_destination = pd.merge(df_user_destination, new_df, on='User', how='outer')
df_user_destination = df_user_destination.rename(columns={'Destination': 'Destination [User destinations]', 'Created at': 'Created at [User destinations]', 'Updated at': 'Updated at [User destinations]', 'Value': 'Value [User destinations]'})
    # join
df_user = pd.merge(df_user, df_user_destination_offset, on='User', how='outer')
df_user = pd.merge(df_user, df_user_destination, on='User', how='outer')
    # save
df_user.to_csv('./datas/user.csv', encoding='utf-8', index=False)


# destination
df = pd.read_csv('./tables/destination.csv', sep=',')
df_destination = df
    # save
df_destination.to_csv('./datas/destination.csv', encoding='utf-8', index=False)
