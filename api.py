# api.py
from flask import Blueprint, jsonify
from models import (
    User,
    Sponsor,
    Influencer,
    Campaign,
    AdRequest,
    Negotiation,
    UserFlag,
    CampaignFlag,
)

api = Blueprint("api", __name__)


@api.route("/data", methods=["GET"])
def get_all_data():
    users = User.query.all()
    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()
    negotiations = Negotiation.query.all()
    user_flags = UserFlag.query.all()
    campaign_flags = CampaignFlag.query.all()

    return jsonify(
        {
            "users": [User.to_dict() for User in users],
            "sponsors": [sponsor.to_dict() for sponsor in sponsors],
            "influencers": [influencer.to_dict() for influencer in influencers],
            "campaigns": [campaign.to_dict() for campaign in campaigns],
            "ad_requests": [ad_request.to_dict() for ad_request in ad_requests],
            "negotiations": [negotiation.to_dict() for negotiation in negotiations],
            "user_flag": [user_flag.to_dict() for user_flag in user_flags],
            "campaign_flag": [
                campaign_flag.to_dict() for campaign_flag in campaign_flags
            ],
        }
    )


@api.route("/sponsors", methods=["GET"])
def get_all_sponsors():
    sponsors = Sponsor.query.all()

    return jsonify([sponsor.to_dict() for sponsor in sponsors])
