from flask import jsonify, request
from src.config import app, db
from src.validadorcampo import *
from src.login import *
from src.models import Produtos, Fornecedores, EntradasEstoque, Funcionarios

@app.route('/entradasestoque/todos', methods=['GET'])
@token_obrigatorio
def exibir_todas_as_entradas(funcionario):
    if not funcionario.administrador:
            return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403 
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
        if len(listadeentradas) == 0:
            return jsonify({'Mensagem': 'Nenhuma entrada foi cadastrada'}),200
        return jsonify(listadeentradas), 200
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500

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
            return jsonify({'mensagem': f'O {funcionario.nome} ainda não cadastrou nenhuma entrada ao estoque'}), 400
        return jsonify(listadeentradas), 200
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500

@app.route('/entradasestoque', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['nota', 'produto_id', 'fornecedor_id', 'quantidade'], {'nota': str, 'produto_id': int, 'fornecedor_id': int, 'quantidade': int})
def adicionar_entrada_ao_estoque(funcionario):
    try:
        nova_entrada_ao_estoque = request.get_json()
        produto = nova_entrada_ao_estoque['produto_id']
        produto_existente = Produtos.query.filter_by(id=produto).first()
        fornecedor_id = nova_entrada_ao_estoque['fornecedor_id']
        if not produto_existente:
            return jsonify({'mensagem': 'Produto inexistente'}), 400
        fornecedor_existente = Fornecedores.query.filter_by(id=fornecedor_id).first()
        if not fornecedor_existente:
            return jsonify({'mensagem': 'Fornecedor inexistente'}), 400
       
        quantidade = nova_entrada_ao_estoque['quantidade']
        if quantidade > 0:
            produto_existente.quantidade += quantidade
        else:
            return jsonify({'mensagem': 'A quantidade de produtos de entrada deve ser maior que zero'}), 400
        entrada_estoque = EntradasEstoque(
            produto_id=produto,
            fornecedor_id=fornecedor_id,
            quantidade=quantidade,
            nota=nova_entrada_ao_estoque['nota'],
            funcionario_matricula=funcionario.matricula
        )  
        db.session.add(entrada_estoque)
        db.session.commit()
        response = {
            'produto_id':produto_existente.id,
            'produto_nome': produto_existente.nome_estoque,
            'fornecedor_id':fornecedor_id,
            'quantidade':quantidade,
            'nota':nova_entrada_ao_estoque['nota'],
           'funcionario_matricula':funcionario.matricula,
           'funcionario_nome': funcionario.nome,
           'fornecedor_nome': fornecedor_existente.nome_fantasia
        }
        return jsonify({'Nova entrada ao estoque cadastrada com sucesso': response}), 200 
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Ocorreu um erro ao processar a solicitação.'}), 500

