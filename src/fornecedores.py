from flask import Flask, jsonify, request
from src.config import app, db
from src.models import Fornecedores

@app.route('/fornecedor', methods=['GET'])
def exibir_fornecedors():
    fornecedores = Fornecedores.query.all()

    listadefornecedores = []
    for fornecedor in fornecedores:
        fornecedor_atual = {}
        fornecedor_atual['cnpj'] = fornecedor.cnpj
        fornecedor_atual['razao_social'] = fornecedor.razao_social
        fornecedor_atual['nome_fantasia'] = fornecedor.nome_fantasia
        fornecedor_atual['email'] = fornecedor.email
        fornecedor_atual['telefone'] = fornecedor.telefone
        listadefornecedores.append(fornecedor_atual)
    return jsonify(listadefornecedores)


@app.route('/fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    try:
        novo_fornecedor = request.get_json()
        cnpj = novo_fornecedor['cnpj']
        fornecedor_existente = Fornecedores.query.filter_by(cnpj=cnpj).first()
        if fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor já cadastrado'}), 400
        fornecedor = Fornecedores(cnpj=novo_fornecedor['cnpj'], razao_social=novo_fornecedor['razao_social'], nome_fantasia=novo_fornecedor['nome_fantasia'], email=novo_fornecedor['email'], telefone=novo_fornecedor['telefone'])
        db.session.add(fornecedor)
        db.session.commit()
        return jsonify({'mensagem': 'Novo Fornecedor cadastrado com sucesso'})

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'algo deu errado'}), 500