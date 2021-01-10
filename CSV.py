import csv, sqlite3

class Produse:
    def __init__(self):
        self.con = sqlite3.connect("Products.sqlite")
        self.cursor = self.con.cursor()
    def __del__(self):
        self.con.close()
    def openCSV(self):
        with open('Products.csv', 'r') as fin:
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['category_name'], i['item_description'], i['vendor_name'], i['bottle_size'], i['bottle_price'])
                     for i in dr]
            print(to_db)
            for tpl in to_db:
                self.cursor.execute(
                    "INSERT INTO Produse (category_name, item_description, vendor_name, bottle_size, bottle_price) VALUES (?, ?, ?, ?, ?);",tpl)
        self.con.commit()
    def createTable(self):
        self.cursor.execute("CREATE TABLE if not exists Produse (category_name, item_description, vendor_name, bottle_size, bottle_price);")
    def getCursorAndCon(self):
        return self.cursor, self.con


