# helper.py
# helper functions for database

from models import User, Campaign, Sponsor , AdRequest , Influencer, Negotiation ,db
import json
from datetime import datetime
from sqlalchemy import func, case



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
    

def get_adrequest_by_userid(user_id):
    """  
    Finding LIST OF Ad_Campaign for RespectiveUSer (sponsor)
    """

    # Find `campaign_id`
    # find `sponsor_id` for respetive campaings and its ID
    # We `have USER_ID`
    sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
    sponsor_id = sponsor_data.sponsor_id
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
    data_campaigns = [campaign.to_dict() for campaign in campaigns]
    # print("TYPE of campaing" , type(data_campaigns))
    # print(data_campaigns)
    # print()

    list_of_campaign_id = [ c["campaign_id"] for c in  data_campaigns ]

    # print(type(list_of_campaign_id))
    # print(list_of_campaign_id)
    # print()

    respective_adreqt_for_campaign = []
    for c_ID in list_of_campaign_id:
        temp_data = AdRequest.query.filter_by(campaign_id=c_ID).all()
        # print("THIS IS OLD TEMP DATA" ,temp_data)
        # print()
        if temp_data:
   
            for c in temp_data :

                respective_adreqt_for_campaign.append(c.to_dict())
            
            
            # print()
    
    # print(respective_adreqt_for_campaign)
    return respective_adreqt_for_campaign





# Function which will return all public ad_request and along with
# its negontiation for respective influencer !!
def get_influencer_campaigns(influencer_id):
    

    # Query to get all the campaigns, ad_requests, and negotiations for the influencer
    campaigns = (
        db.session.query(
            Campaign.campaign_id,
            Campaign.name.label("campaign_name"),
            Campaign.description,
            Campaign.goals,
            Campaign.niche,
            Campaign.sponsor_id,
            Campaign.start_date,
            Campaign.end_date,
            AdRequest.ad_request_id,
            AdRequest.messages,
            AdRequest.payment_amount,
            AdRequest.requirements,
            AdRequest.status,
            AdRequest.influencer_id,
            case(
               
                    (Negotiation.negotiation_id.isnot(None), Negotiation.proposed_payment_amount)
               ,
                else_=AdRequest.payment_amount
            ).label("negotiated_amount"),
            case(
               
                    (Negotiation.negotiation_id.isnot(None), Negotiation.negotiation_status)
               ,
                else_="pending"
            ).label("negotiation_status")
        )
        .join(AdRequest, AdRequest.campaign_id == Campaign.campaign_id)
        .outerjoin(Negotiation, Negotiation.ad_request_id == AdRequest.ad_request_id)
        .filter(AdRequest.influencer_id == influencer_id)
        .all()
    )

    data = []

    for campaign in campaigns:
        campaign_data = {
            "campaign_id": campaign.campaign_id,
            "campaign_name": campaign.campaign_name,
            "description": campaign.description,
            "goals": campaign.goals,
            "niche": campaign.niche,
            "sponsor_id": campaign.sponsor_id,
            "start_date": campaign.start_date.strftime("%Y/%m/%d") if campaign.start_date else None,
            "end_date": campaign.end_date.strftime("%Y/%m/%d") if campaign.end_date else None,
            "ad_request_id": campaign.ad_request_id,
            "influencer_id": campaign.influencer_id,
            "messages": campaign.messages,
            "payment_amount": str(campaign.payment_amount),
            "requirements": campaign.requirements,
            "status": campaign.status,
            "negotiated_amount": str(campaign.negotiated_amount),
            "negotiation_status": campaign.negotiation_status
        }
        data.append(campaign_data)

    return data

