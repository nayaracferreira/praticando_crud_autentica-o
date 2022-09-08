# Antes de rodar, executa ´pip install flask-login´
from dataclasses import dataclass
from flask import Flask, abort, request, render_template
# Importamos a biblioteca flask-login
from flask_login import(
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash
 
login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)

app.config["SECRET_KEY"] = "secret"

@dataclass
class User:
   username: str
   password: str
   is_active: bool = True
   is_anonymous: bool = False
   is_authenticated: bool = True
 
   def get_id(self):
       return self.username

#Banco de dados com usuário padrão que será uma instância da class User informada acima.
#Essa classe vai possuir uma senha que vai ser gerada pelo HASH
database = {"fnay": User("fnay", generate_password_hash("321"))}
 
@app.route("/user", methods=["POST"])
def create_user():
   data = request.json
   data["password"] = generate_password_hash(data["password"])
   return f"olá, {data['username']}"

@app.route("/user/<string:name>", methods=["GET"])
def read_user(name):
   if name not in database:
       abort(404)
 
   data = database[name]
   data["nome"] = name
   return data

#Obter um usuário
# Para proteger uma rota usamos require e construimos a rota normalmente
@login_required
@app.route("/user/<string:name>", methods=["GET"])
def read_user(name):
    #Podemos reagir ao fato do usuário não ter logado, ou se estiver logado mas com usuário diferente do que está pedindo, teremos o erro 403
   if not current_user.is_authenticated or current_user.username != name:
       abort(403)
    #Se o nome não exitir no banco de dados teremos o erro 404
   if name not in database:
       abort(404)
 #Caso tudo estiver correto irá aparecer as informações 
   data = database[name]
   return f"Olá, {data.username}"

#A rota de login irá aceitar dois métodos o GET(requisição de login) e o POST(envia as informações de login)
@app.route("/login", methods=["GET", "POST"])
def login():
    #Vai reagir quando estiver inspecionando o método GET
   if request.method == "GET":
    #No método GET nós iremos imprimir um formulário com o usuário e a senha
       return """
              <form action='login' method='POST'>
               <input type='text' name='username' id='username' placeholder='username'/>
               <input type='password' name='password' id='password' placeholder='password'/>
               <input type='submit' name='submit'/>
              </form>
              """
   #Quando estivermos fora do método GET iremos extrair o nome do usuário dos dados do formulário e determinar se existe um usuário com aquele nome no nosso banco de dados
   username = request.form.get("username")
   user = database.get(username)
 
 #Se existir e a senha fornecida também for igual nós iremos logar no usuário e retornar com a mensagem Login com sucesso!, caso contrário "Login falhou"
   if user and check_password_hash(user.password, request.form.get("password")):
       login_user(user)
       return "Login com sucesso!"
   else:
       return "Login falhou"

#Nesse será aceito a chamada do logout, e vai chamar a função logout user da biblioteca de autenticação, retonando o valor "Usuário deslogado"
@app.route("/logout")
def logout():
    logout_user()
    return "Usuário deslogado"

if __name__ == "__main__":
   app.run(debug=True)
