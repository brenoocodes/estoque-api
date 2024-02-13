from src.config import *
from src.funcionarios import *
from src.fornecedores import *
from src.produtos import *
from src.fornecedorproduto import *
from src.login import *
from src.entradasestoque import *
from src.saidasestoque import *


@app.route('/', methods=['GET'])
def home():
    return '<h2>API controle de estoque</h2>'


if __name__ == '__main__':
    app.run(debug=True)