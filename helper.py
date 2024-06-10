# helper.py
# helper functions for database

from models import User, Campaign, Sponsor, AdRequest, Influencer, Negotiation, db
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


# def get_adrequest_by_userid(user_id):
#     """
#     Finding LIST OF Ad_Campaign for RespectiveUSer (sponsor)
#     """

#     # Find `campaign_id`
#     # find `sponsor_id` for respetive campaings and its ID
#     # We `have USER_ID`
#     sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
#     sponsor_id = sponsor_data.sponsor_id
#     campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
#     data_campaigns = [campaign.to_dict() for campaign in campaigns]
#     # print("TYPE of campaing" , type(data_campaigns))
#     # print(data_campaigns)
#     # print()

#     list_of_campaign_id = [ c["campaign_id"] for c in  data_campaigns ]

#     # print(type(list_of_campaign_id))
#     # print(list_of_campaign_id)
#     # print()

#     respective_adreqt_for_campaign = []
#     for c_ID in list_of_campaign_id:
#         temp_data = AdRequest.query.filter_by(campaign_id=c_ID).all()
#         # print("THIS IS OLD TEMP DATA" ,temp_data)
#         # print()
#         if temp_data:

#             for c in temp_data :

#                 c_dict = c.to_dict()
#                 # print(c_dict)
#                 nego = Negotiation.query.filter_by(ad_request_id = c_dict["ad_request_id"], influencer_id=c_dict["influencer_id"]).first()

#                 if nego:
#                     c_dict["negotiation_status"] = nego.negotiation_status
#                     c_dict["proposed_payment_amount"] = nego.proposed_payment_amount
#                 else:
#                     c_dict["negotiation_status"] = 'None'
#                     c_dict["proposed_payment_amount"] = 'None'

#                 respective_adreqt_for_campaign.append(c_dict)


#             # print()

#     # print(respective_adreqt_for_campaign)
#     return respective_adreqt_for_campaign


def get_adrequest_by_userid(user_id):
    """
    Finding LIST OF Ad_Campaign for Respective User (sponsor)
    """
    # Find sponsor ID for the given user ID
    sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
    if not sponsor_data:
        return []

    sponsor_id = sponsor_data.sponsor_id

    # Find campaigns associated with the sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

    # Collect campaign IDs
    list_of_campaign_id = [campaign.campaign_id for campaign in campaigns]

    # Initialize a list to hold ad request details
    respective_adreqt_for_campaign = []

    for c_ID in list_of_campaign_id:
        # Find ad requests for the given campaign ID
        temp_data = AdRequest.query.filter_by(campaign_id=c_ID).all()

        if temp_data:
            for c in temp_data:
                c_dict = c.to_dict()
                nego = Negotiation.query.filter_by(
                    ad_request_id=c_dict["ad_request_id"],
                    influencer_id=c_dict["influencer_id"],
                ).first()

                if nego:
                    c_dict["negotiation_status"] = nego.negotiation_status
                    c_dict["proposed_payment_amount"] = str(
                        nego.proposed_payment_amount
                    )
                else:
                    c_dict["negotiation_status"] = "None"
                    c_dict["proposed_payment_amount"] = "None"

                # Adding required fields to the dictionary
                respective_adreqt_for_campaign.append(
                    {
                        "ad_request_id": c_dict["ad_request_id"],
                        "campaign_id": c.campaign_id,
                        "influencer_id": c.influencer_id,
                        "requirements": c.requirements,
                        "payment_amount": str(c.payment_amount),
                        "status": c.status,
                        "messages": c.messages,
                        "proposed_payment_amount": c_dict["proposed_payment_amount"],
                        "negotiation_status": c_dict["negotiation_status"],
                    }
                )

    return respective_adreqt_for_campaign


""" 
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
 """
# Function which will return all public ad_request and along with
# its negotiation for respective influencer !!
""" def get_influencer_campaigns(influencer_id):
    

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
            Negotiation.negotiation_id,  # Add negotiation_id to the query
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
            "negotiation_status": campaign.negotiation_status,
            "negotiation_id": campaign.negotiation_id  # Add negotiation_id to the dictionary
        }
        data.append(campaign_data)

    return data
 """


import json


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
            Negotiation.negotiation_id,
            case(
                (
                    Negotiation.negotiation_id.isnot(None),
                    Negotiation.proposed_payment_amount,
                ),
                else_=AdRequest.payment_amount,
            ).label("negotiated_amount"),
            case(
                (
                    Negotiation.negotiation_id.isnot(None),
                    Negotiation.negotiation_status,
                ),
                else_=AdRequest.status,
            ).label("negotiation_status"),
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
            "start_date": (
                campaign.start_date.strftime("%Y/%m/%d")
                if campaign.start_date
                else None
            ),
            "end_date": (
                campaign.end_date.strftime("%Y/%m/%d") if campaign.end_date else None
            ),
            "ad_request_id": campaign.ad_request_id,
            "influencer_id": campaign.influencer_id,
            "messages": campaign.messages,
            "payment_amount": str(campaign.payment_amount),
            "requirements": campaign.requirements,
            "status": campaign.status,
            "negotiated_amount": str(campaign.negotiated_amount),
            "negotiation_status": campaign.negotiation_status,
            "negotiation_id": campaign.negotiation_id,
        }
        data.append(campaign_data)

    return data


def get_sponsor_campaigns_info(sponsor_id):
    # Query to get all the campaigns, ad_requests, and negotiations for the sponsor
    campaigns = (
        db.session.query(
            Campaign.campaign_id,
            AdRequest.influencer_id,
            AdRequest.requirements,
            AdRequest.payment_amount,
            AdRequest.status,
            AdRequest.messages,
            case(
                (
                    Negotiation.negotiation_id.isnot(None),
                    Negotiation.proposed_payment_amount,
                ),
                else_=AdRequest.payment_amount,
            ).label("proposed_payment_amount"),
            case(
                (
                    Negotiation.negotiation_id.isnot(None),
                    Negotiation.negotiation_status,
                ),
                else_=AdRequest.status,
            ).label("negotiation_info"),
        )
        .join(AdRequest, AdRequest.campaign_id == Campaign.campaign_id)
        .outerjoin(Negotiation, Negotiation.ad_request_id == AdRequest.ad_request_id)
        .filter(Campaign.sponsor_id == sponsor_id)
        .all()
    )

    data = []

    for campaign in campaigns:
        campaign_data = {
            "Campaign Id": campaign.campaign_id,
            "Influencer Id": campaign.influencer_id,
            "Requirements": campaign.requirements,
            "Payment Amount": str(campaign.payment_amount),
            "Status": campaign.status,
            "Message": campaign.messages,
            "Proposed Payment Amount": str(campaign.proposed_payment_amount),
            "Negotiation Info": campaign.negotiation_info,
            "Action": (
                "accepted" if campaign.negotiation_info == "accepted" else "pending"
            ),
        }
        data.append(campaign_data)

    return data
