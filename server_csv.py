import pandas
import os

# Create a serverlist.csv file if it doesn't exist
def create_serverlist():
    if not os.path.exists('serverlist.csv'):
        df = pandas.DataFrame(columns=['group', 'server_id', 'server_name', 'game_type'])
        df.to_csv('serverlist.csv', index=False)

# Add group to the dataframe as a column with increasing values
def add_group():
    df = pandas.read_csv('serverlist.csv')
    df['group'] = pandas.Series(range(1, len(df) + 1))
    df.to_csv('serverlist.csv', index=False)


# Add a new row to the dataframe with the given values only if the group does not have n number of servers
def add_row(group, server_id, server_name, game_type, group_size):
    df = pandas.read_csv('serverlist.csv')
    if len(df[df['group'] == group]) < group_size:
        df.loc[len(df)] = [group, server_id, server_name, game_type]
        df.to_csv('serverlist.csv', index=False)
        return True
    return False

# Iterate through the groups and add a new row to the dataframe for each group
def add_rows(server_id, server_name, game_type, group_size=3):
    for i in range(1, 11):
        if add_row(i, server_id, server_name, game_type, group_size) == True:
            print("Added row for group " + str(i))
            return
        else:
            print("Group " + str(i) + " is full")

def get_server_id_group(server_id):
    df = pandas.read_csv('serverlist.csv')
    return df[df['server_id'] == server_id]['group'].values[0]

