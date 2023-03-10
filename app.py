#Intern Imports 
from install import Installer
import os
import os.path
from time import sleep
from xmlrpc.client import boolean
import sqlite3
from platform import system

#Directory files path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.instagram.com/"

PATH_CHROMEDRIVER = os.path.join(BASE_DIR, "chromedriver.exe")
PATH_CHROMEDRIVER_OSX = os.path.join(BASE_DIR, "chromedriver_OSX")
PATH_REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")
PATH = os.path.join(BASE_DIR, "db.sqlite")

#Running Installer for external imports
Installer.RunInstaller(PATH_REQUIREMENTS)

#External imports
import clipboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import selenium
from pyautogui import press
from pyautogui import hotkey

#Variables
OS = system()
sqliteConnection = sqlite3.connect("db.sqlite")
cursor = sqliteConnection.cursor()

options_chrome = Options()
options_chrome.add_argument("--disable-notifications") # disabling notifications in chrome settings

if(OS == 'Windows'):
    service = ChromeService(os.path.join(BASE_DIR, "chromedriver.exe"))
else:
    service = ChromeService(os.path.join(BASE_DIR, "chromedriver_OSX"))


def isEmptyClipboard():
    if not clipboard.paste():
        return True
    return False


#Exceptions
class EmptyClipboard_ERROR(Exception):
    __exception_message = "\n\nClipboard is empty! Please copy the message in your clipboard"
    
    def __init__(self, empty_clipboard, message=__exception_message):
        self.empty_clipboard = empty_clipboard
        self.message = str.upper(message)
        super().__init__(self.message)
        

#Controlling IG Profile Class
class ProfileControl():
    def LogInPopUpDown(self):
        try:
            for i in range(7):
                press('tab')
    
            press('enter')
            
        except TypeError:
            return ProfileControl.LogInPopUpDown()

    def WriteMessage(self):
        if(OS == 'Windows'):
            hotkey("ctrl", "v")
        else:
            hotkey("command", "v")

    def SendMessage(self):
        press('enter')

#Database Class
class Database(object):
    def __init__(self, PATH ,cursor, sqliteConnection):
        self.PATH = PATH
        self.sqliteConnection = sqliteConnection
        self.cursor = cursor
    
    def __createconnection(self):
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
try:
    
    if(isEmptyClipboard() == True):
        raise EmptyClipboard_ERROR(isEmptyClipboard())
    
    username_host = str(input("Enter the host accounts username: "))
    print("\n")
    password_host = input("Enter the host accounts password: ")
    print("\n")

    
    service.start()
    
    Db = Database(PATH, cursor, sqliteConnection)
    PFC = ProfileControl()
    DRIVER = webdriver.Remote(service.service_url, desired_capabilities = webdriver.DesiredCapabilities.CHROME, options=options_chrome)

    # accounts = []
    # for i in range(len(accounts)):
    #     Db.InsertData("AccountsTable", accounts[i])
    # print("Data Inserted")

    data_list = []
    data = Db.SelectData("AccountsTable")

    for row in data:
        data_list.append(str(row))


    DRIVER.get(BASE_URL)

    sleep(3)
    PFC.LogInPopUpDown()
    sleep(2.5)

    username = DRIVER.find_element(by="css selector", value="input[name='username']")
    password = DRIVER.find_element(by="css selector", value="input[name='password']")

    username.clear()
    password.clear()

    username.send_keys(username_host)
    password.send_keys(str(password_host))

    login = DRIVER.find_element(by="css selector", value="button[type='submit']")
    login.click()

    print("\n\n")
    sleep(10)

    for i in range(len(data_list)):
        
        username = data_list[i][2:][:len(data_list[i]) - 5]
        
        url = BASE_URL + str(username)
        DRIVER.get(url)
        sleep(10)
        
        for i in range(12):
            press('tab')

        press('enter')

        sleep(5)
        PFC.WriteMessage()

        sleep(1)
        PFC.SendMessage()
        sleep(3)

        if(i >= len(data_list)):
            service.stop()
            print(username, end="\n\n")
            print("All messages have been sent!")
        else:
            DRIVER.get("https://www.instagram.com")
            print(username, end="\n\n")
            sleep(1)
            
except KeyboardInterrupt:
    print("\n\nProgram Stopped due to manual interrupting")
