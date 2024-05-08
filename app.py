import os
import bcrypt
from flask import Flask, request, abort, jsonify, render_template
from api.v1.views import app_views
from models import db
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from models.question import Question
from models.quiz import Quiz
from models.teacher import Teacher
from models.score import Score
from models.student import Student


host = os.getenv('DATABASEHOST')
password = os.getenv('DATABASEPASSWORD')
user = os.getenv('DATABASEUSERNAME')
database = os.getenv('DATABASE')
mail_username = os.getenv('mail_username')
mail_password = os.getenv('mail_password')
db_uri = 'mysql+pymysql://{}:{}@{}/{}'.format(user, password, host, database)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.register_blueprint(app_views)

# handles sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.secret_key = os.urandom(24)
mail = Mail(app)

db.init_app(app)

#migration handler
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return db.get_or_404(Teacher, id)

@app.route('/')
def home():
    print('something')
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(threaded=True, debug=True)