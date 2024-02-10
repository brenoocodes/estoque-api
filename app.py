from src.config import *
from src.models import *
from src.funcionarios import *
from src.fornecedores import *
from src.produtos import *
from src.fornecedorproduto import *
from src.login import *
from src.entradasestoque import *

@app.route('/', methods=['GET'])
def home():
    return '<p>Ok</p>'


if __name__ == '__main__':
    app.run(debug=True)