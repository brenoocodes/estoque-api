from flask import jsonify, request
from src.config import app, db
from src.validadorcampo import *
from src.login import *
from src.models import Produtos, Fornecedores, ProdutosFornecedores

# Adicionar fornecedor ao produto
@app.route('/produtos/<int:id_produto>', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['id_fornecedor'], {'id_fornecedor': int})
def adicionar_fornecedor_ao_produto(funcionario, id_produto):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403
    
    try:
        # Verificar se o produto existe
        produto = Produtos.query.filter_by(id=id_produto).first()
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
        
        # Obter o id do fornecedor do corpo da solicitação
        novo_fornecedor = request.json
        id_fornecedor = novo_fornecedor['id_fornecedor']
        
        # Verificar se o fornecedor existe
        fornecedor_existente = Fornecedores.query.filter_by(id=id_fornecedor).first()
        if not fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor não existente'}), 404
        
        # Verificar se o fornecedor já está associado a esse produto
        if ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first():
            return jsonify({'mensagem': f'O produto {produto.nome} já está associado a fornecedor {fornecedor_existente.nome_fantasia}'}), 409
        
        # Criar uma nova relação entre produto e fornecedor
        produtofornecedor = ProdutosFornecedores(
            produto_id = produto.id,
            fornecedor_id = fornecedor_existente.id
        )
        db.session.add(produtofornecedor)
        db.session.commit()
        
        return jsonify({'mensagem': f'Novo fornecedor adicionado ao produto {produto.nome}'}), 201
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500

# Exclusão de relação entre produto e fornecedor
@app.route('/produtos/<int:id_produto>/<int:id_fornecedor>', methods=['DELETE'])
@token_obrigatorio
def deletar_fornecedor_do_produto(funcionario, id_produto, id_fornecedor):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403
    
    # Verificar se a relação entre produto e fornecedor existe
    relacao =  ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first()
    produto = Produtos.query.filter_by(id=id_produto).first()
    fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
    
    if relacao:
        # Excluir a relação se ela existir
        db.session.delete(relacao)
        db.session.commit()
        
        if produto and fornecedor:
            return jsonify({'mensagem': f'A relação entre {produto.nome} e {fornecedor.nome_fantasia} foi excluída com sucesso'}), 200
        else:
            return jsonify({'mensagem': f'A relação foi excluída com sucesso'}), 200
    else:
        if produto and fornecedor:
            return jsonify({'mensagem': f'Ainda não existia a relação entre {produto.nome} e {fornecedor.nome_fantasia}.'}), 404
        else:
            return jsonify({'mensagem': f'Ainda não existia a relação.'}), 404

# Adicionar produto ao fornecedor
@app.route('/fornecedor/<int:id_fornecedor>', methods=['POST'])
@verifica_campos_tipos(['id_produto'], {'id_produto': int})
@token_obrigatorio
def adicionar_produto_ao_fornecedor(funcionario, id_fornecedor):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403
    
    try:
        # Verificar se o fornecedor existe
        fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
        if not fornecedor:
            return jsonify({'mensagem': 'Fornecedor não encontrado'}), 404
        
        # Obter o id do produto do corpo da solicitação
        novo_produto = request.json
        id_produto = novo_produto['id_produto']
        
        # Verificar se o produto existe
        produto_existente = Produtos.query.filter_by(id=id_produto).first()
        if not produto_existente:
            return jsonify({'mensagem': 'Produto não existente'}), 404
        
        # Verificar se o fornecedor já está associado a esse produto
        if ProdutosFornecedores.query.filter_by(fornecedor_id=id_fornecedor, produto_id=id_produto).first():
            return jsonify({'mensagem': f'O fornecedor {fornecedor.nome_fantasia} já está associado ao produto {produto_existente.nome}'}), 409
        
        # Criar uma nova relação entre fornecedor e produto
        fornecedorproduto = ProdutosFornecedores(
            fornecedor_id=fornecedor.id,
            produto_id=produto_existente.id
        )
        db.session.add(fornecedorproduto)
        db.session.commit()
        
        return jsonify({'mensagem': f'Novo produto adicionado ao fornecedor {fornecedor.nome_fantasia}'}), 201
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500

# Exclusão de relação entre produto e fornecedor
@app.route('/fornecedor/<int:id_fornecedor>/<int:id_produto>', methods=['DELETE'])
@token_obrigatorio
def deletar_produto_do_fornecedor(funcionario, id_fornecedor, id_produto):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403
    
    # Verificar se a relação entre produto e fornecedor existe
    relacao =  ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first()
    produto = Produtos.query.filter_by(id=id_produto).first()
    fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
    
    if relacao:
        # Excluir a relação se ela existir
        db.session.delete(relacao)
        db.session.commit()
        
        return jsonify ({'mensagem': f'A relação entre {fornecedor.nome_fantasia} e {produto.nome} foi excluído com sucesso'}), 200
    
    return jsonify({'mensagem': f'Ainda não existia a relação entre {fornecedor.nome_fantasia} e {produto.nome}.'}), 404
