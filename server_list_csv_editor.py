import pandas as pd
import os


def create_serverlist():
    if not os.path.exists('serverlist.csv'):
        df = pd.DataFrame(columns=['group', 'server_id', 'server_name', 'game_type'])
        df.to_csv('serverlist.csv', index=False)

def add_group():
    df = pd.read_csv('serverlist.csv')
    df['group'] = pd.Series(range(1, len(df) + 1))
    df.to_csv('serverlist.csv', index=False)

def add_row(group, server_id, server_name, game_type, group_size):
    df = pd.read_csv('serverlist.csv')
    if len(df[df['group'] == group]) < group_size:
        df.loc[len(df)] = [group, server_id, server_name, game_type]
        df.to_csv('serverlist.csv', index=False)
        return True
    return False

def add_rows(server_id, server_name, game_type, group_size=3):
    for i in range(1, 11):
        if add_row(i, server_id, server_name, game_type, group_size) == True:
            print("Added row for group " + str(i))
            return
        else:
            print("Group " + str(i) + " is full")

def get_server_id_group(server_id):
    df = pd.read_csv('serverlist.csv')
    return df[df['server_id'] == server_id]['group'].values[0]