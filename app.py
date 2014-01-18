from flask import Flask, render_template, request
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)

app = Flask(__name__)

@app.route("/storeCreate", methods=['POST', 'GET'])
def store():
	string = request.form['list']
	db = client.test
	collection = db.testData
	col = []
	for thing in collection.find():
		col.append(thing)
	return str(col)

@app.route("/create", methods=['POST', 'GET'])
def create():
	return render_template('create.html')

@app.route("/", methods=['POST', 'GET'])
def hello():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='true')
