from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId

#Configuracion del servidor
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/restapipython'
mongo = PyMongo(app)

#Ruta crear usuario
@app.route('/users', methods=['POST'])
#Funcion crear usuario
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email :
        #cifrar la contraseña
        hash_password = generate_password_hash(password)
        #Insertar usuario a mongodb
        id = mongo.db.users.insert(
            {
                'username' : username,
                'password' : hash_password,
                'email' : email
            }
        )
        response = {
            'id' : str(id),
            'username' : username,
            'password' : hash_password,
            'email' : email
        }
        return response
    else:
        
        return {'message' : 'Faltan ingresar datos'}

#Ruta listar usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

#Ruta listar 1 usuario
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id' : ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

#Eliminar usuario
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id' : ObjectId(id)})
    response = jsonify({
        'message' : 'Usuario: ' + id + ' eliminado'
    })
    return response

#Actualizar usuario
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email :
        hash_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id' : ObjectId(id)}, 
            {'$set' : {
                'username' : username,
                'password' : hash_password,
                'email' : email
            }})
        response = jsonify({
            'message': 'Usuario: ' + id + ' Actualizado'
        })
        return response

#Manejador de error
@app.errorhandler(404)
def not_found(error=None):
    
    response = jsonify({
        'message' : 'Pagina no encontrada: ' + request.url,
        'status' : 404
    })
    response.status_code = 404
    return response

#Ejecutar la aplicacion
if __name__ == "__main__":
    app.run(debug=True)