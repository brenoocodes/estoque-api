from flask import jsonify, request, make_response
from src.config import app, db
from src.validadorcampo import *
from src.models import Produtos, SaidasEstoque, Funcionarios
from src.login import token_obrigatorio

@app.route('/saidasestoque/todos', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_saidas(funcionario):
    if not funcionario.administrador:
        return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403
    try:
        saida_ao_estoque = SaidasEstoque.query.all()  
        listadesaidas = []
        for saida in saida_ao_estoque:
            produto = Produtos.query.get(saida.produto_id)
            funcionario_requisitante = Funcionarios.query.get(saida.funcionario_requisitante)
            funcionario_responsavel = Funcionarios.query.get(saida.funcionario_responsavel) 
            
            saida_atual = {
                'id': saida.id,
                'produto_id': saida.produto_id,
                'produto': produto.nome_estoque,
                'quantidade': saida.quantidade,
                'funcionario_responsavel_matricula': funcionario_responsavel.matricula,
                'funcionario_responsavel_nome': funcionario_responsavel.nome,
                'funcionario_requisitante_matricula': funcionario_requisitante.matricula,
                'funcionario_requisitante_nome': funcionario_requisitante.nome
            }
            listadesaidas.append(saida_atual)
        if len(listadesaidas)  == 0:
            return jsonify({'mensagem': 'Nenhuma saída cadastrada'}),200
        return jsonify(listadesaidas), 200  # OK
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500  # Internal Server Error

@app.route('/saidasestoque', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_saidas_logado(funcionario):
    try:
        saida_ao_estoque = SaidasEstoque.query.filter_by(funcionario_responsavel=funcionario.matricula).all()
        if not saida_ao_estoque:
            return jsonify({'mensagem': f'O {funcionario.nome} ainda não cadastrou nenhuma saída ao estoque'}), 200  # Not Found
        
        listadesaidas = []
        for saida in saida_ao_estoque:
            produto = Produtos.query.get(saida.produto_id)
            funcionario_requisitante = Funcionarios.query.get(saida.funcionario_requisitante)
            funcionario_responsavel = Funcionarios.query.get(saida.funcionario_responsavel) 
            
            saida_atual = {
                'id': saida.id,
                'produto_id': saida.produto_id,
                'produto': produto.nome_estoque,
                'quantidade': saida.quantidade,
                'funcionario_responsavel_matricula': funcionario_responsavel.matricula,
                'funcionario_responsavel_nome': funcionario_responsavel.nome,
                'funcionario_requisitante_matricula': funcionario_requisitante.matricula,
                'funcionario_requisitante_nome': funcionario_requisitante.nome
            }
            listadesaidas.append(saida_atual)
        
        return jsonify(listadesaidas), 200  # OK
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500  # Internal Server Error

@app.route('/saidasestoque', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['produto_id', 'quantidade', 'funcionario_requisitante'], {'produto_id': int, 'quantidade': int, 'funcionario_requisitante': int})
def saida_ao_estoque(funcionario):
    try:
        nova_saida_ao_estoque = request.get_json()
        produto_id = nova_saida_ao_estoque['produto_id']
        funcionario_requisitante_matricula = nova_saida_ao_estoque['funcionario_requisitante']
        
        produto_existente = Produtos.query.get(produto_id)
        if not produto_existente:
            return jsonify({'mensagem': 'Produto inexistente'}), 400  # Bad Request
        
        funcionario_requisitante_existente = Funcionarios.query.get(funcionario_requisitante_matricula)
        if not funcionario_requisitante_existente:
            return jsonify({'mensagem': 'Funcionário inexistente'}), 400  # Bad Request
        quantidade = nova_saida_ao_estoque['quantidade']

        quantidade_em_estoque = produto_existente.quantidade
        if quantidade_em_estoque - quantidade < 0:
            return make_response(f'A quantidade em estoque desse produto, após você modificar, seria igual a {quantidade_em_estoque-quantidade}. Por favor verifique os valores, o estoque não pode ficar negativo'), 400  # Bad Request
        saida_estoque = SaidasEstoque(
            produto_id=produto_id,
            quantidade=quantidade,
            funcionario_responsavel=funcionario.matricula,
            funcionario_requisitante=funcionario_requisitante_matricula
        )
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
        
        return jsonify({'Nova saída ao estoque': response}), 201  # Created
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro ocorreu'}), 500  # Internal Server Error

@app.route('/saidasestoque/<int:id>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['produto_id', 'quantidade', 'funcionario_requisitante'], {'produto_id': int, 'quantidade': int, 'funcionario_requisitante': int})
def atualizar_saida_ao_estoque(funcionario, id):
    try:
        nova_saida_ao_estoque_alterar = request.get_json()
        saida_ao_estoque = SaidasEstoque.query.get(id)
        if not funcionario.administrador:
            if saida_ao_estoque.funcionario_responsavel != funcionario.matricula:
                return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403 
        produto = Produtos.query.filter_by(id=saida_ao_estoque.produto_id).first()
        quantidade = saida_ao_estoque.quantidade
        responsavel = Funcionarios.query.filter_by(matricula=funcionario.matricula).first()
        funcionario_requisitante = Funcionarios.query.filter_by(matricula=saida_ao_estoque.funcionario_requisitante).first()
        
        try:
            if 'produto_id' in nova_saida_ao_estoque_alterar and 'quantidade' in nova_saida_ao_estoque_alterar:
                print('passei no produto_id e na quantidade')
                nova_quantidade = nova_saida_ao_estoque_alterar['quantidade']
                produto_antigo = Produtos.query.filter_by(id=saida_ao_estoque.produto_id).first()
                produto_novo = Produtos.query.filter_by(id=nova_saida_ao_estoque_alterar['produto_id']).first()
                if not produto_novo:
                    return jsonify({'mensagem': 'Não existe produto com esse id'})
                produto_antigo.quantidade += quantidade
                saida_ao_estoque.produto_id = produto_novo.id
                saida_ao_estoque.quantidade = nova_quantidade
                produto_novo.quantidade  -= nova_quantidade
                quantidade = nova_quantidade
                produto = produto_novo
            if 'quantidade' in nova_saida_ao_estoque_alterar:
                print('passei só quantidade')
                produto_antigo = Produtos.query.filter_by(id=saida_ao_estoque.produto_id).first()
                produto_antigo.quantidade += quantidade
                nova_quantidade = nova_saida_ao_estoque_alterar['quantidade']
                produto_antigo.quantidade -= nova_quantidade
                saida_ao_estoque.quantidade = nova_quantidade
                quantidade = nova_quantidade
                produto = produto_antigo
            elif 'produto_id' in nova_saida_ao_estoque_alterar:
                print('passei só produto_id')
                produto_antigo = Produtos.query.filter_by(id=saida_ao_estoque.produto_id).first()
                produto_novo = Produtos.query.filter_by(id=nova_saida_ao_estoque_alterar['produto_id']).first()
                if not produto_novo:
                    return jsonify({'mensagem': 'Não existe produto com esse id'})
                produto_antigo.quantidade += quantidade
                saida_ao_estoque.produto_id = produto_novo.id
                produto_novo.quantidade  -= quantidade
                produto = produto_novo
        except KeyError:
            pass
        try:
            if 'funcionario_requisitante' in nova_saida_ao_estoque_alterar:
                novo_funcionario_requisitante = Funcionarios.query.filter_by(matricula=nova_saida_ao_estoque_alterar['funcionario_requisitante']).first()
                if not novo_funcionario_requisitante:
                    return jsonify({'mensagem': 'Esse funcionário requisitante não existe'}), 400
                saida_ao_estoque.funcionario_requisitante = novo_funcionario_requisitante.matricula
                funcionario_requisitante = novo_funcionario_requisitante
        except KeyError:
            pass
        if produto.quantidade < 0:
            return make_response(f'A quantidade em estoque desse produto, após você modificar, seria igual a {produto.quantidade}. Por favor verifique os valores, o estoque não pode ficar negativo'), 400

        db.session.commit()
        response = {
            'produto_id' : produto.id,
            'funcionario_responsavel': funcionario.nome,
            'produto_nome': produto.nome_estoque,
            'quantidade': quantidade,
            'funcionario_requisitante': funcionario_requisitante.matricula,
            'funcionario_requisitante_nome': funcionario_requisitante.nome
        }
        return jsonify({'Saida alterada com sucesso': response}), 200

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'algum erro'}), 500


@app.route('/saidasestoque/<int:id>', methods=['DELETE'])
@token_obrigatorio
def excluir_saida_ao_estoque(funcionario, id):
    try:
        saida_estoque = SaidasEstoque.query.get(id)
        if not saida_estoque:
            return jsonify({'mensagem': 'Saída não encontrada'}), 404  # Not Found
        
        if not funcionario.administrador:
            if saida_ao_estoque.funcionario_responsavel != funcionario.matricula:
                return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403 
        
        quantidade = saida_estoque.quantidade
        produto = Produtos.query.get(saida_estoque.produto_id)
        produto.quantidade += quantidade
        
        db.session.delete(saida_estoque)
        db.session.commit()
        
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': quantidade
        }
        
        return jsonify({'Saída excluída com sucesso': response}), 200  # OK
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': f'Algum erro ocorreu: {e}'}), 500  # Internal Server Error
