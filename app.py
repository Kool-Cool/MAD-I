#  controller app.py

from flask import Flask , render_template
from flask import jsonify
from models import db ,init_db ,Admin , Sponsor , Influencer ,Campaign , AdRequest
from api import api

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

app.register_blueprint(api, url_prefix='/api')  

@app.before_request
def create_tables():
    init_db(app)


#Routes
@app.route("/")
def home():
    return render_template("index.html")








if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)