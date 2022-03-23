import redis
import json
import sqlite3
from flask import Flask, request
app=Flask(__name__)



@app.route('/test', methods=["GET", "POST"])
def test_handler():
    print(request.json)
    return json.dumps({"name":"test handler"})

    # manufacturer = redis.Redis(host='localhost', port=6379, db=0)
    # manufacturer.publish('dwatson_f10-sale', json.dumps(sale_Order))

app.run(port=3001)