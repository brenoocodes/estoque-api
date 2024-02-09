from flask import jsonify, request
from src.config import app, db
from src.login import *
from src.models import Fornecedores, ProdutosFornecedores, Produtos

@app.route('/fornecedor', methods=['GET'])
@token_obrigatorio
def exibir_fornecedores(funcionario):
    try:
        fornecedores = Fornecedores.query.all()

        listadefornecedores = []
        for fornecedor in fornecedores:
            fornecedor_atual = {}
            fornecedor_atual['id'] = fornecedor.id
            fornecedor_atual['cnpj'] = fornecedor.cnpj
            fornecedor_atual['razao_social'] = fornecedor.razao_social
            fornecedor_atual['nome_fantasia'] = fornecedor.nome_fantasia
            fornecedor_atual['email'] = fornecedor.email
            fornecedor_atual['telefone'] = fornecedor.telefone

            produtos_fornecedor = ProdutosFornecedores.query.filter_by(fornecedor_id=fornecedor_atual['id']).all()
            if produtos_fornecedor:
                produtos_atual = []
                for pf in produtos_fornecedor:
                    produto = Produtos.query.get(pf.produto_id)
                    if produto:
                        produtos_atual.append({'id': produto.id, 'nome': produto.nome})
                fornecedor_atual['produtos'] = produtos_atual
            else:
                fornecedor_atual['produtos'] = 'Esse fornecedor ainda não tem produtos cadastrados'

            listadefornecedores.append(fornecedor_atual)
        
        return jsonify(listadefornecedores)
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500

@app.route('/fornecedor/<int:id>', methods=['GET'])
@token_obrigatorio
def pegar_fornecedor_por_id(funcionario, id):
    fornecedor = Fornecedores.query.filter_by(id=id).first()
    if not fornecedor:
        return jsonify({'mensagem': 'Fornecedor não encontrado'})
    fornecedor_atual = {}
    fornecedor_atual['id'] = fornecedor.id
    fornecedor_atual['cnpj'] = fornecedor.cnpj
    fornecedor_atual['razao_social'] = fornecedor.razao_social
    fornecedor_atual['nome_fantasia'] = fornecedor.nome_fantasia
    fornecedor_atual['email'] = fornecedor.email
    fornecedor_atual['telefone'] = fornecedor.telefone

    produtos_fornecedor = ProdutosFornecedores.query.filter_by(fornecedor_id=fornecedor_atual['id']).all()
    if produtos_fornecedor:
        produtos_atual = []
        for pf in produtos_fornecedor:
            produto = Produtos.query.get(pf.produto_id)
            if produto:
                produtos_atual.append({'id': produto.id, 'nome': produto.nome})
        fornecedor_atual['produtos'] = produtos_atual
    else:
        fornecedor_atual['produtos'] = 'Esse fornecedor ainda não tem produtos cadastrados'
    return jsonify(fornecedor_atual)


@app.route('/fornecedor', methods=['POST'])
@token_obrigatorio
def cadastrar_fornecedor(funcionario):
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


@app.route('/fornecedor/<int:id>', methods=['PUT'])
@token_obrigatorio
def alterar_fornecedor(funcionario, id):
    try:
        fornecedor_alterar = request.get_json()
        fornecedor = Fornecedores.query.filter_by(id=id).first()
        if not fornecedor:
            return jsonify({'mensagem': 'Fornecedor inexistente'})
        try:
            if 'cnpj' in fornecedor_alterar:
                fornecedor.cnpj = fornecedor_alterar['cnpj']
        except KeyError:
           pass
        try:
            if 'razao_social' in fornecedor_alterar:
                fornecedor.razao_social = fornecedor_alterar['razao_social']
        except KeyError:
           pass
        try:
            if 'nome_fantasia' in fornecedor_alterar:
                fornecedor.nome_fantasia = fornecedor_alterar['nome_fantasia']
        except KeyError:
           pass
        try:
            if 'email' in fornecedor_alterar:
                fornecedor.email = fornecedor_alterar['email']
        except KeyError:
           pass
        try:
            if 'telefone' in fornecedor_alterar:
                fornecedor.telefone = fornecedor_alterar['telefone']
        except KeyError:
           pass
        db.session.commit()
        return jsonify({'mensagem':f'Alteração feita com êxito para {fornecedor.nome_fantasia} '})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'erro interno'})
    
#delete fornecedor
@app.route('/fornecedor/<int:id>', methods=['DELETE'])
@token_obrigatorio
def deletar_fornecedor(funcionario, id):
    fornecedor = Fornecedores.query.filter_by(id=id).first()
    if not fornecedor:
        return jsonify({'mensagem': 'Não existe esse fornecedor'})
    fornecedor_excluido = {
        'id': fornecedor.id,
        'cnpj': fornecedor.cnpj,
        'razao_social': fornecedor.razao_social,
        'nome_fantasia': fornecedor.nome_fantasia
    }
    db.session.delete(fornecedor)
    db.session.commit()
    return jsonify({'Fornecedor Excluído': fornecedor_excluido})