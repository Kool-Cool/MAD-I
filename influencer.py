from flask import Blueprint , session , redirect , url_for ,request , render_template ,flash
from models import db , User ,Influencer, Campaign ,Negotiation , AdRequest
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




@influencer.route("/accept_adrequest/<int:adrequest_id>" ,methods=['GET', 'POST'])
def accept_adrequest(adrequest_id):
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            user_id = session["user_id"]
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            data = helper.get_influencer_campaigns(influencer_id)
            
            show_info = None
            for d in data:
                # print(d)
                if d['ad_request_id'] == adrequest_id:
                    show_info = d
                    break
            
            
            
            
            if show_info is not None:
                if request.method == "POST":
                    # check if any negotiationa is there ,if there delete !
                    if show_info['negotiation_id']:
                        nego = Negotiation.query.filter_by(negotiation_id = show_info['negotiation_id'] ).first()
                        nego.negotiation_status = "accepted"
                        nego.proposed_payment_amount = show_info['payment_amount']

                        try:
                            db.session.commit()
                        
                        except Exception as e:
                            error_message = str(e).split("\n")[0]
                            flash(f"Error: {error_message}", "error")
                            db.session.rollback()
                    else:
                        new_nego = Negotiation(
                            ad_request_id = show_info['ad_request_id'] ,
                            influencer_id = show_info['influencer_id'],
                            negotiation_status = "accepted" ,
                            proposed_payment_amount = show_info['payment_amount'],
                        )

                        try:
                            db.session.add(new_nego)
                            db.session.commit()
                        except Exception as e:
                            error_message = str(e).split("\n")[0]
                            flash(f"Error: {error_message}", "error")
                            db.session.rollback()


                    
                    # change ad_request status to accepted !
                    ad_reqst = AdRequest.query.filter_by(ad_request_id =show_info['ad_request_id']).first_or_404()
                    ad_reqst.status = "accepted"
                    try:
                        db.session.commit()
                        
                    except Exception as e:
                        error_message = str(e).split("\n")[0]
                        flash(f"Error: {error_message}", "error")
                        db.session.rollback()

                    flash("Accepted the Ad_request","success")
                    return redirect(url_for("influencer.login"))
                    

                return render_template("influencer_accept.html" ,show_info = show_info)
            
            flash("Wrong ad_request_id !!","faliled")
            return redirect(url_for("influencer.login"))
        
    
    flash("Please Login !","faliled")
    return redirect(url_for("influencer.login"))
    




@influencer.route("/nego_adrequest/<int:adrequest_id>" ,methods=['GET', 'POST'])
def nego_adrequest(adrequest_id):
    if "user_name" in session and "role" in session:
        if session["role"] == "influencer":
            user_id = session["user_id"]
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            data = helper.get_influencer_campaigns(influencer_id)
            
            show_info = None
            for d in data:
                # print(d)
                if d['ad_request_id'] == adrequest_id:
                    show_info = d
                    break


            # Check if Already Accepted !!

            if show_info['negotiation_status'] == "accepted" and show_info['status'] == "accepted" :
                flash("You have Already Accepted the offer !! ","failure")
                return redirect(url_for("influencer.login"))

            # Check if Already Rejected !!
            if show_info['negotiation_status'] == "rejected":
                flash("You have Already Rejected the offer !! ","failure")
                return redirect(url_for("influencer.login"))
            

            if request.method == "POST":

                new_nego_amount = request.form.get("nego_amount")
                # print(new_nego_amount)

                #Change Ad_request status
                old_ad_requt = AdRequest.query.filter_by(ad_request_id =  show_info['ad_request_id']).first_or_404()
                old_ad_requt.status = "negotiation"

                try:
                    db.session.commit()
                        
                except Exception as e:
                    error_message = str(e).split("\n")[0]
                    flash(f"Error: {error_message}", "error")
                    db.session.rollback()

                #Change Nego_amount and status
                if show_info["negotiation_id"] is not None:
                    old_nego = Negotiation.query.filter_by(negotiation_id = show_info['negotiation_id']).first_or_404()
                    # print(old_nego.to_dict())
                    old_nego.proposed_payment_amount = new_nego_amount
                    try:
                        db.session.commit()
                        
                    except Exception as e:
                        error_message = str(e).split("\n")[0]
                        flash(f"Error: {error_message}", "error")
                        db.session.rollback()



                else:
                    add_new_nego = Negotiation(
                        ad_request_id = show_info['ad_request_id'],
                        influencer_id = show_info['influencer_id'],
                        negotiation_status = "pending",
                        proposed_payment_amount = new_nego_amount
                    )
                    try:
                        db.session.add(add_new_nego)
                        db.session.commit()
                    except Exception as e:
                        error_message = str(e).split("\n")[0]
                        flash(f"Error: {error_message}", "error")
                        db.session.rollback()

                flash(f"UPDATED THE Negotiation ({new_nego_amount}) ")
                return  redirect(url_for("influencer.login"))

            return render_template("influencer_nego.html", show_info = show_info)
    
    
    flash("Please Login !","faliled")
    return redirect(url_for("influencer.login"))