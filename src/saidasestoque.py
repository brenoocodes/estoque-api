from flask import jsonify, request, make_response
from src.config import app, db
from src.login import *
from src.models import Produtos, Fornecedores, SaidasEstoque, Funcionarios

@app.route('/saidasestoque', methods=['POST'])
@token_obrigatorio
def saida_ao_estoque(funcionario):
    try:
        nova_saida_ao_estoque = request.get_json()
        produto_id = nova_saida_ao_estoque['produto_id']
        funcionario_requisitante_matricula = nova_saida_ao_estoque['funcionario_requisitante']
        produto_existente = Produtos.query.get(produto_id)
        if not produto_existente:
            return jsonify({'mensagem': 'Produto inexistente'}), 400
        funcionario_requisitante_existente = Funcionarios.query.get(funcionario_requisitante_matricula)
        if not funcionario_requisitante_existente:
            return jsonify({'mensagem': 'Funcionário inexistente'}), 400
        quantidade_em_estoque = produto_existente.quantidade
        quantidade_em_estoque = int(quantidade_em_estoque)
        if quantidade_em_estoque <= 0:
            return make_response('A quantidade em estoque desse produto é igual a zero')
        quantidade = int(nova_saida_ao_estoque['quantidade'])
        saida_estoque = SaidasEstoque(produto_id=produto_id, quantidade=quantidade, funcionario_responsavel=funcionario.matricula, funcionario_requisitante=funcionario_requisitante_matricula)
        db.session.add(saida_estoque)
        produto_existente.quantidade -= quantidade
        db.session.commit()
        response = {
            'matricula': funcionario.matricula,
            'funcionario_responsável': funcionario.nome,
            'produto': produto_existente.nome_estoque,
            'funcionario requisitante': funcionario_requisitante_existente.nome,
            'quantidade': quantidade
        }
        return jsonify({'Nova saída ao estoque': response})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})
    
@app.route('/saidasestoque/<int:id>', methods=['PUT'])
@token_obrigatorio
def atualizar_saida_ao_estoque(funcionario, id):
    try:
        saida_estoque = SaidasEstoque.query.get(id)
        if not saida_estoque:
            return jsonify({'mensagem': 'Não existe essa saída do estoque'})
        if saida_estoque.funcionario_responsavel != funcionario.matricula:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'})
        saida_ao_estoque_alterar = request.get_json()
        quantidade = saida_estoque.quantidade
        

    except Exception as e:
        print(e)
        return jsonify({'Mensagem': 'Algo deu errado'})