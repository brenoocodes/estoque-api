from flask import Flask, jsonify, request
from src.config import app, db, bcrypt
from src.models import Funcionarios


@app.route('/funcionario', methods=['GET'])
def exibir_funcionarios():
    funcionarios = Funcionarios.query.all()

    listadefuncionarios = []
    for funcionario in funcionarios:
        funcionario_atual = {}
        funcionario_atual['matricula'] = funcionario.matricula
        funcionario_atual['nome'] = funcionario.nome
        funcionario_atual['email'] = funcionario.email
        funcionario_atual['administrador'] = funcionario.administrador
        listadefuncionarios.append(funcionario_atual)
    return jsonify(listadefuncionarios)

@app.route('/funcionario', methods=['POST'])
def cadastrar_funcionario():
    try:
        novo_funcionario = request.get_json()
        email = novo_funcionario['email']
        funcionario_existente = Funcionarios.query.filter_by(email=email).first()
        if funcionario_existente:
            return jsonify({'mensagem':'Funcionário já cadastrado'}), 400
        senha_criptografada = bcrypt.generate_password_hash(novo_funcionario['senha']).decode('utf-8')
        funcionario = Funcionarios(nome=novo_funcionario['nome'], email=novo_funcionario['email'], senha=senha_criptografada, administrador=novo_funcionario['administrador'])
        db.session.add(funcionario)
        db.session.commit()
        return jsonify({'mensagem':'Novo funcionário cadastrado com sucesso'})
        
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado'}), 500

