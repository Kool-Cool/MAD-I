#admin.py 
# Controller for admin login and registration

from flask import Blueprint, request, render_template, redirect, url_for
from models import db , User,Sponsor ,Campaign ,AdRequest ,Influencer ,Flag
from flask import session , flash ,jsonify
import helper

admin = Blueprint('admin', __name__)

@admin.route("/registration" ,methods=['GET', 'POST'])
def admin_registration():
    
    if request.method == "POST":
        new_username = request.form.get("username") 
        new_password = request.form.get("password")
        new_email = request.form.get("email") 
        new_role = request.form.get("role")

        add_admin = User(username=new_username, password=new_password, email=new_email, role=new_role)
        
        try:
            db.session.add(add_admin)  
            db.session.commit()
            flash("Registered New Admin Successfully", "success")
            return redirect(url_for('admin.admin_login'))
        except Exception as e:
            error_message = str(e).split('\n')[0]  # Get the first line of the error
            flash(f"Error: {error_message}", "error")
            db.session.rollback()  
        
    return render_template("admin_registration.html")


@admin.route("/login", methods=['GET', 'POST'])
def admin_login():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            # and this user_name of admin
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return redirect(url_for("app.home"))


    if request.method == "POST":
        admin_name =  request.form.get('name')
        admin_pass = request.form.get('password')

        admin_data = helper.get_data_by_name(admin_name)
        # print(admin_data)
        if admin_data :
            if admin_name == admin_data["username"] and admin_pass==admin_data["password"] and admin_data["role"]=='admin':
                session["user_name"] = admin_name # We are using UserName (so that no two User (admin/contractor/influncer) login at same)
                session["role"]="admin"
                session["user_id"] = admin_data["user_id"]
                return redirect(url_for("admin.admin_dashboard"))
            else:
                flash("Please enter Correct Information !!")
        else:
            flash("Please enter Correct Information !!")

    return render_template("admin_login.html")


@admin.route("/dashboard")
def admin_dashboard():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":

            return render_template("admin_dashboard.html" , info_data=session)
    return redirect(url_for("app.home"))

@admin.route('/dashboard/data', methods=['GET'])
def admin_dashboard_data():
    total_users = User.query.count()
    total_sponsors = Sponsor.query.count()
    total_campaigns_public = Campaign.query.filter_by(visibility='public').count()
    total_campaigns_private = Campaign.query.filter_by(visibility='private').count()
    total_ad_requests_pending = AdRequest.query.filter_by(status='pending').count()
    total_ad_requests_rejected = AdRequest.query.filter_by(status='rejected').count()
    total_ad_requests_negotiation = AdRequest.query.filter_by(status='negotiation').count()
    total_ad_requests_accepted = AdRequest.query.filter_by(status='accepted').count()
    total_influencers = Influencer.query.count()
    flagged_items = Flag.query.count()
    
    data = {
        'total_users': total_users,
        'total_sponsors': total_sponsors,
        'total_campaigns_public': total_campaigns_public,
        'total_campaigns_private': total_campaigns_private,
        'total_ad_requests_pending': total_ad_requests_pending,
        'total_ad_requests_rejected': total_ad_requests_rejected,
        'total_ad_requests_negotiation': total_ad_requests_negotiation,
        'total_ad_requests_accepted': total_ad_requests_accepted,
        'total_influencers': total_influencers,
        'flagged_items': flagged_items
    }
    
    return jsonify(data)




@admin.route('/allusers')
def all_users():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":

            data = dict()
            
            data["admin"] = [user.to_dict() for user in User.query.filter_by(role="admin").all()]
            data["sponsor"] = [user.to_dict() for user in User.query.filter_by(role="sponsor").all()]
            data["influencer"] = [user.to_dict() for user in User.query.filter_by(role="influencer").all()]

            return render_template("admin_allusers.html", data=data)
    return redirect(url_for("home"))



@admin.route('/allsponsors')
def all_sponsors():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            sponsors = Sponsor.query.all()
            return render_template("admin_allsponsors.html", sponsors=sponsors)
    return redirect(url_for("home"))



@admin.route('/allinfluencers')
def all_influencers():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            influencers = Influencer.query.all()
            return render_template("admin_allinfluencers.html", influencers=influencers)
    return redirect(url_for("home"))



@admin.route('/allflags')
def all_flags():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            flags = Flag.query.all()
            return render_template("admin_allflags.html", flags=flags)
    return redirect(url_for("home"))



@admin.route('/allcampaigns')
def all_campaigns():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            campaigns = Campaign.query.all()
            return render_template("admin_allcampaigns.html", campaigns=campaigns)
    return redirect(url_for("home"))

@admin.route('/alladrequests')
def all_adrequests():
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            ad_requests = AdRequest.query.all()
            return render_template("admin_alladrequests.html", ad_requests=ad_requests)
    return redirect(url_for("home"))


@admin.route('/flag/user/<int:user_id>', methods=['POST'])
def flag_user(user_id):
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            data = request.get_json()
            reason = data.get('reason')
            flag = Flag(flagged_by=session["user_id"], user_id=user_id, reason=reason)
            db.session.add(flag)
            db.session.commit()
            return jsonify({"message": "User flagged successfully!"}), 200
    return jsonify({"message": "Unauthorized"}), 403

@admin.route('/flag/campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign(campaign_id):
    if "user_name" in session and "role" in session:
        if session["role"] == "admin":
            data = request.get_json()
            reason = data.get('reason')
            flag = Flag(flagged_by=session["user_id"], campaign_id=campaign_id, reason=reason)
            db.session.add(flag)
            db.session.commit()
            return jsonify({"message": "Campaign flagged successfully!"}), 200
    return jsonify({"message": "Unauthorized"}), 403



