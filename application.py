from flask import Flask,jsonify,render_template, request, url_for, flash, redirect
from procuraDocente import procuraDocentes, coletarDadosDoBanco
from pegaDadosParaJson import ColetaDadosDoBancoETransformaEmJson
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '9455214A428C8137B01669B6F7CD2AF198E24D29'

@app.route('/')
def raiz():
    return jsonify({
    'retorna-os-dados-do-docente':'/read/nome completo do docente',
    'busca-dados-de-docentes-e-indexa-no-banco': '/create'
    })

@app.route('/rota2')
def rota2():
    return '<h1>Esta é a rota 2!</h1>'

@app.route('/docente/<string:nome>')
def docente(nome):
    return jsonify({'nome':nome})

@app.route('/template')
def index():
    return render_template('index.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        content = request.form['content']
        flash('Deu certo! Iniciando a procura de dados destes: '+ content)
        if not content:
            flash('Ao menos o nome de um docente é necessário')
        else:
            
            listaDeDocentes = content.split(',')
            print(listaDeDocentes)
            procuraDocentes(listaDeDocentes)
            
            flash('Deu certo! Dados coletados dos docentes disponíveis na planilha: '+ content)

    return render_template('create.html')

@app.route('/read/<string:docente>')
def dadosdocentes(docente):
    listaJson = ColetaDadosDoBancoETransformaEmJson(docente)
    return jsonify(listaJson)


# app.run(debug=True)