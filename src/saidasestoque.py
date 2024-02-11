from flask import jsonify, request, make_response
from src.config import app, db
from src.login import *
from src.models import Produtos, SaidasEstoque, Funcionarios

@app.route('/saidasestoque/todos', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_saidas(funcionario):
    try:
        saida_ao_estoque = SaidasEstoque.query.all()
        listadesaidas = []
        for saida in saida_ao_estoque:
            produto = Produtos.query.filter_by(id=saida.produto_id).first()
            funcionario_requisitante = Funcionarios.query.filter_by(matricula=saida.funcionario_requisitante).first()
            funcionario_responsavel = Funcionarios.query.filter_by(matricula=saida.funcionario_responsavel).first() 
            saida_atual = {}
            saida_atual['id'] = saida.id
            saida_atual['produto_id'] = saida.produto_id
            saida_atual['produto'] = produto.nome_estoque
            saida_atual['quantidade'] = saida.quantidade
            saida_atual['funcionario_responsavel_matricula'] = funcionario_responsavel.matricula
            saida_atual['funcionario_responsavel_nome'] = funcionario_responsavel.nome
            saida_atual['funcionario_requisitante_matricula'] = funcionario_requisitante.matricula
            saida_atual['funcionario_requisitante_nome'] = funcionario_requisitante.nome
            listadesaidas.append(saida_atual)
        if len(listadesaidas) == 0:
            return jsonify({'mensagem': 'ainda não foram registradas saídas'})
        return jsonify(listadesaidas)
    except Exception as e:
        print(e)
        return jsonify({'mensagem':'Algum erro'})
    
@app.route('/saidasestoque', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_saidas_logado(funcionario):
    try:
        saida_ao_estoque = SaidasEstoque.query.filter_by(funcionario_responsavel= funcionario.matricula)
        listadesaidas = []
        for saida in saida_ao_estoque:
            produto = Produtos.query.filter_by(id=saida.produto_id).first()
            funcionario_requisitante = Funcionarios.query.filter_by(matricula=saida.funcionario_requisitante).first()
            funcionario_responsavel = Funcionarios.query.filter_by(matricula=saida.funcionario_responsavel).first() 
            saida_atual = {}
            saida_atual['id'] = saida.id
            saida_atual['produto_id'] = saida.produto_id
            saida_atual['produto'] = produto.nome_estoque
            saida_atual['quantidade'] = saida.quantidade
            saida_atual['funcionario_responsavel_matricula'] = funcionario_responsavel.matricula
            saida_atual['funcionario_responsavel_nome'] = funcionario_responsavel.nome
            saida_atual['funcionario_requisitante_matricula'] = funcionario_requisitante.matricula
            saida_atual['funcionario_requisitante_nome'] = funcionario_requisitante.nome
            listadesaidas.append(saida_atual)
        if len(listadesaidas) == 0:
            return jsonify({'mensagem': f'O {funcionario.nome} ainda não cadastrou nenhuma saída ao estoque'})
        return jsonify(listadesaidas)

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})

