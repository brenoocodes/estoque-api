from flask import jsonify, request
from src.config import app, db
from src.validadorcampo import *
from src.login import *
from src.models import Fornecedores, ProdutosFornecedores, Produtos

# Exibir todos os fornecedores
@app.route('/fornecedor', methods=['GET'])
@token_obrigatorio
def exibir_fornecedores(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para essa rota'}), 403
    
    try:
        fornecedores = Fornecedores.query.all()
        listadefornecedores = []
        
        for fornecedor in fornecedores:
            fornecedor_atual = {
                'id': fornecedor.id,
                'cnpj': fornecedor.cnpj,
                'razao_social': fornecedor.razao_social,
                'nome_fantasia': fornecedor.nome_fantasia,
                'email': fornecedor.email,
                'telefone': fornecedor.telefone
            }
            
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
        
        return jsonify(listadefornecedores), 200
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500

# Pegar fornecedor por ID
@app.route('/fornecedor/<int:id>', methods=['GET'])
@token_obrigatorio
def pegar_fornecedor_por_id(funcionario, id):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para acessar este recurso'}), 403
    
    fornecedor = Fornecedores.query.filter_by(id=id).first()
    if not fornecedor:
        return jsonify({'mensagem': 'Fornecedor não encontrado'}), 404
    
    fornecedor_atual = {
        'id': fornecedor.id,
        'cnpj': fornecedor.cnpj,
        'razao_social': fornecedor.razao_social,
        'nome_fantasia': fornecedor.nome_fantasia,
        'email': fornecedor.email,
        'telefone': fornecedor.telefone
    }
    
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
    
    return jsonify(fornecedor_atual), 200

# Cadastrar fornecedor
@app.route('/fornecedor', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['cnpj', 'razao_social', 'nome_fantasia', 'email', 'telefone'], {'cnpj': str, 'razao_social': str, 'nome_fantasia': str, 'email': str, 'telefone': str})
def cadastrar_fornecedor(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para cadastrar um novo fornecedor'}), 403
    
    try:
        novo_fornecedor = request.get_json()
        cnpj = novo_fornecedor['cnpj']
        fornecedor_existente = Fornecedores.query.filter_by(cnpj=cnpj).first()
        
        if fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor já cadastrado'}), 409
        
        fornecedor = Fornecedores(cnpj=novo_fornecedor['cnpj'], razao_social=novo_fornecedor['razao_social'], nome_fantasia=novo_fornecedor['nome_fantasia'], email=novo_fornecedor['email'], telefone=novo_fornecedor['telefone'])
        db.session.add(fornecedor)
        db.session.commit()
        
        return jsonify({'mensagem': 'Novo fornecedor cadastrado com sucesso'}), 201
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado ao cadastrar o fornecedor'}), 500

# Alterar fornecedor
@app.route('/fornecedor/<int:id>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['cnpj', 'razao_social', 'nome_fantasia', 'email', 'telefone'], {'cnpj': str, 'razao_social': str, 'nome_fantasia': str, 'email': str, 'telefone': str})
def alterar_fornecedor(funcionario, id):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para alterar os dados deste fornecedor'}), 403
    
    try:
        fornecedor_alterar = request.get_json()
        fornecedor = Fornecedores.query.filter_by(id=id).first()
        
        if not fornecedor:
            return jsonify({'mensagem': 'Fornecedor inexistente'}), 404
        
        if 'cnpj' in fornecedor_alterar:
            fornecedor.cnpj = fornecedor_alterar['cnpj']
        if 'razao_social' in fornecedor_alterar:
            fornecedor.razao_social = fornecedor_alterar['razao_social']
        if 'nome_fantasia' in fornecedor_alterar:
            fornecedor.nome_fantasia = fornecedor_alterar['nome_fantasia']
        if 'email' in fornecedor_alterar:
            fornecedor.email = fornecedor_alterar['email']
        if 'telefone' in fornecedor_alterar:
            fornecedor.telefone = fornecedor_alterar['telefone']
        
        db.session.commit()
        
        return jsonify({'mensagem': f'Os dados do fornecedor {fornecedor.nome_fantasia} foram atualizados com sucesso'}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado ao alterar o fornecedor'}), 500

# Deletar fornecedor
@app.route('/fornecedor/<int:id>', methods=['DELETE'])
@token_obrigatorio
def deletar_fornecedor(funcionario, id):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para excluir este fornecedor'}), 403
    
    fornecedor = Fornecedores.query.filter_by(id=id).first()
    if not fornecedor:
        return jsonify({'mensagem': 'Não existe esse fornecedor'}), 404
    
    fornecedor_excluido = {
        'id': fornecedor.id,
        'cnpj': fornecedor.cnpj,
        'razao_social': fornecedor.razao_social,
        'nome_fantasia': fornecedor.nome_fantasia
    }
    
    db.session.delete(fornecedor)
    db.session.commit()
    
    return jsonify({'Fornecedor excluído': fornecedor_excluido}), 200
