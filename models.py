# models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    industry = db.Column(db.String(255))
    budget = db.Column(db.Numeric(10,2))
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(255))
    niche = db.Column(db.String(255))
    reach = db.Column(db.Numeric(10,2))
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(10,2))
    visibility = db.Column(db.Enum('public', 'private'))
    goals = db.Column(db.Text)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'))
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'))
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Numeric(10,2))
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def init_db(app):
    with app.app_context():
        db.create_all()

    # Check if there are any admins already (for example)
    if Admin.query.first() is None:
        # Add dummy data
        admin = Admin(name='admin', password='password')
        db.session.add(admin)
        db.session.commit()

        sponsor = Sponsor(password='sponsor_password', name='sponsor_name', industry='industry_name', budget=10000)
        db.session.add(sponsor)
        db.session.commit()

        influencer = Influencer(password='influencer_password', name='influencer_name', category='category_name', niche='niche_name', reach=5000)
        db.session.add(influencer)
        db.session.commit()
        
        start_date = datetime.strptime('2024-01-01', '%Y-%m-%d').date()
        end_date = datetime.strptime('2025-12-31', '%Y-%m-%d').date()
        
        campaign = Campaign(name='campaign_name', description='campaign_description', start_date=start_date, end_date=end_date, budget=5000, visibility='public', goals='campaign_goals', sponsor_id=sponsor.id)
        db.session.add(campaign)
        db.session.commit()

        ad_request = AdRequest(campaign_id=campaign.id, influencer_id=influencer.id, messages='ad_request_messages', requirements='ad_request_requirements', payment_amount=200, status='pending')
        db.session.add(ad_request)
        db.session.commit()

        