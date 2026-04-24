from flask import Flask, render_template, url_for, redirect, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/livros')
def cadastrar():
    #por enquanto tá funcionando só p admin, ai qunado tiver o p gnt normal, tem q colocar um condicional aq 
    return redirect (url_for('cadastro_livros'))

@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastro_livros():

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']

        # lê o arquivo json
        with open('livros.json', 'r', encoding='utf-8') as f:
            livros = json.load(f)

        livros.append({
            'titulo': titulo,
            'autor': autor,
            'ano': ano,
            'genero': genero
        })

        # salva no arquivo json
        with open('livros.json', 'w', encoding='utf-8') as f:
            json.dump(livros, f, indent=4, ensure_ascii=False)

    # lê o arquivo json p poder mostrar os cadastrados
    with open('livros.json', 'r', encoding='utf-8') as f:
        livros = json.load(f)

    return render_template('livros.html', livros=livros) 