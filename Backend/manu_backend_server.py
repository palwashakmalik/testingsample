import redis
import json
import sqlite3
from flask import Flask

app=Flask(__name__)
# Connecting to database
conn = sqlite3.connect('Manufacturer.db')

med_ID=int(input('Enter medicine ID: '))
quantity= int(input('Enter medicine quantity: '))
cursor = conn.cursor()
cursor.execute("SELECT Quantity FROM ManufacturerInventory where MedID=?", (med_ID,))
Inventory_Quantity = cursor.fetchone()
Inventory_Quantity = int(''.join(map(str, Inventory_Quantity)))
cursor.execute("SELECT ReorderPoint FROM ManufacturerInventory where MedID=?", (med_ID,))
ReorderPoint = cursor.fetchone()
ReorderPoint = int(''.join(map(str, ReorderPoint)))


if Inventory_Quantity < ReorderPoint:
    order_id = 80
    order = {'manu': 'manu1', 'order_id': order_id, 'quantity': quantity, 'medID': med_ID}
    query = """Update ManufacturerOrder set OrderID=? where MedID = ?"""
    data = (orderID, med_ID)
    cursor.execute(query, data)
    conn.commit()
    manufacturer = redis.Redis(host='localhost', port=6379, db=0)
    manufacturer.publish('manu1', json.dumps(order))