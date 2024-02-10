from flask import jsonify, request
from src.config import app, db
from src.login import *
from src.models import Produtos, Fornecedores, EntradasEstoque

@app.route('/entradasestoque', methods=['POST'])
@token_obrigatorio
def entrada_ao_estoque(funcionario):
    try:
        nova_entrada_ao_estoque = request.get_json()
        produto_id = nova_entrada_ao_estoque['produto_id']
        fornecedor_id = nova_entrada_ao_estoque['fornecedor_id']
        
        # Verifica se o produto existe
        produto_existente = Produtos.query.get(produto_id)
        if not produto_existente:
            return jsonify({'mensagem': 'Produto inexistente'}), 400
        
        # Verifica se o fornecedor existe
        fornecedor_existente = Fornecedores.query.get(fornecedor_id)
        if not fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor inexistente'}), 400
        
        quantidade = int(nova_entrada_ao_estoque['quantidade'])
        
        # Cria a entrada no estoque
        entrada_estoque = EntradasEstoque(
            produto_id=produto_id,
            fornecedor_id=fornecedor_id,
            quantidade=quantidade,
            nota=nova_entrada_ao_estoque['nota'],
            funcionario_matricula=funcionario.matricula
        )
        
        db.session.add(entrada_estoque)
        
        # Atualiza a quantidade do produto no estoque
        produto_existente.quantidade += quantidade
        
        db.session.commit()
        
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto_existente.nome_estoque,
            'quantidade': quantidade
        }
        
        return jsonify({'Nova entrada ao estoque': response})
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})
    

@app.route('/entradasestoque/<int:id>', methods=['PUT'])
@token_obrigatorio
def atualizar_entrada_ao_estoque(funcionario, id):
    try:
        entrada_estoque = EntradasEstoque.query.get(id)
        
        if not entrada_estoque:
            return jsonify({'mensagem': 'Entrada de estoque não encontrada'}), 404
        
        # Verifica se o funcionário que está tentando atualizar é o mesmo que criou a entrada de estoque
        if entrada_estoque.funcionario_matricula != funcionario.matricula:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar esta entrada de estoque'}), 403
        
        nova_quantidade = request.json.get('quantidade')
        
        if nova_quantidade is not None:
            # Atualiza a quantidade do produto no estoque
            produto = Produtos.query.get(entrada_estoque.produto_id)
            produto.quantidade -= entrada_estoque.quantidade  # Remove a quantidade anterior
            produto.quantidade += nova_quantidade  # Adiciona a nova quantidade
            entrada_estoque.quantidade = nova_quantidade
        
        db.session.commit()
        
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': nova_quantidade
        }
        
        return jsonify({'Entrada de estoque atualizada': response})
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500
