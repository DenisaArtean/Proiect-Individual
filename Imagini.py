import sqlite3
import CSV


class Imagini():
    def __init__(self):
        self.con = sqlite3.connect("Products.sqlite")
        self.cursor = self.con.cursor()
    def createTableImg(self):
        self.cursor.execute('''
        CREATE TABLE if not exists Imagini(
        id integer primary key autoincrement, 
        imagine blob not null); 
        ''')
    def addImg(self, bytes):
        self.createTableImg()
        self.cursor.execute('''
        Insert Into Imagini(imagine) values (?);
        ''', (bytes,))
        self.con.commit()

    def getCursorAndCon(self):
        return self.cursor, self.con

obj = Imagini()

poze = ['fruits.jpg', 'gin.png', 'liqueurs.jpg', 'Rum.jpg', 'tequila.jpg', 'vodka.jpg', 'whiskey.jpg', 'creme.jpg']
for poza in poze:
    with open(poza, "rb") as f:
        bytes = f.read()
        obj.addImg(bytes)
