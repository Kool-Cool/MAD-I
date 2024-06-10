# sponsor.py
# Controller for sponsor login and registration....

from flask import Blueprint, request, render_template, redirect, url_for
from models import (
    db,
    User,
    Sponsor,
    Campaign,
    AdRequest,
    Influencer,
)
from flask import session, flash, jsonify
import helper
import datetime

sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/registration", methods=["GET", "POST"])
def sponsor_registration():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        company_name = request.form["company_name"]
        industry = request.form["industry"]
        budget = request.form["budget"]

        new_user = User(
            username=username, password=password, email=email, role="sponsor"
        )
        try:
            db.session.add(new_user)
            db.session.commit()

            new_sponsor = Sponsor(
                user_id=new_user.user_id,
                company_name=company_name,
                industry=industry,
                budget=budget,
            )
            db.session.add(new_sponsor)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("sponsor.sponsor_login"))
        except Exception as e:
            error_message = str(e).split("\n")[0]
            flash(f"Error: {error_message}", "error")
            db.session.rollback()

    return render_template("sponsor_registration.html")


@sponsor.route("/login", methods=["GET", "POST"])
def sponsor_login():

    if "user_name" in session and "role" in session:
        if session["role"] == "sponsor":
            return redirect(url_for("sponsor.sponsor_managecampaign"))
        else:
            return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, role="sponsor").first()

        if user and user.password == password:
            session["user_name"] = user.username
            session["role"] = user.role
            session["user_id"] = user.user_id

            flash("Login successful!", "success")
            return redirect(url_for("sponsor.sponsor_managecampaign"))
        else:
            flash("Invalid User name or password", "danger")

    return render_template("sponsor_login.html")


@sponsor.route("/search_influencer", methods=["GET", "POST"])
def search_influencer():
    influencer_data = Influencer.query.all()
    # print(influencer_data)
    data = []
    for d in influencer_data:
        data.append(d.to_dict())
    # print(data)

    return render_template("sponsor_search_influ.html", data=data)


