from flask import jsonify, request
from src.login import *
from src.validadorcampo import *
from src.config import app, db, bcrypt
from src.models import Funcionarios

# Exibir todos os funcionários
@app.route('/funcionario', methods=['GET'])
@token_obrigatorio
def exibir_funcionarios(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para alterar esse processo'}), 403 

    funcionarios = Funcionarios.query.all()
    listadefuncionarios = []

    for funcionario_ in funcionarios:
        funcionario_atual = {
            'matricula': funcionario_.matricula,
            'nome': funcionario_.nome,
            'email': funcionario_.email,
            'administrador': funcionario_.administrador
        }
        listadefuncionarios.append(funcionario_atual)

    return jsonify(listadefuncionarios), 200

# Pegar funcionário por matrícula
@app.route('/funcionario/<int:matricula>', methods=['GET'])
@token_obrigatorio
def pegar_funcionario_por_matricula(funcionario, matricula):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para alterar esse processo'}), 403

    funcionario_ = Funcionarios.query.filter_by(matricula=matricula).first()

    if not funcionario_:
        return jsonify({'mensagem': 'Funcionário não encontrado'}), 400

    funcionario_escolhido = {
        'matricula': funcionario_.matricula,
        'nome': funcionario_.nome,
        'email': funcionario_.email,
        'adminstrador': funcionario_.administrador
    }

    return jsonify(funcionario_escolhido), 200

# Cadastrar novo funcionário
@app.route('/funcionario', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['nome', 'email', 'senha', 'administrador'], {'nome': str, 'email': str, 'senha': str, 'administrador': bool})
def cadastrar_funcionario(adm):
    if not adm.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para alterar esse processo'}), 403

    try:
        novo_funcionario = request.get_json()
        email = novo_funcionario['email']
        funcionario_existente = Funcionarios.query.filter_by(email=email).first()

        if funcionario_existente:
            return jsonify({'mensagem':'Funcionário já cadastrado'}), 400

        senha_criptografada = bcrypt.generate_password_hash(novo_funcionario['senha']).decode('utf-8')
        funcionario_ = Funcionarios(
            nome=novo_funcionario['nome'],
            email=novo_funcionario['email'],
            senha=senha_criptografada,
            administrador=novo_funcionario['administrador']
        )
        db.session.add(funcionario_)
        db.session.commit()

        return jsonify({'mensagem':'Novo funcionário cadastrado com sucesso'}), 200
        
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado'}), 500

# Alterar funcionário por matrícula
@app.route('/funcionario/<int:matricula>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['matricula', 'email', 'senha', 'telefone', 'administrador'], {'matricula': str, 'email': str, 'senha': str, 'telefone': str, 'administrador': bool})
def alterar_funcionario(funcionario, matricula):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para alterar esse processo'}), 403

    try:
        funcionario_alterar = request.get_json()
        funcionario_ = Funcionarios.query.filter_by(matricula=matricula).first()

        if not funcionario_:
            return jsonify({'mensagem': 'Funcionário não existente'}), 400

        if 'nome' in funcionario_alterar:
            funcionario_.nome = funcionario_alterar['nome']
        if 'email' in funcionario_alterar:
            funcionario_.email = funcionario_alterar['email']
        if 'administrador' in funcionario_alterar:
            funcionario_.administrador = funcionario_alterar['administrador']
        if 'senha' in funcionario_alterar:
            senha_criptografada = bcrypt.generate_password_hash(funcionario_alterar['senha']).decode('utf-8')
            funcionario_.senha = senha_criptografada

        db.session.commit()

        return jsonify({'mensagem': 'Atualização do funcionário bem-sucedida'}), 200

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500