@app.route('/saidasestoque', methods=['POST'])
@token_obrigatorio
def saida_ao_estoque(funcionario):
    try:
        nova_saida_ao_estoque = request.get_json()

        campos_obrigatorios = ['produto_id', 'funcionario_requisitante', 'quantidade']
        for campo in campos_obrigatorios:
            if campo not in nova_saida_ao_estoque:
                return jsonify({'mensagem': f'O campo obrigatório "{campo}" não foi preenchido'}), 400
        
        # Verifica se os tipos de dados são os esperados
        if not isinstance(nova_saida_ao_estoque['produto_id'], int):
            return jsonify({'mensagem': 'O campo "produto_id" deve ser um inteiro'}), 400
        if not isinstance(nova_saida_ao_estoque['funcionario_requisitante'], int):
            return jsonify({'mensagem': 'O campo "funcionario_requisitante" deve ser um inteiro'}), 400
        if not isinstance(nova_saida_ao_estoque['quantidade'], int):
            return jsonify({'mensagem': 'O campo "quantidade" deve ser um inteiro'}), 400
        
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
        funcionario_requisitante_existente = Funcionarios.query.filter_by(matricula=saida_estoque.funcionario_requisitante).first()
        if not saida_estoque:
            return jsonify({'mensagem': 'Não existe essa saída do estoque'})
        if saida_estoque.funcionario_responsavel != funcionario.matricula:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'})
        saida_ao_estoque_alterar = request.get_json()
        quantidade = saida_estoque.quantidade
        try:
            if 'produto_id' in saida_ao_estoque_alterar:
                if not isinstance(saida_ao_estoque_alterar['produto_id'], int):
                    return jsonify({'mensagem': 'O campo "produto_id" deve ser um inteiro'}), 400
                produto_id = saida_ao_estoque_alterar['produto_id']
                produto_existente = Produtos.query.filter_by(id=produto_id).first()
                if not produto_existente:
                    return jsonify({'mensagem': 'Produto inexistente'}), 400
                if produto_id != saida_estoque.produto_id:
                    produto_aumentar = Produtos.query.filter_by(id= saida_estoque.produto_id).first()
                    produto_aumentar.quantidade += quantidade
                    saida_estoque.produto_id = produto_id
                    if 'quantidade' in saida_ao_estoque_alterar:
                        if not isinstance(saida_ao_estoque_alterar['quantidade'], int):
                            return jsonify({'mensagem': 'O campo "quantidade" deve ser um inteiro'}), 400
                        nova_quantidade = saida_ao_estoque_alterar['quantidade']
                        produto_existente.quantidade -= nova_quantidade
                        quantidade = nova_quantidade
                    else:
                        produto_existente.quantidade -= quantidade
                        produto = produto_existente
        except KeyError:
            pass

        try:
            if 'quantidade' in saida_ao_estoque_alterar:
                if not isinstance(saida_ao_estoque_alterar['quantidade'], int):
                        return jsonify({'mensagem': 'O campo "quantidade" deve ser um inteiro'}), 400
                nova_quantidade = saida_ao_estoque_alterar['quantidade']
                produto = Produtos.query.get(saida_estoque.produto_id)
                produto.quantidade += quantidade
                produto.quantidade -= nova_quantidade
                produto_existente = produto
                saida_estoque.quantidade = nova_quantidade
                quantidade = nova_quantidade
        except KeyError:
            pass
        try:
            if 'funcionario_requisitante' in saida_ao_estoque_alterar:
                if not isinstance(saida_ao_estoque_alterar['funcionario_requisitante'], int):
                    return jsonify({'mensagem': 'O campo "funcionario_requisitante" deve ser um inteiro'}), 400
                funcionario_requisitante_matricula = saida_ao_estoque_alterar['funcionario_requisitante']
                funcionario_requisitante_existente = Funcionarios.query.get(funcionario_requisitante_matricula)
                if not funcionario_requisitante_existente:
                    return jsonify({'mensagem': 'Funcionário inexistente'}), 400
                saida_estoque.funcionario_requisitante = funcionario_requisitante_existente.matricula
        except KeyError:
            pass
        db.session.commit()
        response = {
            'id': saida_estoque.id,
            'matricula': funcionario.matricula,
            'funcionario_responsável': funcionario.nome,
            'produto': produto_existente.nome_estoque,
            'funcionario requisitante': funcionario_requisitante_existente.nome,
            'quantidade': quantidade
        }
        return jsonify({'Saída alterada com sucesso': response})

    except Exception as e:
        print(e)
        return jsonify({'Mensagem': 'Algo deu errado'})

#delete
@app.route('/saidasestoque/<int:id>', methods=['DELETE'])
@token_obrigatorio
def excluir_saida_ao_estoque(funcionario, id):
    try:
        saida_estoque = SaidasEstoque.query.get(id)
        if not saida_estoque:
            return jsonify({'mensagem': 'Saída não encontrada'})
        if saida_estoque.funcionario_responsavel != funcionario.matricula:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar esta saída de estoque'}), 403
        try:
            quantidade = saida_estoque.quantidade
            produto = Produtos.query.get(saida_estoque.produto_id)
            produto.quantidade += quantidade
        except Exception as e:
            print(e)
            return jsonify({'mensagem': 'Erro ao atualizar a quantidade'})
        db.session.delete(saida_estoque)
        db.session.commit()
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': quantidade
        }
        return jsonify({'Saída excluída com sucesso': response})
    except Exception as e:
        print(e)
        return jsonify({'mensagem': f'Algum erro{e}'})