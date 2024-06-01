# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.orm import validates
from flask import flash
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.Enum("admin", "sponsor", "influencer"), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    sponsors = db.relationship("Sponsor", backref="user", lazy=True)
    influencers = db.relationship("Influencer", backref="user", lazy=True)
    user_flags = db.relationship(
        "UserFlag", foreign_keys="UserFlag.flagged_by", backref="flagger", lazy=True
    )
    flagged_by_user_flags = db.relationship(
        "UserFlag", foreign_keys="UserFlag.user_id", backref="flagged_user", lazy=True
    )
    campaign_flags = db.relationship(
        "CampaignFlag",
        foreign_keys="CampaignFlag.flagged_by",
        backref="flagger",
        lazy=True,
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sponsor(db.Model):
    __tablename__ = "sponsors"

    sponsor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    company_name = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    budget = db.Column(db.Numeric(10, 2))

    campaigns = db.relationship("Campaign", backref="sponsor", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Influencer(db.Model):
    __tablename__ = "influencers"

    influencer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    niche = db.Column(db.String(255))
    reach = db.Column(db.Integer)

    ad_requests = db.relationship("AdRequest", backref="influencer", lazy=True)
    negotiations = db.relationship("Negotiation", backref="influencer", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Campaign(db.Model):
    __tablename__ = "campaigns"

    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sponsor_id = db.Column(
        db.Integer, db.ForeignKey("sponsors.sponsor_id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    visibility = db.Column(db.Enum("public", "private"),default="public")
    goals = db.Column(db.Text, nullable=False)
    niche = db.Column(db.String(255), nullable=False)

    ad_requests = db.relationship("AdRequest", backref="campaign", lazy=True)
    campaign_flags = db.relationship("CampaignFlag", backref="campaign", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @validates("end_date")
    def validate_end_date(self, key, end_date):
        # print(end_date)
        # print(type(end_date))
        if self.start_date and end_date:
            if end_date < self.start_date:
                # raise ValueError("End date must be greater than start date")
                flash("End date must be greater than start date", "error")
        return end_date


class AdRequest(db.Model):
    __tablename__ = "ad_requests"

    ad_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(
        db.Integer, db.ForeignKey("campaigns.campaign_id"), nullable=False
    )
    influencer_id = db.Column(
        db.Integer, db.ForeignKey("influencers.influencer_id"), nullable=False
    )
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum("pending", "accepted", "rejected", "negotiation") , default = "pending")
    messages = db.Column(db.Text)

    negotiations = db.relationship("Negotiation", backref="ad_request", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Negotiation(db.Model):
    __tablename__ = "negotiations"

    negotiation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad_request_id = db.Column(
        db.Integer, db.ForeignKey("ad_requests.ad_request_id"), nullable=False
    )
    influencer_id = db.Column(
        db.Integer, db.ForeignKey("influencers.influencer_id"), nullable=False
    )
    proposed_payment_amount = db.Column(db.Numeric(10, 2))
    negotiation_status = db.Column(db.Enum("pending", "accepted", "rejected") ,default = "pending")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserFlag(db.Model):
    __tablename__ = "user_flags"

    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flagged_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CampaignFlag(db.Model):
    __tablename__ = "campaign_flags"

    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flagged_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    campaign_id = db.Column(
        db.Integer, db.ForeignKey("campaigns.campaign_id"), nullable=False
    )
    reason = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def init_db(app):
    with app.app_context():
        db.create_all()

        # Check if the database already contains data
        if not User.query.first():
            # Add dummy data
            admin = User(
                username="admin",
                password="password",
                email="admin@example.com",
                role="admin",
            )
            sponsor = User(
                username="sponsor",
                password="password",
                email="sponsor@example.com",
                role="sponsor",
            )
            influencer = User(
                username="influencer",
                password="password",
                email="influencer@example.com",
                role="influencer",
            )

            db.session.add(admin)
            db.session.add(sponsor)
            db.session.add(influencer)
            db.session.commit()

            sponsor_data = Sponsor(
                user_id=sponsor.user_id,
                company_name="Sponsor Company",
                industry="Technology",
                budget=10000.00,
            )
            influencer_data = Influencer(
                user_id=influencer.user_id,
                name="Influencer Name",
                category="Lifestyle",
                niche="Travel",
                reach=5000,
            )

            db.session.add(sponsor_data)
            db.session.add(influencer_data)
            db.session.commit()

            campaign = Campaign(
                sponsor_id=sponsor_data.sponsor_id,
                name="Campaign 1",
                description="Description of campaign 1",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31),
                budget=5000.00,
                visibility="public",
                goals="Increase brand awareness",
                niche="health",  # New field for niche
            )

            db.session.add(campaign)
            db.session.commit()

            ad_request = AdRequest(
                campaign_id=campaign.campaign_id,
                influencer_id=influencer_data.influencer_id,
                requirements="Requirements for the ad",
                payment_amount=1000.00,
                status="pending",
                messages="Initial message",
            )

            db.session.add(ad_request)
            db.session.commit()

            negotiation = Negotiation(
                ad_request_id=ad_request.ad_request_id,
                influencer_id=influencer_data.influencer_id,
                proposed_payment_amount=1200.00,
                negotiation_status="pending",
            )

            db.session.add(negotiation)
            db.session.commit()

            user_flag = UserFlag(
                flagged_by=admin.user_id,
                user_id=influencer.user_id,
                reason="Inappropriate behavior",
            )

            db.session.add(user_flag)
            db.session.commit()

            campaign_flag = CampaignFlag(
                flagged_by=admin.user_id,
                campaign_id=campaign.campaign_id,
                reason="Inappropriate content",
            )

            db.session.add(campaign_flag)
            db.session.commit()
