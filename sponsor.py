#sponsor.py 
# Controller for sponsor login and registration....

from flask import Blueprint, request, render_template, redirect, url_for
from models import db , User,Sponsor ,Campaign ,AdRequest ,Influencer ,UserFlag , CampaignFlag
from flask import session , flash ,jsonify
import helper

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
            return redirect(url_for("sponsor.sponsor_dashboard"))
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
            return redirect(url_for('sponsor.sponsor_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('sponsor_login.html')


@sponsor.route('/dashboard')
def sponsor_dashboard():
    if 'user_name' in session and session['role'] == 'sponsor':
        return render_template('sponsor_dashboard.html' ,data = session)
    return redirect(url_for('sponsor.sponsor_login'))