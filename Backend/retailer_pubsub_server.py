import redis
import sqlite3
import json
global found

# Connecting to database
conn = sqlite3.connect('Retailer.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

retailer = redis.Redis(host='localhost', port=6379, db=0)
retailer = retailer.pubsub()
retailer.subscribe('dwatson_f10-delayed')
retailer.subscribe('dwatson_f10-sale')

# retailer is getting messages from subscribed channels
for message in retailer.listen():
    print(message)
    if message['channel'] == b'dwatson_f10-delayed':
        if (type(message['data'])!=int):
            delayedOrder = json.loads(message['data'])
            OrderID = delayedOrder['OrderID']
            qty = delayedOrder['quantity']
            deliveryTime = delayedOrder['deliveryTime']
            MedName = delayedOrder['MedName']
            Status=delayedOrder['OrderStatus']
            query = """Update RetailerOrder set OrderId=?, OrderStatus='Confirmed', DeliveryTime=?, Quantity=?, OrderStatus=? where MedName= ?"""
            data = (OrderID, deliveryTime, qty, Status, MedName)
            cursor.execute(query, data)
            conn.commit()

    elif message['channel'] == b'dwatson_f10-sale':
        if (type(message['data'])!=int):
            invoice = json.loads(message['data'])
            SaleID = invoice['OrderID']
            qty = invoice['quantity']
            deliveryTime= invoice['deliveryTime']
            Status = invoice['OrderStatus']
            MedName=invoice['MedName']
            MedID = invoice['MedId']
            BatchID = invoice['BatchID']
            MedCategory=invoice['MedCategory']
            cursor.execute('''SELECT MedName FROM Inventory''')
            result = [dict(row) for row in cursor.fetchall()]
            for i in result:
                if MedName in i['MedName']:
                    found = True
                    break
                else:
                    found = False
            if found:
                query = """Update RetailerOrder set OrderId=?, OrderStatus='Confirmed', DeliveryTime=?, Quantity=?, OrderStatus=? where MedName= ?"""
                data = (SaleID,deliveryTime,qty,Status,MedName)
                cursor.execute(query, data)
                conn.commit()
                cursor.execute("SELECT Stock FROM Inventory where MedName=?", (MedName,))
                stock = cursor.fetchone()
                stock = int(''.join(map(str, stock)))
                stock=stock+qty
                query = """Update Inventory set MedId=?, BatchID=?, Stock=? where MedName= ?"""
                data = (MedID, BatchID, stock, MedName)
                cursor.execute(query, data)
                conn.commit()
            else:
                query = ''' INSERT INTO Inventory(MedName,Stock,MedCategory,MedID,BatchID)
                          VALUES(?,?,?,?,?) '''
                data = (MedName, qty, MedCategory, MedID, BatchID)
                cursor.execute(query,data)
                query1 = """Update RetailerOrder set OrderId=?, OrderStatus='Confirmed', DeliveryTime=?, OrderStatus=? where MedName= ?"""
                data1 = (SaleID, deliveryTime, Status, MedName)
                cursor.execute(query1, data1)
                conn.commit()




