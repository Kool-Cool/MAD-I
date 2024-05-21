#api.py
from flask import Blueprint, jsonify
from models import Admin, Sponsor, Influencer, Campaign, AdRequest

api = Blueprint('api', __name__)

@api.route('/data', methods=['GET'])
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

@api.route('/sponsors' , methods=['GET'])
def get_all_sponsors():
    sponsors = Sponsor.query.all()

    return jsonify([sponsor.to_dict() for sponsor in sponsors])
    
