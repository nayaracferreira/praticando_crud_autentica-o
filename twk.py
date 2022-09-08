# Antes de rodar, executa ´pip install flask-login´
from dataclasses import dataclass
from flask import Flask, abort, request, render_template
# Ao invés de flask-login utilizaremos flask-jwt
#Essa biblioteca utiliza um dos diversos padrões de autenticação por token, nesse caso o json web token.
from flask_jwt import JWT, jwt_require, current_identify
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

@dataclass
class User:
   username: str
   password: str
   is_active: bool = True
   is_anonymous: bool = False
   is_authenticated: bool = True
 
# Aqui colocamos essa propriedade
   @property 
   def id(self):
       return self.username

database = {"fnay": User("fnay", generate_password_hash("321"))}

# Incluimos um outro tipo de autenticação 
# Essa parte substitui a parte do formulário do anterior
def authenticate(username, password):
    user = database.get(username, None)
    if user and check_password_hash(user.password, password):
        return user

def identify(playload):
    user_id = playload["identify"]
    return database.get(user_id, None)

# A rota de Autenticação vem dessa linha, onde a gente pede para que a rota jwt embrulhe o app
jwt = JWT(app, authenticate, identify)


@app.route("/user", methods=["POST"])
def create_user():
   data = request.json
   data["password"] = generate_password_hash(data["password"])
   return f"olá, {data['username']}"

@app.route("/user/<string:name>", methods=["GET"])
# A autenticação de uma rota através de login é feita através da atribuição JWT
@jwt_require()
def read_user(name):
   return current_identify.username

if __name__ == "__main__":
   app.run(debug=True)
"""
Comandos de login:
Use o HTTPIE para testar!

http localhost:5000/auth username=fbidu password=123 --> Isso irá te dar um token
http localhost:5000/user/fbidu --> Falha com 401
http localhost:5000/user/fbidu Authorization:"JWT <token>" _ Sucesso!
"""   