@app.route('/entradasestoque/<int:id>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['nota', 'produto_id', 'fornecedor_id', 'quantidade'], {'nota': str, 'produto_id': int, 'fornecedor_id': int, 'quantidade': int})
def alterar_entrada_ao_estoque(funcionario, id):
    try:
        nova_entrada_ao_estoque_alterar = request.get_json()
        entrada_ao_estoque = EntradasEstoque.query.get(id)
        if not funcionario.administrador:
            if entrada_ao_estoque.funcionario_matricula != funcionario.matricula:
                return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403 
        produto = Produtos.query.filter_by(id=entrada_ao_estoque.produto_id).first()
        quantidade = entrada_ao_estoque.quantidade
        nota = entrada_ao_estoque.nota
        fornecedor = Fornecedores.query.filter_by(id=entrada_ao_estoque.fornecedor_id).first()
        if not entrada_ao_estoque:
            return jsonify({'mensagem': 'Entrada ao estoque inexistente'}), 400
        try:
            if 'produto_id' in nova_entrada_ao_estoque_alterar and 'quantidade' in nova_entrada_ao_estoque_alterar:
                print('passei no produto_id e quantidade')
                nova_quantidade = nova_entrada_ao_estoque_alterar['quantidade']
                produto_antigo = Produtos.query.filter_by(id=entrada_ao_estoque.produto_id).first()
                produto_novo = Produtos.query.filter_by(id=nova_entrada_ao_estoque_alterar['produto_id']).first()
                if not produto_novo:
                    return jsonify({'mensagem': 'Não existe produto com esse id'}), 400
                produto_antigo.quantidade -= quantidade
                entrada_ao_estoque.produto_id = produto_novo.id
                entrada_ao_estoque.quantidade = nova_quantidade
                produto_novo.quantidade  += nova_quantidade
                quantidade = nova_quantidade
                produto = produto_novo
            if 'quantidade' in nova_entrada_ao_estoque_alterar:
                print('passei só quantidade')
                produto_antigo = Produtos.query.filter_by(id=entrada_ao_estoque.produto_id).first()
                produto_antigo.quantidade -= quantidade
                nova_quantidade = nova_entrada_ao_estoque_alterar['quantidade']
                produto_antigo.quantidade += nova_quantidade
                entrada_ao_estoque.quantidade = nova_quantidade
                quantidade = nova_quantidade
                produto = produto_antigo
            elif 'produto_id' in nova_entrada_ao_estoque_alterar:
                print('passei só produto_id')
                produto_antigo = Produtos.query.filter_by(id=entrada_ao_estoque.produto_id).first()
                produto_novo = Produtos.query.filter_by(id=nova_entrada_ao_estoque_alterar['produto_id']).first()
                if not produto_novo:
                    return jsonify({'mensagem': 'Não existe produto com esse id'}), 400
                produto_antigo.quantidade -= quantidade
                entrada_ao_estoque.produto_id = produto_novo.id
                produto_novo.quantidade  += quantidade
                produto = produto_novo
        except KeyError:
            pass
        try:
            if 'fornecedor_id' in nova_entrada_ao_estoque_alterar:
                novo_fornecedor = Fornecedores.query.filter_by(id=nova_entrada_ao_estoque_alterar['fornecedor_id']).first()
                if not novo_fornecedor:
                    return jsonify({'mensagem': 'Esse fornecedor não existe'}), 400
                entrada_ao_estoque.fornecedor_id = novo_fornecedor.id 
                fornecedor = novo_fornecedor     
        except KeyError:
            pass
        
        try:
            if 'nota' in nova_entrada_ao_estoque_alterar:
                entrada_ao_estoque.nota = nova_entrada_ao_estoque_alterar['nota']
                nota = nova_entrada_ao_estoque_alterar['nota']
        except KeyError:
            pass

        db.session.commit()
        response = {
            'produto_id' : produto.id,
            'funcionário_responsavel': funcionario.nome,
            'nota': nota,
            'produto_nome': produto.nome_estoque,
            'quantidade': quantidade,
            'fornecedor_id': fornecedor.id,
            'fornecedor_nome': fornecedor.nome_fantasia
        }

        
        return jsonify({'Entrada alterada com sucesso': response}), 200
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'erro na solicitação'}), 500


#delete
@app.route('/entradasestoque/<int:id>', methods=['DELETE'])
@token_obrigatorio
def excluir_entrada_ao_estoque(funcionario, id):
    try:
        entrada_estoque = EntradasEstoque.query.get(id)
        if not entrada_estoque:
            return jsonify({'mensagem': 'Entrada de estoque não encontrada'}), 404
        if not funcionario.administrador:
            if entrada_estoque.funcionario_matricula != funcionario.matricula:
                return jsonify({'mensagem': 'Você não tem permissão para atualizar essa saída de estoque'}), 403 
        try:
            quantidade = entrada_estoque.quantidade
            quantidade = int(quantidade)
            produto = Produtos.query.get(entrada_estoque.produto_id)
            produto.quantidade -= quantidade
        except Exception as e:
            print(e)
            return jsonify({'mensagem': 'Erro ao atualizar a quantidade'}), 500
        db.session.delete(entrada_estoque)
        db.session.commit()
        response = {
            'matricula': funcionario.matricula,
            'funcionario_nome': funcionario.nome,
            'produto': produto.nome_estoque,
            'quantidade': quantidade
        }
        return jsonify({'Entrada excluída com sucesso': response}),200   
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Algum erro'}), 500