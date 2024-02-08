from flask import Flask, jsonify, request
from config import app, db, bcrypt
from src.models import Autor

@app.route('/autores', methods=['GET'])

def obter_autores():
    autores = Autor.query.all()
    if autores:
        listadeautores = []
        for autor in autores:
            autor_atual = {}
            autor_atual['id_autor'] = autor.id_autor
            autor_atual['nome'] = autor.nome
            autor_atual['email'] = autor.email
            listadeautores.append(autor_atual)
        return jsonify(listadeautores)  # assim só retorna o jsons, bem mais fácil de tratar
    else:
        return jsonify({'mensagem': 'nenhum autor'})


@app.route('/autores/<int:id_autor>', methods=['GET'])

def obter_autor_por_id(id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Autor não encontrado')
    autor_escolhido = {}
    autor_escolhido['id_autor'] = autor.id_autor
    autor_escolhido['nome'] = autor.nome
    autor_escolhido['email'] = autor.email
    return jsonify(autor_escolhido)


@app.route('/autores', methods=['POST'])
def novo_autor():
    try:
        novo_autor = request.get_json()
        email = novo_autor['email']
        # Verificar se o e-mail já está cadastrado
        autor_existente = Autor.query.filter_by(email=email).first()
        if autor_existente:
            return jsonify({'mensagem': 'E-mail já cadastrado'}), 400
        senha_criptografada = bcrypt.generate_password_hash(novo_autor['senha']).decode('utf-8')
        autor = Autor(nome=novo_autor['nome'], email=email, senha=senha_criptografada, admin=True, email_verificado=False)
        db.session.add(autor)
        db.session.commit()
        return jsonify({'mensagem': 'Novo autor cadastrado com sucesso. Verifique seu e-mail para ativar a conta'})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado.'}), 500