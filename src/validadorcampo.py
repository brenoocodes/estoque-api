from flask import jsonify, request
from functools import wraps
from json import JSONDecodeError

def verifica_campos_tipos(campos_obrigatorios, tipos_esperados):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                nova_entrada_ao_estoque = request.get_json()
                if nova_entrada_ao_estoque is None:
                    return jsonify({'mensagem': 'JSON inválido ou ausente.'}), 400
                
                for campo in nova_entrada_ao_estoque:
                    if campo not in campos_obrigatorios:
                        return jsonify({'mensagem': f'O campo {campo} não é esperado, favor confirmar os campos necessários'}), 400
                for campo, tipo_esperado in tipos_esperados.items():
                    if campo not in nova_entrada_ao_estoque:
                        return jsonify({'mensagem': f'O campo obrigatório {campo} não foi encontrado, por favor verificar.'}), 400
                    
                    valor = nova_entrada_ao_estoque[campo]

                    if not isinstance(valor, tipo_esperado):
                        return jsonify({'mensagem': f'O campo {campo} deve ser do tipo {tipo_esperado.__name__}.'}), 400
                
                return func(*args, **kwargs)
            except JSONDecodeError:
                return jsonify({'mensagem': 'Erro ao decodificar JSON. Certifique-se de que o JSON esteja formatado corretamente.'}), 400  
            except Exception as e:
                print(e)
                return jsonify({'mensagem': 'Ocorreu um erro ao processar a solicitação.'}), 500
        return wrapper
    return decorator

def verifica_alterar(campos_obrigatorios, tipos_esperados):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                nova_entrada_ao_estoque_alterar = request.get_json()
                if nova_entrada_ao_estoque_alterar is None:
                    return jsonify({'mensagem': 'JSON inválido ou ausente.'}), 400
                
                for campo in nova_entrada_ao_estoque_alterar:
                    if campo not in campos_obrigatorios:
                        return jsonify({'mensagem': f'O campo {campo} não é esperado, favor confirmar os campos necessários'})
                
                for campo, tipo_esperado in tipos_esperados.items():
                    valor = nova_entrada_ao_estoque_alterar.get(campo)
                    if valor is not None and not isinstance(valor, tipo_esperado):
                        return jsonify({'mensagem': f'O campo {campo} deve ser do tipo {tipo_esperado.__name__}.'}), 400
                
                return func(*args, **kwargs)
            
            except JSONDecodeError:
                return jsonify({'mensagem': 'Erro ao decodificar JSON. Certifique-se de que o JSON esteja formatado corretamente.'}), 400
            except Exception as e:
                print(e)
                return jsonify({'mensagem': 'Ocorreu um erro ao processar a solicitação.'}), 500
        return wrapper
    return decorator
