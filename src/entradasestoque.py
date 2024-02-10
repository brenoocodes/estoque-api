from flask import jsonify, request
from src.config import app, db
from src.login import *
from src.models import Produtos, Fornecedores, EntradasEstoque, Funcionarios

@app.route('/entradasestoque/todos', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_entradas(funcionario):
    try:
        entradas_ao_estoque = EntradasEstoque.query.all()
        listadeentradas = []
        for entrada in entradas_ao_estoque:
            produto = Produtos.query.filter_by(id=entrada.produto_id).first()
            fornecedor = Fornecedores.query.filter_by(id=entrada.fornecedor_id).first()
            funcionario_responsavel = Funcionarios.query.filter_by(matricula=entrada.funcionario_matricula).first()
            entrada_atual = {}
            entrada_atual['id'] = entrada.id
            entrada_atual['nota'] = entrada.nota
            entrada_atual['produto_id'] = entrada.produto_id
            entrada_atual['produto'] = produto.nome_estoque
            entrada_atual['fornecedor_id'] = entrada.fornecedor_id
            entrada_atual['nome_do_fornecedor'] = fornecedor.nome_fantasia
            entrada_atual['data_entrada'] = entrada.data_entrada
            entrada_atual['matricula_responsável'] = entrada.funcionario_matricula
            entrada_atual['nome_responsável'] = funcionario_responsavel.nome
            listadeentradas.append(entrada_atual)
        return jsonify(listadeentradas)
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})

@app.route('/entradasestoque', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_entradas_logado(funcionario):
    try:
        entradas_ao_estoque = EntradasEstoque.query.filter_by(funcionario_matricula= funcionario.matricula)
        listadeentradas = []
        for entrada in entradas_ao_estoque:
            produto = Produtos.query.filter_by(id=entrada.produto_id).first()
            fornecedor = Fornecedores.query.filter_by(id=entrada.fornecedor_id).first()
            funcionario_responsavel = Funcionarios.query.filter_by(matricula=entrada.funcionario_matricula).first()
            entrada_atual = {}
            entrada_atual['id'] = entrada.id
            entrada_atual['nota'] = entrada.nota
            entrada_atual['produto_id'] = entrada.produto_id
            entrada_atual['produto'] = produto.nome_estoque
            entrada_atual['fornecedor_id'] = entrada.fornecedor_id
            entrada_atual['nome_do_fornecedor'] = fornecedor.nome_fantasia
            entrada_atual['data_entrada'] = entrada.data_entrada
            entrada_atual['matricula_responsável'] = entrada.funcionario_matricula
            entrada_atual['nome_responsável'] = funcionario_responsavel.nome
            listadeentradas.append(entrada_atual)
        if len(listadeentradas) == 0:
            return jsonify({'mensagem': f'O {funcionario.nome} ainda não cadastrou nenhuma saída ao estoque'})
        return jsonify(listadeentradas)
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'})


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
        
        entrada_ao_estoque_alterar = request.get_json()
        quantidade = entrada_estoque.quantidade
        
        try:
            if 'produto_id' in entrada_ao_estoque_alterar:
                produto_id = entrada_ao_estoque_alterar['produto_id']
                produto_existente = Produtos.query.filter_by(id=produto_id).first()
                if not produto_existente:
                    return jsonify({'mensagem': 'Produto inexistente'}), 400
                
                if produto_id != entrada_estoque.produto_id:
                    produto_diminuir = Produtos.query.filter_by(id=entrada_estoque.produto_id).first()
                    quantidade_anterior = entrada_estoque.quantidade
                    produto_diminuir.quantidade -= quantidade_anterior
                    entrada_estoque.produto_id = produto_id

                    if 'quantidade' in entrada_ao_estoque_alterar:
                        nova_quantidade = entrada_ao_estoque_alterar['quantidade']
                        nova_quantidade = int(nova_quantidade)
                        produto_existente.quantidade += nova_quantidade
                        quantidade = nova_quantidade
                    else:
                        produto_existente.quantidade += quantidade_anterior
                        quantidade = quantidade_anterior
                        produto = produto_existente
        except KeyError:
            pass
        
        try:
            if 'quantidade' in entrada_ao_estoque_alterar:
                nova_quantidade = entrada_ao_estoque_alterar['quantidade']
                nova_quantidade = int(nova_quantidade)
                
                # Atualiza a quantidade do produto no estoque
                produto = Produtos.query.get(entrada_estoque.produto_id)
                produto.quantidade -= entrada_estoque.quantidade  # Remove a quantidade anterior
                produto.quantidade += nova_quantidade  # Adiciona a nova quantidade
                entrada_estoque.quantidade = nova_quantidade
                quantidade = nova_quantidade
        except KeyError:
            pass
        
        try:
            if 'fornecedor_id' in entrada_ao_estoque_alterar:
                fornecedor_existente = Fornecedores.query.get(entrada_ao_estoque_alterar['fornecedor_id'])
                if not fornecedor_existente:
                    return jsonify({'mensagem': 'Fornecedor inexistente'}), 400
                entrada_estoque.fornecedor_id = entrada_ao_estoque_alterar['fornecedor_id']
        except KeyError:
            pass
        
        try:
            if 'nota' in entrada_ao_estoque_alterar:
                entrada_estoque.nota = entrada_ao_estoque_alterar['nota']
        except KeyError:
            pass
        
        db.session.commit()
        
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': quantidade
        }
        
        return jsonify({'Entrada de estoque atualizada': response})
    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500

#delete
@app.route('/entradasestoque/<int:id>', methods=['DELETE'])
@token_obrigatorio
def excluir_entrada_ao_estoque(funcionario, id):
    try:
        entrada_estoque = EntradasEstoque.query.get(id)
        if not entrada_estoque:
            return jsonify({'mensagem': 'Entrada de estoque não encontrada'}), 404
        if entrada_estoque.funcionario_matricula != funcionario.matricula:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar esta entrada de estoque'}), 403
        try:
            quantidade = entrada_estoque.quantidade
            quantidade = int(quantidade)
            produto = Produtos.query.get(entrada_estoque.produto_id)
            produto.quantidade -= quantidade
        except Exception as e:
            print(e)
            return jsonify({'mensagem': 'Erro ao atualizar a quantidade'})
        db.session.delete(entrada_estoque)
        db.session.commit()
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': quantidade
        }
        return jsonify({'Entrada excluída com sucesso': response})    
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500