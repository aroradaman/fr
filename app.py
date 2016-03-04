import json
import time
import hashlib
from random import randrange
from flask import Flask, request

def md5(inpt) :
	m = hashlib.md5()
	m.update(str(inpt))
	return  m.hexdigest()

users = set()
credentials = {}
data = {}

app = Flask(__name__)

@app.route("/register",methods=["POST"])
def register():
	user_email = request.form["email"]
	user_password = request.form["password"]
	users.add(user_email)
	credentials.update({user_email:user_password})
	return "true"

@app.route("/login",methods=["POST"])
def login():
	user_email = request.form["email"]
	user_password = request.form["password"]
	if user_email in users :
		if credentials[user_email] == user_password :
			return "true"
		else :
			return "false"
	else :
		return "false"
	

@app.route("/update",methods=['POST'])
def update():	
	status = request.form["status"]
	unq_id = request.form["id"]
	if unq_id in data :
		data[unq_id]['status'] = status
		return "true"
	else :
		return "false"
	

@app.route("/search",methods=['POST'])
def search():
	new_data = []
	for unq_id,val in data.iteritems() :
		val.update({'id':unq_id})
		new_data.append(val)
	return json.dumps({
		'list' : new_data,
		'count':len(new_data)
	})
	

@app.route("/insert",methods=['POST'])
def insert():
	lat = float(request.form["lat"])
	lng = float(request.form["lng"])
	description = request.form["description"]
	status = request.form["status"]
	name = request.form["name"]
	unq_id = md5(str(time.time() *1000) + '__BOOM_SHIVA__' + str(randrange(100000,999999)))
	data.update({ unq_id : {
			'lat' : lat,
			'lng' : lng,
			'description' : description,
			'status' : status,
			'name' : name

		}})
	return str(unq_id)

if __name__ == "__main__":	
	app.run(host='0.0.0.0', port=80,debug=True)
