from flask import Flask, jsonify, request
from src.config import app, db
from src.models import Produtos, Fornecedores, ProdutosFornecedores

#adicionar fornecedor ao produto
@app.route('/produtos/<int:id_produto>', methods=['POST'])
def adicionar_fornecedor_ao_produto(id_produto):
    try:
        produto = Produtos.query.filter_by(id=id_produto).first()
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'})
        
        novo_fornecedor = request.json
        id_fornecedor = novo_fornecedor['id_fornecedor']
        
        fornecedor_existente = Fornecedores.query.filter_by(id=id_fornecedor).first()
        
        if not fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor não existente'})
        
        # Verificar se o fornecedor já está associado a esse produto
        if ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first():
            return jsonify({'mensagem': f'O produto {produto.nome} já está associado a fornecedor {fornecedor_existente.nome_fantasia}'})
        
        produtofornecedor = ProdutosFornecedores(
            produto_id = produto.id,
            fornecedor_id = fornecedor_existente.id
        )
        db.session.add(produtofornecedor)
        db.session.commit()
        return jsonify({'mensagem': f'Novo fornecedor adicionado ao produto {produto.nome}'})
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})
#exclusão
@app.route('/produtos/<int:id_produto>/<int:id_fornecedor>', methods=['DELETE'])
def deletar_fornecedor_do_produto(id_produto, id_fornecedor):
    relacao =  ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first()
    produto = Produtos.query.filter_by(id=id_produto).first()
    fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
    if relacao:
        db.session.delete(relacao)
        db.session.commit()
        return jsonify ({'mensagem': f'A relação entre {produto.nome} e {fornecedor.nome_fantasia} foi excluído com sucesso'})
    return jsonify({'mensagem': f'Ainda não existia a relação entre {produto.nome} e {fornecedor.nome_fantasia}.'})


#adicionar produto ao fornecedor

@app.route('/fornecedor/<int:id_fornecedor>', methods=['POST'])
def adicionar_produto_ao_fornecedor(id_fornecedor):
    try:
        fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
        if not fornecedor:
            return jsonify({'mensagem': 'Fornecedor não encontrado'})
        
        novo_produto = request.json
        id_produto = novo_produto['id_produto']
        
        produto_existente = Produtos.query.filter_by(id=id_produto).first()
        if not produto_existente:
            return jsonify({'mensagem': 'Produto não existente'})
        
        # Verificar se o fornecedor já está associado a esse produto
        if ProdutosFornecedores.query.filter_by(fornecedor_id=id_fornecedor, produto_id=id_produto).first():
            return jsonify({'mensagem': f'O fornecedor {fornecedor.nome_fantasia} já está associado ao produto {produto_existente.nome}'})
        
        fornecedorproduto = ProdutosFornecedores(
            fornecedor_id=fornecedor.id,
            produto_id=produto_existente.id
        )
        db.session.add(fornecedorproduto)
        db.session.commit()
        
        return jsonify({'mensagem': f'Novo produto adicionado ao fornecedor {fornecedor.nome_fantasia}'})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500
#exclusão
@app.route('/fornecedor/<int:id_fornecedor>/<int:id_produto>', methods=['DELETE'])
def deletar_produto_do_fornecedor(id_fornecedor, id_produto):
    relacao =  ProdutosFornecedores.query.filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor).first()
    produto = Produtos.query.filter_by(id=id_produto).first()
    fornecedor = Fornecedores.query.filter_by(id=id_fornecedor).first()
    if relacao:
        db.session.delete(relacao)
        db.session.commit()
        return jsonify ({'mensagem': f'A relação entre {fornecedor.nome_fantasia} e {produto.nome} foi excluído com sucesso'})
    return jsonify({'mensagem': f'Ainda não existia a relação entre {fornecedor.nome_fantasia} e {produto.nome}.'})