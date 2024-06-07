from flask import Blueprint , session , redirect , url_for ,request , render_template ,flash
from models import db , User ,Influencer, Campaign ,Negotiation
import helper


influencer = Blueprint('influencer', __name__)





@influencer.route("/registration" , methods=["GET", "POST"])
def registration():
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            return redirect(url_for("influencer.login"))

    if request.method == "POST":
                
        #  Adding as a User !
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        name = request.form['influencer_name']
        category = request.form['category']
        niche = request.form['niche']
        reach = request.form['reach']

        new_user = User(username = username , password = password , email=email , role='influencer')

        try:
            db.session.add(new_user)
            db.session.commit()

            new_influ = Influencer(
                user_id = new_user.user_id,
                category = category,
                name = name,
                niche = niche,
                reach = reach
            )

            db.session.add(new_influ)
            db.session.commit()

            flash("New Influencer Registered Successfully !! Login Please :) , success")
            return redirect(url_for("influencer.login"))
        except Exception as e:
            error_message = str(e).split("\n")[0]
            flash(f"Error: {error_message}", "error")
            db.session.rollback()

    return render_template("influencer_registration.html")







@influencer.route("/login", methods=['GET', 'POST'])
def login():
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            return redirect(url_for("influencer.dashboard"))
        else:
            return redirect(url_for("home"))
        
    if request.method == "POST":
        username = request.form['name']
        password = request.form["password"]

        user = User.query.filter_by(username = username , role ="influencer").first()

        if user and user.password == password :
            session["user_name"] = user.username
            session["role"] = user.role
            session["user_id"] = user.user_id

            flash("Login successful!", "success")
            return redirect(url_for("influencer.dashboard")) # Redirect to dashboard !
        else:
            flash("Invalid User name or password", "danger")
    
    return render_template("influrencer_login.html")


@influencer.route("/dashboard",methods=['GET', 'POST'])
def dashboard():
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            user_id = session["user_id"]
            # print(user_id)
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            # print("This is the influencer ID:", influencer_id)

            data = helper.get_influencer_campaigns(influencer_id)
            # print(data)
            return render_template("influencer_dashboard.html" , data = data)
    

    
    flash("Please Login !","faliled")
    return redirect(url_for("influencer.login"))


@influencer.route("/campaigns",methods=['GET', 'POST'])
def show_campaign():
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":

            public_campaing = Campaign.query.filter_by(visibility = "public").all()
            data = []
            for c in public_campaing:
                data.append(c.to_dict())
            return render_template("influencer_campaign.html" , data=data)
    
    
    flash("Please Login !","faliled")
    return redirect(url_for("influencer.login"))




@influencer.route("/accept_adrequest/<int:adrequest_id>")
def accept_adrequest(adrequest_id):
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            show_info = []
            # check if any negotiationa is there ,if there delete !

            nego = Negotiation.query.filter_by(ad_request_id = adrequest_id )

            if nego:
                pass
            
            # change ad_request status to accepted !

            return render_template("influencer_accept.html")
        
    
    flash("Please Login !","faliled")
    return redirect(url_for("influencer.login"))
    