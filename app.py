from src import app
from src.config.login import *
from src.routes.funcionarios.index import *
from src.routes.produtos.index import *
from src.routes.fornecedores.index import *
from src.routes.afaop.index import *
from src.routes.apaof.index import *
from src.routes.entradasestoque import *
from src.routes.saidasestoque import * 


@app.route('/', methods=['GET'])
def home():
    return '<h2>API controle de estoque</h2>'



if __name__ == '__main__':
    app.run(debug=True)