@sponsor.route("/managecampaign")
def sponsor_managecampaign():
    if "user_name" in session and session["role"] == "sponsor":

        campaign_data = helper.get_campaign_by_userid(session["user_id"])

        return render_template(
            "sponsor_managecampaign.html", data=session, campaign_data=campaign_data
        )

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route("/managecampaign/addcampaign", methods=["GET", "POST"])
def add_campaign():
    if "user_name" in session and session["role"] == "sponsor":

        if request.method == "POST":
            user_id = session["user_id"]
            sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
            sponsor_id = sponsor_data.sponsor_id

            # print("user_id" , user_id)
            # print("sponsor_iddd ," , sponsor_id)

            new_campaign_data = {
                "budget": request.form.get("campaignbudget"),
                "description": request.form.get("campaigndescription"),
                "end_date": request.form.get("campaignenddate"),
                "goals": request.form.get("campaigngoals"),
                "name": request.form.get("campaignname"),
                "niche": request.form.get("campaignniche"),
                "sponsor_id": sponsor_id,
                "start_date": request.form.get("campaignstartdate"),
                "visibility": request.form.get("campaignvisibility"),
            }
            # print(new_campaign_data)

            # print()
            # print(new_campaign_data['visibility'])

            # print("old Type" , type(new_campaign_data['start_date']))

            new_campaign = Campaign(
                sponsor_id=new_campaign_data["sponsor_id"],
                name=new_campaign_data["name"],
                description=new_campaign_data["description"],
                # start_date': '2024-06-01' YYYY-MM-DD
                start_date=datetime.datetime.strptime(
                    new_campaign_data["start_date"], "%Y-%m-%d"
                ).date(),
                end_date=datetime.datetime.strptime(
                    new_campaign_data["end_date"], "%Y-%m-%d"
                ).date(),
                budget=new_campaign_data["budget"],
                visibility=new_campaign_data["visibility"],
                goals=new_campaign_data["goals"],
                niche=new_campaign_data["niche"],
            )

            # print(new_campaign_data)

            try:
                # print(new_campaign)
                db.session.add(new_campaign)
                db.session.commit()
                flash("Added New Campaign Successfully", "success")
                return redirect(url_for("sponsor.sponsor_managecampaign"))

            except Exception as e:
                error_message = str(e).split("\n")[0]  # Get the first line of the error
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_addcampaign.html")
    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route(
    "/managecampaign/editcampaign/<int:campaign_id>", methods=["GET", "POST"]
)
def edit_campaign(campaign_id):
    if "user_name" in session and session["role"] == "sponsor":
        # return f"this is for editing the campaign data of id {campaign_id}"
        campaign = Campaign.query.get(campaign_id)

        if not campaign:
            flash("Campaign not found.", "error")
            return redirect(url_for("sponsor.sponsor_managecampaign"))

        if request.method == "POST":
            # Update campaign data based on user input
            campaign.budget = request.form.get("campaignbudget")
            campaign.description = request.form.get("campaigndescription")
            campaign.end_date = datetime.datetime.strptime(
                request.form.get("campaignenddate"), "%Y-%m-%d"
            ).date()
            campaign.goals = request.form.get("campaigngoals")
            campaign.name = request.form.get("campaignname")
            campaign.niche = request.form.get("campaignniche")
            campaign.start_date = datetime.datetime.strptime(
                request.form.get("campaignstartdate"), "%Y-%m-%d"
            ).date()
            campaign.visibility = request.form.get("campaignvisibility")

            try:
                db.session.commit()
                flash("Campaign updated successfully.", "success")
                return redirect(url_for("sponsor.sponsor_managecampaign"))
            except Exception as e:
                error_message = str(e).split("\n")[0]
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_editcampaign.html", campaign=campaign)

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route(
    "/managecampaign/deletecampaign/<int:campaign_id>", methods=["GET", "POST"]
)
def delete_campaign(campaign_id):
    if "user_name" in session and session["role"] == "sponsor":
        # return f"this is for Deleting the campaign data of id {campaign_id}"

        # Retrieve the campaign by its ID
        campaign = Campaign.query.get(campaign_id)

        if not campaign:
            flash("Campaign not found.", "error")
            return redirect(url_for("sponsor.sponsor_managecampaign"))

        if request.method == "POST":
            try:
                # Delete the campaign from the database
                db.session.delete(campaign)
                db.session.commit()
                flash("Campaign deleted successfully.", "success")
                return redirect(url_for("sponsor.sponsor_managecampaign"))
            except Exception as e:
                error_message = str(e)
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_deletecampaign.html", campaign=campaign)

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route("/manageadrequest")
def sponsor_manageadrequest():
    if "user_name" in session and session["role"] == "sponsor":
        adrequest_data = helper.get_adrequest_by_userid(session["user_id"])
        # print(adrequest_data)

        return render_template(
            "sponsor_manage_adrequests.html", adrequest_data=adrequest_data
        )

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route("/manageadrequest/add_adrequest", methods=["GET", "POST"])
def add_adrequest():
    if "user_name" in session and session["role"] == "sponsor":

        if request.method == "POST":
            campaign_exists = Campaign.query.filter_by(
                campaign_id=request.form.get("campaignid")
            ).first()
            influencer_exists = Influencer.query.filter_by(
                influencer_id=request.form.get("influencerid")
            ).first()
            # print(campaign_exists)
            # print()
            # print(influencer_exists)
            if not campaign_exists:
                flash("Error: Campaign ID does not exist.", "error")
                return redirect(url_for("sponsor.add_adrequest"))

            if not influencer_exists:
                flash("Error: Influencer ID does not exist.", "error")
                return redirect(url_for("sponsor.add_adrequest"))

            new_reqst = AdRequest(
                campaign_id=request.form.get("campaignid"),
                influencer_id=request.form.get("influencerid"),
                messages=request.form.get("messages"),
                payment_amount=request.form.get("payment_amount"),
                requirements=request.form.get("requirements"),
                status=request.form.get("status"),
            )

            try:
                db.session.add(new_reqst)
                db.session.commit()
                flash("Added New Ad Request Successfully", "success")
                return redirect(url_for("sponsor.sponsor_manageadrequest"))
            except Exception as e:
                error_message = str(e).split("\n")[0]
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_add_adrequest.html")

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route(
    "/manageadrequest/edit_adrequest/<int:adrequest_id>", methods=["GET", "POST"]
)
def edit_adrequest(adrequest_id):
    if "user_name" in session and session["role"] == "sponsor":
        ad_data = AdRequest.query.get(adrequest_id)

        if not ad_data:
            flash("Ad Request not found.", "error")
            return redirect(url_for("sponsor.sponsor_manageadrequest"))

        if request.method == "POST":
            campaign_exists = Campaign.query.filter_by(
                campaign_id=request.form.get("campaignid")
            ).first()
            influencer_exists = Influencer.query.filter_by(
                influencer_id=request.form.get("influencerid")
            ).first()
            # print(campaign_exists)
            # print()
            # print(influencer_exists)
            if not campaign_exists:
                flash("Error: Campaign ID does not exist.", "error")
                return redirect(
                    url_for(
                        "sponsor.edit_adrequest", adrequest_id=ad_data["ad_request_id"]
                    )
                )

            if not influencer_exists:
                flash("Error: Influencer ID does not exist.", "error")
                return redirect(
                    url_for(
                        "sponsor.edit_adrequest", adrequest_id=ad_data["ad_request_id"]
                    )
                )

            ad_data.campaign_id = request.form.get("campaignid")
            ad_data.influencer_id = request.form.get("influencerid")
            ad_data.messages = request.form.get("messages")
            ad_data.payment_amount = request.form.get("payment_amount")
            ad_data.requirements = request.form.get("requirements")
            ad_data.status = request.form.get("status")

            try:
                db.session.commit()
                flash("Ad Request updated successfully.", "success")
                return redirect(url_for("sponsor.sponsor_manageadrequest"))
            except Exception as e:
                error_message = str(e).split("\n")[0]
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_edit_adrequest.html", ad_data=ad_data)

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))


@sponsor.route(
    "/manageadrequest/delete_adrequest/<int:adrequest_id>", methods=["GET", "POST"]
)
def deleted_adrequest(adrequest_id):
    if "user_name" in session and session["role"] == "sponsor":
        ad_data = AdRequest.query.get(adrequest_id)

        if not ad_data:
            flash("Ad Request Not Found !", "error")
            return redirect(url_for("sponsor.sponsor_manageadrequest"))

        if request.method == "POST":
            try:
                db.session.delete(ad_data)
                db.session.commit()
                flash("Add reuquest Deleted ! Successfully", "success")
                return redirect(url_for("sponsor.sponsor_manageadrequest"))
            except Exception as e:
                error_message = str(e)
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template("sponsor_delete_adrequest.html", ad_data=ad_data)

    flash("Please Login !", "faliled")
    return redirect(url_for("sponsor.sponsor_login"))
