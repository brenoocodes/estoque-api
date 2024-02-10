from datetime import datetime  # Para manipulation de datas e horas
from src.config import app, db
 # Importa o objeto db, que é uma instância do SQLAlchemy definida no __init__.py

class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    matricula = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    administrador = db.Column(db.Boolean, default=False)

class Fornecedores(db.Model):
    __tablename__ = 'fornecedores'
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    razao_social = db.Column(db.String(255), nullable=False)
    nome_fantasia = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(14), nullable=False)

class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, index=True)
    nome_estoque = db.Column(db.String(255), nullable=False)
    medida = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, default=0.0)
    quantidade = db.Column(db.Integer)

    fornecedores = db.relationship('Fornecedores', secondary='produtos_fornecedores', backref=db.backref('produtos', lazy='dynamic'))

class ProdutosFornecedores(db.Model):
    __tablename__ = 'produtos_fornecedores'
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), primary_key=True)

class EntradasEstoque(db.Model):
    __tablename__ = 'entradaestoque'
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.String(50), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantidade = db.Column(db.Integer, nullable=False)
    funcionario_matricula = db.Column(db.Integer, db.ForeignKey('funcionarios.matricula'), nullable=False)

class SaidasEstoque(db.Model):
    __tablename__='saidasestoque'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    data_saida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantidade = db.Column(db.Integer, nullable=False)
    funcionario_responsavel = db.Column(db.Integer, db.ForeignKey('funcionarios.matricula'), nullable=False)
    funcionario_requisitante = db.Column(db.Integer, db.ForeignKey('funcionarios.matricula'), nullable=False)

# Criar o database
# with app.app_context():
#     db.drop_all()
#     db.create_all()