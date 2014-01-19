from flask import Flask, render_template, request
from pymongo import MongoClient
import gridfs
import string
import random

client = MongoClient('127.0.0.1', 27017)
db = client.test
collection = db.testData
fs = gridfs.GridFS(db, collection='testData')
app = Flask(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@app.route("/view", methods=['POST', 'GET'])
def view():
	ranid = request.form['ranid']
	# wishlist = collection.find_one({"id": ranid})
	wishlist = [] 
	line = fs.get_version(ranid).read()
	line.replace('\r', '')
	for item in line.split('\n'):
		wishlist.append(item)
	return render_template('view.html', wishlist = wishlist) 

@app.route("/storeCreate", methods=['POST', 'GET'])
def store():
	ranid = id_generator()
	string = request.form['list']
	a = fs.put(str(string), filename=ranid)
	# post = {"WishList": string, "id": ranid}
	# post_id = collection.insert(post)
	return render_template('storeCreate.html', ranid=ranid)

@app.route("/create", methods=['POST', 'GET'])
def create():
	return render_template('create.html')

@app.route("/", methods=['POST', 'GET'])
def hello():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='true')
