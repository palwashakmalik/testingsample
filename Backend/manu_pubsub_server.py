import redis
import sqlite3
import json

conn = sqlite3.connect('Manufacturer.db')
cursor = conn.cursor()
# manufacturer server
manufacturer = redis.Redis(host='localhost', port=6379, db=0)
manufacturer=manufacturer.pubsub()
manufacturer.subscribe('dwatson_f10')

for message in manufacturer.listen():
    print(message)
    if (type(message['data'])!=int):
        order = json.loads(message['data'])
        medName=order['MedicineName']
        OrderID = 123
        OrderStatus = 'Delayed'
        cursor.execute("SELECT Quantity FROM ManufacturerInventory where MedName=?", (medName,))
        Inventory_Quantity = cursor.fetchone()
        Inventory_Quantity = int(''.join(map(str, Inventory_Quantity)))
        cursor.execute("SELECT MedCategory FROM ManufacturerInventory where MedName=?", (medName,))
        MedCategory = cursor.fetchone()
        MedCategory = ''.join(MedCategory)
        if Inventory_Quantity < order['Quantity']:
            delayed_order = {'manu': 'manu1','OrderID': OrderID,'quantity': order['Quantity'],
                             'MedName':medName,'deliveryTime': '13 week','OrderStatus':OrderStatus,'MedCategory':MedCategory}
            manufacturer = redis.Redis(host='localhost', port=6379, db=0)
            manufacturer.publish('dwatson_f10-delayed', json.dumps(delayed_order))
        else:
            saleID=123
            OrderStatus='Confirmed'
            cursor.execute("SELECT BatchID FROM ManufacturerInventory where MedName=?", (medName,))
            BatchID = cursor.fetchone()
            BatchID = int(''.join(map(str, BatchID)))
            cursor.execute("SELECT MedID FROM ManufacturerInventory where MedName=?", (medName,))
            MedID = cursor.fetchone()
            MedID = int(''.join(map(str, MedID)))
            sale_Order = {'manu': 'manu1','OrderID': saleID,'quantity': order['Quantity'], 'MedName':medName,'deliveryTime': '1 week'
                ,'BatchID': BatchID,'MedId': MedID,'OrderStatus':OrderStatus,'MedCategory':MedCategory}
            manufacturer = redis.Redis(host='localhost', port=6379, db=0)
            manufacturer.publish('dwatson_f10-sale', json.dumps(sale_Order))

