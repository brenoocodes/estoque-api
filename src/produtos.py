from flask import jsonify, request
from src.login import *
from src.validadorcampo import *
from src.config import app, db
from src.models import Produtos, Fornecedores, ProdutosFornecedores

# Listar todos os produtos
@app.route('/produtos', methods=['GET'])
@token_obrigatorio
def listar_produtos(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para acessar esta rota'}), 403
    
    try:
        produtos = Produtos.query.all()

        lista_de_produtos = []
        for produto in produtos:
            produto_atual = {
                'id': produto.id,
                'nome': produto.nome,
                'nome_estoque': produto.nome_estoque,
                'medida': produto.medida,
                'preco': produto.preco,
                'quantidade': produto.quantidade
            }
            
            fornecedores_produto = ProdutosFornecedores.query.filter_by(produto_id=produto_atual['id']).all()
            if fornecedores_produto:
                fornecedores_do_produto = []
                for fornecedor_produto in fornecedores_produto:
                    fornecedor = Fornecedores.query.get(fornecedor_produto.fornecedor_id)
                    if fornecedor:
                        fornecedores_do_produto.append({'id': fornecedor.id, 'nome_fantasia': fornecedor.nome_fantasia})
                produto_atual['fornecedores'] = fornecedores_do_produto
            else:
                produto_atual['fornecedores'] = 'Esse produto ainda não tem fornecedores cadastrados'
            
            lista_de_produtos.append(produto_atual)
        
        return jsonify(lista_de_produtos), 200
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500

# Pegar produto por ID
@app.route('/produtos/<int:id>', methods=['GET'])
@token_obrigatorio
def pegar_produto_por_id(funcionario, id):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para acessar esta rota'}), 403
    
    produto = Produtos.query.filter_by(id=id).first()
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404
    
    produto_atual = {
        'id': produto.id,
        'nome': produto.nome,
        'nome_estoque': produto.nome_estoque,
        'medida': produto.medida,
        'preco': produto.preco,
        'quantidade': produto.quantidade
    }
    
    fornecedores_produto = ProdutosFornecedores.query.filter_by(produto_id=produto_atual['id']).all()
    if fornecedores_produto:
        fornecedores_do_produto = []
        for fornecedor_produto in fornecedores_produto:
            fornecedor = Fornecedores.query.get(fornecedor_produto.fornecedor_id)
            if fornecedor:
                fornecedores_do_produto.append({'id': fornecedor.id, 'nome_fantasia': fornecedor.nome_fantasia})
        produto_atual['fornecedores'] = fornecedores_do_produto
    else:
        produto_atual['fornecedores'] = 'Esse produto ainda não tem fornecedores cadastrados'
    
    return jsonify(produto_atual), 200

# Cadastrar produto
@app.route('/produtos', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['nome', 'nome_estoque', 'medida', 'preco', 'quantidade'], {'nome': str, 'nome_estoque': str, 'medida': str, 'preco': float, 'quantidade': int})
def cadastrar_produto(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para acessar esta rota'}), 403
    
    try:
        novo_produto = request.get_json()
        nome = novo_produto['nome']
        
        # Verifica se o produto já existe pelo nome
        produto_existente = Produtos.query.filter_by(nome=nome).first()
        if produto_existente:
            return jsonify({'mensagem': 'Produto já cadastrado'}), 409
        
        produto = Produtos(
            nome=novo_produto['nome'],
            nome_estoque=novo_produto['nome_estoque'],
            medida = novo_produto['medida'],
            preco=novo_produto['preco'],
            quantidade=novo_produto['quantidade']
        )
        db.session.add(produto)
        db.session.commit()
        
        return jsonify({'mensagem': 'Novo produto cadastrado com sucesso'}), 201
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado ao cadastrar o produto'}), 500

# Alterar produto
@app.route('/produtos/<int:id>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['nome', 'nome_estoque', 'medida', 'preco', 'quantidade'], {'nome': str, 'nome_estoque': str, 'medida': str, 'preco': float, 'quantidade': int})
def alterar_produto(funcionario, id):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para acessar esta rota'}), 403
    
    try:
        produto_alterado = request.get_json()
        produto = Produtos.query.filter_by(id=id).first()
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
        
        if 'nome' in produto_alterado:
            produto.nome = produto_alterado['nome']
        if 'nome_estoque' in produto_alterado:
            produto.nome_estoque = produto_alterado['nome_estoque']
        if 'medida' in produto_alterado:
            produto.medida = produto_alterado['medida']
        if 'preco' in produto_alterado:
            produto.preco = produto_alterado['preco']
        if 'quantidade' in produto_alterado:
            produto.quantidade = produto_alterado['quantidade']
        
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto alterado com sucesso'}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo de errado não está certo'}), 500  


