import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect("Data.sqlite")
        self.cursor = self.con.cursor()
    def __del__(self):
        self.con.close()

    def addAccount(self, username, password, first_name, last_name, email):
        self.createTable()
        self.cursor.execute('''
             insert into usersInfo(Username, Password, First_name, Last_name, Email) values (?,?,?,?,?)
         ''', (username, password, first_name, last_name, email))
        self.con.commit()

    def createTable(self):
        self.cursor.execute('''
            create table if not exists usersInfo(
            Username text primary key not null, 
            Password text not null, 
            First_name text not null, 
            Last_name text not null, 
            Email text not null 
                
            
        )''' )

    def getCursorAndCon(self):
        return self.cursor, self.con
    def delAccount(self):
        pass
    def checkAccount(self):
        pass