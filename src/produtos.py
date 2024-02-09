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
    return jsonify(lista_de_produtos)

@app.route('/produtos/<int:id>', methods=['GET'])
def pegar_produto_por_id(id):
    produto = Produtos.query.filter_by(id=id).first()
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'})
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
    return jsonify(produto_atual)

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
            medida = novo_produto['medida'],
            preco=novo_produto['preco'],
            quantidade=novo_produto['quantidade']
        )
        db.session.add(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Novo Produto cadastrado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo deu errado'}), 500

@app.route('/produtos/<int:id>', methods=['PUT'])
def alterar_produtos(id):
    try:
        produto_alterado = request.get_json()
        produto = Produtos.query.filter_by(id=id).first()
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'})
        try:
            if 'nome' in produto_alterado:
                produto.nome = produto_alterado['nome']
        except KeyError:
            pass
        try:
            if 'nome_estoque' in produto_alterado:
                produto.nome_estoque = produto_alterado['nome_estoque']
        except KeyError:
            pass
        try:
            if 'nome' in produto_alterado:
                produto.nome = produto_alterado['nome']
        except KeyError:
            pass
        try:
            if 'medida' in produto_alterado:
                produto.medida = produto_alterado['medida']
        except KeyError:
            pass
        try:
            if 'preco' in produto_alterado:
                produto.preco = produto_alterado['preco']
        except KeyError:
            pass
        try:
            if 'quantidade' in produto_alterado:
                produto.quantidade = produto_alterado['quantidade']
        except KeyError:
            pass
        db.session.commit()
        return jsonify({'mensagem': f'{produto.nome_estoque} alterado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algo de errado não está certo'}), 500  
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produtos(id):
    produto = Produtos.query.filter_by(id=id).first()
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'})
    produto_excluido = {
        'id': produto.id,
        'nome': produto.nome,
        'nome_estoque': produto.nome_estoque
    }
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'Produto Excluído': produto_excluido})