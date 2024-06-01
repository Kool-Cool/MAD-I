#sponsor.py 
# Controller for sponsor login and registration....

from flask import Blueprint, request, render_template, redirect, url_for
from models import db , User,Sponsor ,Campaign ,AdRequest ,Influencer ,UserFlag , CampaignFlag
from flask import session , flash ,jsonify
import helper
import datetime

sponsor = Blueprint('sponsor', __name__)


@sponsor.route('/registration', methods=['GET', 'POST'])
def sponsor_registration():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        company_name = request.form['company_name']
        industry = request.form['industry']
        budget = request.form['budget']


        new_user = User(username=username, password=password, email=email, role='sponsor')
        try:
            db.session.add(new_user)
            db.session.commit()

            
            new_sponsor = Sponsor(user_id=new_user.user_id, company_name=company_name, industry=industry, budget=budget)
            db.session.add(new_sponsor)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('sponsor.sponsor_login'))
        except Exception as e:
            error_message = str(e).split('\n')[0]  
            flash(f"Error: {error_message}", "error")
            db.session.rollback()  

    return render_template('sponsor_registration.html')




@sponsor.route('/login', methods=['GET', 'POST'])
def sponsor_login():

    if "user_name" in session and "role" in session:
        if session["role"] == "sponsor":
            return redirect(url_for("sponsor.sponsor_managecampaign"))
        else:
            return redirect(url_for("home"))


    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, role='sponsor').first()

        if user and user.password == password:
            session['user_name'] = user.username
            session['role'] = user.role
            session['user_id'] = user.user_id

            flash('Login successful!', 'success')
            return redirect(url_for('sponsor.sponsor_managecampaign'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('sponsor_login.html')


@sponsor.route('/managecampaign')
def sponsor_managecampaign():
    if 'user_name' in session and session['role'] == 'sponsor':

        campaign_data = helper.get_campaign_by_userid(session['user_id'])

        return render_template('sponsor_managecampaign.html' ,data = session, campaign_data=campaign_data)
    

    return redirect(url_for('sponsor.sponsor_login'))

@sponsor.route("/managecampaign/addcampaign" , methods=['GET', 'POST'])
def add_campaign():
    if 'user_name' in session and session['role'] == 'sponsor':

        if request.method == "POST":
            user_id = session['user_id']
            sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
            sponsor_id = sponsor_data.sponsor_id

            # print("user_id" , user_id)
            # print("sponsor_iddd ," , sponsor_id)

            new_campaign_data = {
                "budget": request.form.get("campaignbudget"),
                "description" : request.form.get("campaigndescription"),
                "end_date" : request.form.get("campaignenddate"),
                "goals" : request.form.get("campaigngoals"),
                "name" : request.form.get("campaignname"),
                "niche" : request.form.get("campaignniche"),
                "sponsor_id" : sponsor_id ,
                "start_date" : request.form.get("campaignstartdate"),
                "visibility" : request.form.get("campaignvisibility")
            }
            # print(new_campaign_data)

            # print()
            # print(new_campaign_data['visibility'])

            # print("old Type" , type(new_campaign_data['start_date']))

            new_campaign = Campaign(
                sponsor_id = new_campaign_data['sponsor_id'],
                name = new_campaign_data['name'],
                description = new_campaign_data['description'],
                # start_date': '2024-06-01' YYYY-MM-DD
                start_date = datetime.datetime.strptime(new_campaign_data['start_date'], '%Y-%m-%d').date() ,
                end_date = datetime.datetime.strptime(new_campaign_data['end_date'], '%Y-%m-%d').date(),
                budget = new_campaign_data['budget'],
                visibility = new_campaign_data['visibility'],
                goals = new_campaign_data['goals'],
                niche =new_campaign_data['niche']
            )

            # print(new_campaign_data)

            try:
                # print(new_campaign)
                db.session.add(new_campaign)  
                db.session.commit()
                flash("Added New Campaign Successfully" , "success")
                return redirect(url_for('sponsor.sponsor_managecampaign'))


            except Exception as e:
                error_message = str(e)#.split('\n')[0]  # Get the first line of the error
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

            
        return render_template('sponsor_addcampaign.html')
    return redirect(url_for('sponsor.sponsor_login'))




@sponsor.route("/managecampaign/editcampaign/<int:campaign_id>", methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    if 'user_name' in session and session['role'] == 'sponsor':
        # return f"this is for editing the campaign data of id {campaign_id}"
        campaign = Campaign.query.get(campaign_id)

        if not campaign:
            flash("Campaign not found.", "error")
            return redirect(url_for('sponsor.sponsor_managecampaign'))

        if request.method == "POST":
            # Update campaign data based on user input
            campaign.budget = request.form.get("campaignbudget")
            campaign.description = request.form.get("campaigndescription")
            campaign.end_date = datetime.datetime.strptime(request.form.get("campaignenddate"), '%Y-%m-%d').date()
            campaign.goals = request.form.get("campaigngoals")
            campaign.name = request.form.get("campaignname")
            campaign.niche = request.form.get("campaignniche")
            campaign.start_date = datetime.datetime.strptime(request.form.get("campaignstartdate"), '%Y-%m-%d').date()
            campaign.visibility = request.form.get("campaignvisibility")

            try:
                db.session.commit()
                flash("Campaign updated successfully.", "success")
                return redirect(url_for('sponsor.sponsor_managecampaign'))
            except Exception as e:
                error_message = str(e)
                flash(f"Error: {error_message}", "error")
                db.session.rollback()

        return render_template('sponsor_editcampaign.html', campaign=campaign)
    
    return redirect(url_for('sponsor.sponsor_login'))



