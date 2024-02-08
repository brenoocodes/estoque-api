from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FsjdejefweFRFWG#3452%@%@TRWWewrgwg4rtwghyettwwt254536g'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:breno19042003@brenocodesbanco.clysq3fxahpq.us-east-1.rds.amazonaws.com/brenocodesbanco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:breno19042003@localhost/estoqueapi'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
verificador = URLSafeTimedSerializer(app.config['SECRET_KEY'])



