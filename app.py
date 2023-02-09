#Imports 
import os
import json as js
import os.path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import selenium
from pyautogui import press
from pyautogui import typewrite
import platform
# from instabot import Bot
import sqlite3

#Variables
sqliteConnection = sqlite3.connect("db.sqlite")
cursor = sqliteConnection.cursor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
message = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy."
options_chrome = webdriver.ChromeOptions()
PATH_CHROMEDRIVER = os.path.join(BASE_DIR, "chromedriver.exe")
PATH_CHROMEDRIVER_OSX = os.path.join(BASE_DIR, "chromedriver_OSX")
PATH = os.path.join(BASE_DIR, "db.sqlite")

if(platform.system() == 'Windows'):
    service = ChromeService(os.path.join(BASE_DIR, "chromedriver.exe"))
else:
    service = ChromeService(os.path.join(BASE_DIR, "chromedriver_OSX"))

service.start()


#Controlling IG Profile Class
class ProfileControl():
    def LogInPopUpDown(self):
        try:
            press('tab')
            press('tab')
            press('tab')
            press('tab')
            press('tab')
            press('tab')
            press('tab')
            press('enter')
        except TypeError:
            return ProfileControl.LogInPopUpDown()
        
    def SearchProfile(self):
        press('tab')
        press('tab')
        press('tab')
        press('enter')
        
    def GetToAccountMainPage(self):
        press('enter')
        press('enter')
    
    def WriteMessage(self, message):
        typewrite(message)
    
    def SendMessage(self):
        press('enter')
    
    def NotificationPOPUP(self):
        press('tab')
        press('tab')
        press('enter')
        sleep(1)
#Database Class
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

    def __closeconnection(self):
        return self.sqliteConnection.close()
    
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
            
        self.__closeconnection()
    
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
        
        self.__closeconnection()         
    
    def __lookUpData(self, table_from, data):
        self.__createconnection()
        
        try:
            self.cursor.execute(f"SELECT * FROM {table_from}")
            data_look = self.cursor.fetchall()
            self.sqliteConnection.commit()
            
            for i in range(len(data_look)):
                for row in data_look:
                    if row[i] == data:
                        self.__closeconnection()
                        return True
        except IndexError:         
            self.__closeconnection()  
            return False
            
    def Createdatabase(self, table_name, rows: str):
        self.__createconnection()
    
        try:
            Data_Table = f""" CREATE TABLE {table_name} ({rows}) """
            self.cursor.execute(Data_Table)
        except Exception as e:
            print(e)
        
        self.__closeconnection()
        print(f"\nDatabase Created: \nPath: {PATH} \nTable_Name: {table_name}, \nRows: {rows}")

    def find(self, table_from, data):
        return self.__lookUpData(table_from, data)


#MAIN
Db = Database(PATH, cursor, sqliteConnection)
PFC = ProfileControl()
# try:
#     DRIVER = webdriver.Chrome(PATH_CHROMEDRIVER) if platform.system == "Windows" else webdriver.Safari()
# except Exception:
#     DRIVER = webdriver.Chrome(PATH_CHROMEDRIVER)
DRIVER = webdriver.Remote(service.service_url, desired_capabilities = webdriver.DesiredCapabilities.CHROME)
# bot = Bot()
accounts = ["alexandru6041", "tudor.rtf", "alexandru6041"]
for i in range(len(accounts)):
    Db.InsertData("AccountsTable", accounts[i])
print("Data Inserted")
data_list = []
# Db.InsertData("AccountsTable", "alexandru6041")
data = Db.SelectData("AccountsTable")
for row in data:
    data_list.append(str(row))

DRIVER.get("https://www.instagram.com")
# DRIVER.fullscreen_window()
sleep(1)
PFC.LogInPopUpDown()
sleep(2.5)
username = DRIVER.find_element(by="css selector", value="input[name='username']")
password = DRIVER.find_element(by="css selector", value="input[name='password']")
username.clear()
password.clear()
username.send_keys("george_de_la_cnva")
password.send_keys("lvanuagricol")
login = DRIVER.find_element(by="css selector", value="button[type='submit']")
login.click()
sleep(8)
for i in range(len(data_list)):
    username = data_list[i][2:][:len(data_list[i]) - 5]
    PFC.SearchProfile()
    DRIVER.find_element(
        by="class name", value = "_aauy"
        ).send_keys(username)
    sleep(0.5)
    PFC.GetToAccountMainPage()
    sleep(3)
    press('tab')
    press('tab')
    press('enter')
    sleep(2)
    if(i == 0):
        press('tab')
        press('tab')
        press('enter')
    sleep(3)
    PFC.WriteMessage(message)
    sleep(0.2)
    PFC.SendMessage()
    sleep(3)
    if(i >= len(data_list)):
        service.stop()
        print(username, end="\n")

    else:
        DRIVER.get("https://www.instagram.com")
        print(username, end="\n")
        sleep(1)
    # sleep(2)
    # press('enter')
    # press('enter')
    # sleep(2)
    # press('tab')
    # press('tab')
    # press('enter')
    # sleep(3)
    # print("ok")
    # typewrite(message)
    # sleep(3)
    # print("message typed")
    # press('enter')
    print(username, end="\n")
    

# data = Db.SelectData("AccountsTable")
# print(data)
# Rows = "Username VARCHAR(50) NOT NULL"
# Db.Createdatabase("AccountsTable", Rows)
# Db.DeleteData("AccountsTable", "__maria_bianca__", "WHERE Username = ?")

# bot = Bot()
# bot.login(username=userId, password=Pass)
# print("ok")