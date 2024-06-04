#  controller app.py

from flask import Flask , render_template , session ,flash , redirect , url_for
from flask import jsonify
from models import db ,init_db , Sponsor , Influencer ,Campaign , AdRequest

from api import api
from admin import admin
from sponsor import sponsor
from influencer import influencer

from helper import get_data_by_name

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


app.register_blueprint(api, url_prefix='/api')  
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(sponsor, url_prefix='/sponsor')
app.register_blueprint(influencer , url_prefix='/influencer')


@app.before_request
def create_tables():
    init_db(app)


#Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()

    flash("Log out successful", "success")
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)