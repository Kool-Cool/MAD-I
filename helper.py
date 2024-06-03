# helper.py
# helper functions for database

from models import User, Campaign, Sponsor , AdRequest


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





