from flask import Blueprint , session , redirect , url_for ,request , render_template ,flash
from models import db , User ,Influencer


influencer = Blueprint('influencer', __name__)





@influencer.route("/registration" , methods=["GET", "POST"])
def registration():

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


@influencer.route("/dashboard")
def dashboard():
    return render_template("influencer_dashboard.html")
