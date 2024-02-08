from src.config import *
from src.models import *
from src.funcionarios import *

@app.route('/', methods=['GET'])
def home():
    return '<p>Ok</p>'


if __name__ == '__main__':
    app.run(debug=True)