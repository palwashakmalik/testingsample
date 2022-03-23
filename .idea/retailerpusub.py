#retailer pubsub server
import redis 
sql_db = sql_connect('localhost', 22983)

redis_conn = Redis.connect('localhost')


redis_conn.subscribe('dwatson_f10-delayed')
redis_conn.subscribe('dwatson_f10-sale')

for message in redis_conn.listen():
  if message['topic'] == 'dwatson_f10-delayed':
    delayed_order = JSON.loads(message['data'])
    manufacturer = delayed_order['manu']
    order_id = delayed_order['order_id']
    delay = delayed_order['delay']
    sql_db.update('orders', order_id, {'status': "delayed", 'delivery_time': delay})
    
  elif message['topic'] == 'dwatson_f10-sale':
    invoice = JSON.loads(message['data'])
    sale_id = delayed_order['sale_id']
    drug_id = delayed_order['drug_id']
    qty = delayed_order['qty']

    inventory_row = sql_db.get('inventory', drug_id)
    if inventory_row['reorder_point'] > inventory_row['qty']:
      redis_conn.publish(inventory_row['manu'], some_order)
      
