import pyodbc
import os
import datetime

class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
    
    def insert_server(self, server_id, server_name, prefix):
        self.cursor.execute(''' 
            INSERT INTO servers (server_id, server_name, prefix)
            VALUES (?, ?, ?);
        ''', server_id, server_name, prefix)
        self.conn.commit()

    def insert_activity(self, server_id, server_name, channel_id, channel_name, user_name, user_id, command, turn_count, attachment_url):
        self.cursor.execute('''
            INSERT INTO activity (server_id, server_name, channel_id, channel_name, user_name, user_id, command, turn_count, attachment_url, sent_date, sent_time)
            VALUES (?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?);
        ''', server_id, server_name, channel_id, channel_name, user_name, user_id, command, turn_count, attachment_url, str(datetime.date.today()), str(datetime.datetime.now().time())) 
        self.conn.commit()

    def select_activity(self):
        self.cursor.execute('SELECT * FROM activity')
        results = self.cursor.fetchall()
        return results