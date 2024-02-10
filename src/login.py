from flask import jsonify, request, make_response
from src.config import app, bcrypt
from datetime import datetime, timedelta
from sqlalchemy import or_
from src.models import Funcionarios
from functools import wraps
import jwt

blacklisted_tokens = []

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify ({'mensagem': 'Token não incluído'}, 401)
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            funcionario = Funcionarios.query.filter_by(matricula=resultado['matricula']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token é inválido'}), 401
        
        return f(funcionario, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    funcionario = Funcionarios.query.filter(or_(Funcionarios.email == auth.username, Funcionarios.matricula == auth.username)).first()
    if not funcionario:
        return make_response('Não existe esse usuário cadastrado', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    if bcrypt.check_password_hash(funcionario.senha, auth.password):
        print('Senha válida')
        token = jwt.encode({'matricula': funcionario.matricula, 'exp': (datetime.utcnow() + timedelta(days=20)).timestamp()}, app.config['SECRET_KEY'])
        resposta_data = {
            'token': token,
            'matricula': funcionario.matricula,
            'nome': funcionario.nome,
            'email': funcionario.email,
            'administrador': funcionario.administrador
        }
        return jsonify(resposta_data)
    else:
        return make_response('Senha incorreta', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})

