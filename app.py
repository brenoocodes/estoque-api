from config import *
from models import *
from autor import *

@app.route('/')
def home():
    return '<p>Ok</p>'


if __name__ == '__main__':
    app.run(debug=True)