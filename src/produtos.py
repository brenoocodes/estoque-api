from flask import Flask, jsonify, request
from src.config import app, db
from src.models import Produtos, Fornecedores, ProdutosFornecedores

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produtos.query.all()

    lista_de_produtos = []
    for produto in produtos:
        produto_atual = {
            'id': produto.id,
            'nome': produto.nome,
            'nome_estoque': produto.nome_estoque,
            'preco': produto.preco,
            'quantidade': produto.quantidade,
            'fornecedores': [fornecedor.razao_social for fornecedor in produto.fornecedores]
        }
        lista_de_produtos.append(produto_atual)
    return jsonify(lista_de_produtos)

@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    try:
        novo_produto = request.get_json()
        nome = novo_produto['nome']
        # Verifica se o produto já existe pelo nome
        produto_existente = Produtos.query.filter_by(nome=nome).first()
        if produto_existente:
            return jsonify({'mensagem': 'Produto já cadastrado'}), 400
        
        produto = Produtos(
            nome=novo_produto['nome'],
            nome_estoque=novo_produto['nome_estoque'],
            preco=novo_produto['preco'],
            quantidade=novo_produto['quantidade']
        )
        db.session.add(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Novo Produto cadastrado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado'}), 500

        