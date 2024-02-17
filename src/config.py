from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Configuração da chave secreta para proteger sessões e outros dados
app.config['SECRET_KEY'] = 'Sua chave'

# Configuração da URI do banco de dados SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'Sua conexão ao banco'

# Inicialização do objeto de banco de dados SQLAlchemy
db = SQLAlchemy(app)

# Inicialização do objeto Bcrypt para criptografia de senhas
bcrypt = Bcrypt(app)
