from flask import Flask, render_template, request
from pymongo import MongoClient
import gridfs
import string
import random

client = MongoClient('127.0.0.1', 27017)
db = client.test
collection = db.testData
app = Flask(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@app.route("/view", methods=['POST', 'GET'])
def view():
	ranid = request.form['ranid']
	wishlist = collection.find_one({"id": ranid})
	return render_template('view.html', wishlist = str(wishlist['WishList'])) 

@app.route("/storeCreate", methods=['POST', 'GET'])
def store():
	ranid = id_generator()
	print str(request.form)
	string = request.form['list']
	post = {"WishList": string, "id": ranid}
	post_id = collection.insert(post)
	return render_template('storeCreate.html', ranid=ranid)

@app.route("/create", methods=['POST', 'GET'])
def create():
	return render_template('create.html')

@app.route("/", methods=['POST', 'GET'])
def hello():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='true')
