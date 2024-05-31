#sponsor.py 
# Controller for sponsor login and registration....

from flask import Blueprint, request, render_template, redirect, url_for
from models import db , User,Sponsor ,Campaign ,AdRequest ,Influencer ,UserFlag , CampaignFlag
from flask import session , flash ,jsonify
import helper

sponsor = Blueprint('sponsor', __name__)

@sponsor.route("/login", methods=['GET', 'POST'])
def sponsor_login():
    return "sponsor Logged in !!"
