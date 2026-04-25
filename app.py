from flask import Flask, render_template, url_for, redirect, request, session, flash
import json

app = Flask(__name__)
app.secret_key = 'segredo'
#p diferenciar usuários comuns de admins e separar oq cada um pd fazer 
cod_admin = '2024.1'


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/livros')
def listar_livros():
    #por enquanto tá funcionando só p admin, ai qunado tiver o p gnt normal, tem q colocar um condicional aq 
    if 'usuario' not in session:
        return redirect(url_for('login'))

    with open('livros.json', 'r', encoding='utf-8') as f:
        livros = json.load(f)

    # o bixo d string de consulta q ele pediu
    titulo = request.args.get('titulo')
    genero = request.args.get('genero')

    if titulo:
        livros = [l for l in livros if titulo.lower() in l['titulo'].lower()]

    if genero:
        livros = [l for l in livros if genero.lower() in l['genero'].lower()]

    return render_template('livros.html', livros=livros)

@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastro_livros():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session.get('tipo') != 'admin':
        flash('Apenas administradores podem cadastrar livros')
        return redirect(url_for('listar_livros'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']

        # lê o arquivo json
        with open('livros.json', 'r', encoding='utf-8') as f:
            livros = json.load(f)

        #só pra n poder cadastrar o msm livro duas vezes
        #funciona se estiver escrito igual (n é sensível a letras maiúsculas, ent se a diferença for essa tb n vai deixar cadastrar)
        for livro in livros:
            if livro['titulo'].lower() == titulo.lower() and livro['autor'].lower() == autor.lower():
                flash('Livro já cadastrado')
                return redirect(url_for('cadastro_livros'))

        livros.append({
            'titulo': titulo,
            'autor': autor,
            'ano': ano,
            'genero': genero
        })

        # salva no arquivo json
        with open('livros.json', 'w', encoding='utf-8') as f:
            json.dump(livros, f, indent=4, ensure_ascii=False)

        return redirect(url_for('listar_livros'))

    return render_template('cadastro_livro.html')

@app.route('/excluir_livro/<int:id>')
def excluir (id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session.get('tipo') != 'admin':
        flash('Apenas administradores podem remover livros')
        return redirect(url_for('listar_livros'))
    
    # lê o arquivo json
    with open('livros.json', 'r', encoding='utf-8') as f:
            livros = json.load(f)

    #exclui pelo índice
    if 0 <= id < len(livros):
        livros.pop(id)

    with open('livros.json', 'w', encoding='utf-8') as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)

    return redirect(url_for('listar_livros'))   

@app.route('/editar_livro/<int:id>', methods=['POST'])
def editar(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session.get('tipo') != 'admin':
        flash('Apenas administradores podem editar livros')
        return redirect(url_for('listar_livros'))

    with open('livros.json', 'r', encoding='utf-8') as f:
        livros = json.load(f)

    if 0 <= id < len(livros):
        livros[id]['titulo'] = request.form['titulo']
        livros[id]['autor'] = request.form['autor']
        livros[id]['ano'] = request.form['ano']
        livros[id]['genero'] = request.form['genero']

    with open('livros.json', 'w', encoding='utf-8') as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)

    return redirect(url_for('listar_livros')) 

@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        codigo = request.form.get('codigo_admin')
        
        if codigo == cod_admin:
            tipo = 'admin'
        else:
            tipo = 'comum'
            
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
            
        for u in usuarios:
            if u['usuario'] == user:
                flash('Usuário já existe')
                return redirect(url_for('cadastro'))
        
        usuarios.append({
            'usuario': user,
            'senha': senha,
            'tipo': tipo
        })
        
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)


        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)

        for u in usuarios:
            if u['usuario'] == user and u['senha'] == senha:
                session['usuario'] = user
                session['tipo'] = u['tipo']
                return redirect(url_for('listar_livros'))
        flash('usuário ou senha inválidos')
        return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    user = session['usuario']
    
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        usuarios = json.load(f)
        
    for u in usuarios:
        if u['usuario'] == user:
            senha = u['senha']
            tipo = u['tipo']
            break
    
    senhaf ="*" * len(senha)
    return render_template('perfil.html' , usuario=user , senha=senhaf, tipo=tipo)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
       app.run(debug=True)