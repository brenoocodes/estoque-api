from flask import jsonify, request
from src.login import *
from src.config import app, db, bcrypt
from src.models import Funcionarios


@app.route('/funcionario', methods=['GET'])
@token_obrigatorio
def exibir_funcionarios(funcionario):
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

@app.route('/funcionario/<int:matricula>', methods=['GET'])
@token_obrigatorio
def pegar_funcionario_por_matricula(funcionario, matricula):
    funcionario = Funcionarios.query.filter_by(matricula=matricula).first()
    if not funcionario:
        return jsonify({'mensagem': 'Funcionário não encontrado'})
    funcionario_escolhido ={}
    funcionario_escolhido['matricula'] = funcionario.matricula
    funcionario_escolhido['nome'] = funcionario.nome
    funcionario_escolhido['email'] = funcionario.email
    funcionario_escolhido['adminstrador'] = funcionario.administrador
    return jsonify(funcionario_escolhido)


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


@app.route('/funcionario/<int:matricula>', methods=['PUT'])
@token_obrigatorio
def alterar_funcionario(funcionario, matricula):
    try:
        funcionario_alterar = request.get_json()
        funcionario = Funcionarios.query.filter_by(matricula=matricula).first()
        if not funcionario:
            return jsonify({'mensagem': 'Funcionário não existente'})
        try:
           if 'nome' in funcionario_alterar:
               funcionario.nome = funcionario_alterar['nome']
        except KeyError:
            pass
        try:
           if 'email' in funcionario_alterar:
               funcionario.email = funcionario_alterar['email']
        except KeyError:
            pass
        try:
           if 'administrador' in funcionario_alterar:
               funcionario.administrador = funcionario_alterar['administrador']
        except KeyError:
            pass
        try:
           if 'senha' in funcionario_alterar:
               senha_criptografada = bcrypt.generate_password_hash(funcionario_alterar['senha']).decode('utf-8')
               funcionario.senha = senha_criptografada
        except KeyError:
            pass
        
        # Retorne uma resposta vazia se nenhum erro ocorrer
        db.session.commit()
        return jsonify({'mensagem': 'Atualização do funcionário bem-sucedida'})

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})

