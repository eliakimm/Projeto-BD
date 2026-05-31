from flask import Flask
from database.conexao import conectar

app = Flask(__name__)

@app.route("/")
def home():

    conexao = conectar()
    return ('<h1 style= "color: red; text-align: center" >Usando o modo de depuração do flask!!!</h1>'
            '<p style= "color: red; text-align: center">Testando paragrafos</p>')

app.run(debug=True)