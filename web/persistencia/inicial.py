from flask import Flask, render_template, request
from aluno import *

lista = [Aluno('Leandro','17')]

app = Flask(__name__)

@app.route('/')
def listar_alunos():
    return render_template('listar_alunos.html', alunos=Aluno.select())

@app.route('/form_cadastro')
def abrir_form():
    return render_template('form_cadastrar_aluno.html')

@app.route('/cadastrar')
def cadastrar():
    nome = request.args.get('nome')
    idade = request.args.get('idade')
    Aluno.create(nome=nome, idade=idade)

    return listar_alunos()

@app.route('/excluir_aluno')
def excluir():
    count = None
    nome = request.args.get('nome')
    for a in lista:
        if a.nome == nome:
            count = lista.index(a) # count = a
            break
    if count is not None:
        lista.pop(count)   # lista.remove(a)
        return listar_alunos()


app.run(debug=True)