#Imports 
import os
import os.path
from instabot import Bot
import sqlite3

#Variables
sqliteConnection = sqlite3.connect("db.sqlite")
cursor = sqliteConnection.cursor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "db.sqlite")

#Database Class API
class Database(object):
    def __init__(self, PATH ,cursor, sqliteConnection):
        self.PATH = PATH
        self.sqliteConnection = sqliteConnection
        self.cursor = cursor
    
    def __createconnection(self):
        error = None
        
        try:
            self.sqliteConnection = sqlite3.connect(self.PATH)
            self.cursor = self.sqliteConnection.cursor()
        
        except sqlite3.Error as e:
            print(e)

    def InsertData(self, table_to, data):
        self.__createconnection()
        
        if(self.__lookUpData(table_to, data) == True):
            return None
        
        try:
            self.cursor.execute(f"INSERT INTO {table_to} VALUES (?)", [data])
            self.sqliteConnection.commit()
            print(f"{data} successfully added to database: {self.PATH} \ntable_name: {table_to}")    
        except Exception as e:
            print(e)
        
        self.sqliteConnection.close()
    
    def DeleteData(self, table_from, data, condition: str = ""):
        self.__createconnection()
        # self.cursor.execute(f"SELECT * FROM {table_from}")
        if(self.__lookUpData(table_from, data) == False):
            return None
        try:
            self.cursor.execute(f"DELETE FROM {table_from} {condition}", [data])
            self.sqliteConnection.commit()
            print(f"{data} successfully removed from database: {self.PATH} \ntable_name: {table_from}")
        except Exception as e:
            print(e)
            
    def SelectData(self, table_from):
        self.__createconnection()
        
        try:
            self.cursor.execute(f"SELECT * FROM {table_from}")
            data = self.cursor.fetchall()
            # self.sqliteConnection.commit()
            return data
        except Exception as e:
            print(e)
        
        self.sqliteConnection.close()         
    
    def __lookUpData(self, table_from, data):
        self.__createconnection()
        
        try:
            self.cursor.execute(f"SELECT * FROM {table_from}")
            data_look = self.cursor.fetchall()
            self.sqliteConnection.commit()
            
            for i in range(len(data_look)):
                for row in data_look:
                    if row[i] == data:
                        return True
        except IndexError:            
            return False
            
    def Createdatabase(self, table_name, rows: str):
        self.__createconnection()
    
        try:
            Data_Table = f""" CREATE TABLE {table_name} ({rows}) """
            self.cursor.execute(Data_Table)
        except Exception as e:
            print(e)
        
        self.sqliteConnection.close()
        print(f"\nDatabase Created: \nPath: {PATH} \nTable_Name: {table_name}, \nRows: {rows}")

    def find(self, table_from, data):
        return self.__lookUpData(table_from, data)


#MAIN
Db = Database(PATH, cursor, sqliteConnection)
bot = Bot()
data_list = []

data = Db.SelectData("AccountsTable")
for row in data:
    data_list.append(str(row))

for i in range(len(data_list)):
    username = data_list[i][2:][:len(data_list[i]) - 5]
    print(username, end="\n")

# data = Db.SelectData("AccountsTable")
# print(data)
# Rows = "Username VARCHAR(50) NOT NULL"
# Db.Createdatabase("AccountsTable", Rows)
# Db.DeleteData("AccountsTable", "__maria_bianca__", "WHERE Username = ?")

# bot = Bot()
# bot.login(username=userId, password=Pass)
# print("ok")