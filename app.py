from flask import Flask, render_template, url_for, redirect, request, session
import json

app = Flask(__name__)
app.secret_key = 'segredo'

usuarios = {}

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

@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')

        usuarios[user] = senha 

        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')

        if user in usuarios and usuarios[user] == senha:
            session['usuario'] = user
            return redirect(url_for('index'))
        
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    user = session['usuario']
    senhaf ="*" * len(usuarios[user])
    return render_template('perfil.html' , usuario=user , senha=senhaf)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
       app.run(debug=True)