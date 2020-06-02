from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost/pythonmongodb'

mongo = PyMongo(app)


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': f"Resource Not Found {request.url}",
        'status': 404
    })
    response.status_code = 404
    return response

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'welcome to my rest api with mongo'
    })

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username'] # iden
    password = request.json['password'] # es necesario encriptar y necesitamos el modulo werkzeug.security
    email = request.json['email']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert({'username':username, 'password':hashed_password, 'email':email})
        return {'id':str(id), 'username':username, 'password':hashed_password, 'email':email}
    else:
        return not_found()
    return {'message':'received'}

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find() # en el fondo retorna un bson, necesitamos parcear con otro modulo
    response = json_util.dumps(users) # bson a json
    return Response(response, mimetype='application/json') # especificamos la cabecera

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify({
        'message': f"User {id} was deleted successfully."
    })
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username'] # iden
    password = request.json['password'] # es necesario encriptar y necesitamos el modulo werkzeug.security
    email = request.json['email']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':{
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({
            'message': f"User {id} was updated successfully."
        })
        return response

if __name__ == "__main__":
    app.run(debug=True)