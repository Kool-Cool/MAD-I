#  controller

from flask import Flask
from flask import jsonify
from models import db ,init_db ,Admin , Sponsor , Influencer ,Campaign , AdRequest


app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


@app.before_request
def create_tables():
    init_db(app)


#Routes
@app.route("/")
def home():
    return "Initial Setup"



@app.route('/api/data', methods=['GET'])
def get_all_data():
    admins = Admin.query.all()
    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()

    return jsonify({
        'admins': [admin.to_dict() for admin in admins],
        'sponsors': [sponsor.to_dict() for sponsor in sponsors],
        'influencers': [influencer.to_dict() for influencer in influencers],
        'campaigns': [campaign.to_dict() for campaign in campaigns],
        'ad_requests': [ad_request.to_dict() for ad_request in ad_requests]
    })


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run()