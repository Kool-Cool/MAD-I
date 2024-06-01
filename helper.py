# helper.py
# helper functions for database

from models import User, Campaign, Sponsor


def get_data_by_name(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.to_dict()
    else:
        return None


def get_campaign_by_userid(user_id):
    sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
    sponsor_id = sponsor_data.sponsor_id
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

    if campaigns is not None:
        return [campaign.to_dict() for campaign in campaigns]
    else:
        return None
