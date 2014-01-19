from flask import Flask, render_template, request
from pymongo import MongoClient
from collections import OrderedDict
import gridfs
import string
import random

client = MongoClient('127.0.0.1', 27017)
db = client.test
collection = db.testData
fs = gridfs.GridFS(db, collection='testData')
app = Flask(__name__)

@app.route('/update', methods=['POST', 'GET'])
def update():
	ranid = request.values.get('ranid', None)
	print ranid
	item = request.values.get('item', None)
	print item
	print collection.update({"id": str(ranid), "Item":str(item)},{'$set': {"bought": 1}});
	return 'hello' 
	

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@app.route("/view", methods=['POST', 'GET'])
def view():
	ranid = request.form['ranid']
	wishlist = collection.find( { "id": ranid }, { "Item": 1, "bought": 1 }).sort("num", 1 )
	items = OrderedDict()
	for item in wishlist:
		 items[item['Item']] = item['bought']
		 print item['Item']
	print items
	return render_template('view.html', items = items, ranid=ranid) 

@app.route("/storeCreate", methods=['POST', 'GET'])
def store():
	ranid = id_generator()
	string = request.form['list']
	string = string.replace('\r', '')
	i=0
	for item in string.split('\n'):
		post = {"Item": str(item), "id": ranid, "num": i, "bought": 0}
		collection.insert(post)
		i+=1
	return render_template('storeCreate.html', ranid=ranid)

@app.route("/create", methods=['POST', 'GET'])
def create():
	return render_template('create.html')

@app.route("/", methods=['POST', 'GET'])
def hello():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='true')
