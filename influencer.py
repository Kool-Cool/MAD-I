from flask import Blueprint , session , redirect , url_for ,request

influencer = Blueprint('influencer', __name__)




@influencer.route("/login", methods=['GET', 'POST'])
def login():
    return "THIS IS LOGIN PAGE for Influencer !!"
