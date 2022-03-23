import redis
import json
import random
import time
import sqlite3
from flask import Flask

app=Flask(__name__)
@app.route('/test', methods=["GET", "POST"])
def test_handler():
   return json.dumps({"name":"test handler"})

# Connecting to database
conn = sqlite3.connect('Retailer.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

@app.route("/Place_Order")
def manualOrder():
    global found
    MedName=input('Enter medicine name: ')
    Quantity = int(input('Enter order quantity: '))
    cursor.execute('''SELECT MedName FROM Inventory''')
    result = [dict(row) for row in cursor.fetchall()]
    for i in result:
        if MedName in i['MedName']:
            found=True
            break
        else:
            found=False
    if found:
        cursor.execute("SELECT Stock FROM Inventory where MedName=?",(MedName,))
        stock=cursor.fetchone()
        stock = int(''.join(map(str, stock)))
        cursor.execute("SELECT ReorderStockPoint FROM Inventory where MedName=?",(MedName,))
        Reorder_point=cursor.fetchone()
        Reorder_point = int(''.join(map(str, Reorder_point)))
        cursor.execute("SELECT MedCategory FROM Inventory where MedName=?",(MedName,))
        MedCategory=cursor.fetchone()
        MedCategory = ''.join(MedCategory)
        cursor.execute("SELECT RetailerLoc FROM RetailerIdentity left JOIN Inventory "
                       "on Inventory.RetailerID=RetailerIdentity.RetailerID and MedName=?",(MedName,))
        RetailerLoc=cursor.fetchone()
        RetailerLoc= ''.join(RetailerLoc)
        cursor.execute("SELECT RetailerName FROM RetailerIdentity left JOIN Inventory "
                       "on Inventory.RetailerID=RetailerIdentity.RetailerID and MedName=?",(MedName,))
        RetailerName=cursor.fetchone()
        RetailerName= ''.join(RetailerName)
        # generating order
        if stock < Reorder_point:
            order={'MedicineName': MedName, 'MedCategory':MedCategory,
                   'Quantity': Quantity, 'RetailerLoc': RetailerLoc,'RetailerName':RetailerName}
            retailer = redis.Redis(host='localhost', port=6379, db=0)
            retailer.publish('dwatson_f10', json.dumps(order))
    else:
        MedCategory=input('Enter Medicnie Category:')
        query = ''' INSERT INTO RetailerOrder(MedName,Quantity,MedCategory)
          VALUES(?,?,?) '''
        data=(MedName,Quantity,MedCategory)
        cursor.execute(query,data)
        conn.commit()
        cursor.execute("SELECT RetailerLoc FROM RetailerIdentity")
        RetailerLoc = cursor.fetchone()
        RetailerLoc = ''.join(RetailerLoc)
        cursor.execute("SELECT RetailerName FROM RetailerIdentity")
        RetailerName = cursor.fetchone()
        RetailerName = ''.join(RetailerName)
        order = {'MedicineName': MedName, 'MedCategory': MedCategory,
                 'Quantity': Quantity, 'RetailerLoc': RetailerLoc, 'RetailerName': RetailerName}
        retailer = redis.Redis(host='localhost', port=6379, db=0)
        retailer.publish('dwatson_f10', json.dumps(order))


def autoOrder():
    global cursor
    while True:
        cursor.execute('''SELECT * FROM Inventory''')
        for index, row in enumerate(cursor):
            data = dict(row)
            print(data)
            MedName = row['MedName']
            MedCategory = row['MedCategory']
            Stock = row['Stock']
            ReorderPoint=row['ReorderStockPoint']
            Quantity=100
            RetailerID=row['RetailerID']
            cursor = conn.cursor()
            RetailerLoc=cursor.execute("SELECT RetailerLoc FROM RetailerIdentity left JOIN Inventory "
                                       "on Inventory.RetailerID=RetailerIdentity.RetailerID and MedName=?",
                (MedName,)).fetchone()
            RetailerLoc= ''.join(RetailerLoc)
            RetailerName= cursor.execute("SELECT RetailerName FROM RetailerIdentity left JOIN Inventory "
                                         "on Inventory.RetailerID=RetailerIdentity.RetailerID and MedName=?",
                 (MedName,)).fetchone()
            RetailerName= ''.join(RetailerName)
            if Stock < ReorderPoint:
                order={'MedicineName': MedName, 'MedCategory':MedCategory,
                       'Quantity': Quantity, 'RetailerLoc': RetailerLoc,'RetailerName':RetailerName}
                retailer = redis.Redis(host='localhost', port=6379, db=0)
                retailer.publish('dwatson_f10', json.dumps(order))
            time.sleep(0.5)
