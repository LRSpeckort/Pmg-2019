from flask import Flask, jsonify
from playhouse.shortcuts import model_to_dict
from classes import *

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bem-vindo ao BACKEND"

@app.route("/listar_turmas")
def listar_turmas():
    turmas = list(map(model_to_dict, Turma.select()))
    return jsonify ({'lista' :turmas})

app.run(debug=True, port=4999)