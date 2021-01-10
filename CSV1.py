import sqlite3


con = sqlite3.connect("Products.sqlite")
cursor = con.cursor()

cursor.execute('''
Select * from Produse
''')
produse = cursor.fetchall()
for produs in produse:
    if produs[0] == "Whiskey":
        image_id = 7
    elif produs[0] == "Liqueurs":
        image_id = 3
    elif produs[0] == "Vodka":
        image_id = 6
    elif produs[0] == "Fruits":
        image_id = 1
    elif produs[0] == "Rum":
        image_id = 4
    elif produs[0] == "Gin":
        image_id = 2
    elif produs[0] == "Tequila":
        image_id = 5
    else:
        image_id = 8

    cursor.execute('''
    INSERT INTO Produs (image_id, category_name, item_description, vendor_name, bottle_size, bottle_price) VALUES (?, ?, ?, ?, ?, ?)
    ''', (image_id,)+produs)
con.commit()

