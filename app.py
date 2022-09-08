from flask import Flask, abort, request
 
app = Flask(__name__)
 
database = {}

#Método GET
@app.route("/")
def home():   
   return "Olá, Tera!"

#Método POST
@app.route("/user", methods=["POST"])
def create_user():
   data = request.json
   name = data.pop("nome")
   database[name] = data
   return "olá, Tera!"

#Obtendo dados salvos pelo POST
@app.route("/user/<string:name>")
def  get_user(name):
    if not name in database:
        abort(404)
    
    data["nome"] = name
    data = database[name]
    return data

#PUT - Atualização do usuário 
@app.route("/user/<string:name>", methods=["PUT"])
def update_user(name):
   if name not in database:
       abort(404)
 
   data = request.json
   database[name] = data
   return data

#DELETE
@app.route("/user/<string:name>", methods=["DELETE"])
def delete_user(name):
   if name not in database:
       abort(404)
 
   del database[name]
   return "Usuário excluído", 200
   
if __name__ == "__main__":
   app.run(debug=True)
