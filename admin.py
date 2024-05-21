#admin.py 
# Controller for admin login and registration

from flask import Blueprint, request, render_template, redirect, url_for
from models import db, Admin
from flask import session , flash
import helper

admin = Blueprint('admin', __name__)

@admin.route("/registration")
def admin_registration():
    return render_template("admin_registration.html")


@admin.route("/login", methods=['GET', 'POST'])
def admin_login():

    if request.method == "POST":
        admin_name =  request.form.get('name')
        admin_pass = request.form.get('password')
        print("___________________")
        print(admin_pass ,admin_name )

        if admin_name in session:
            return redirect(url_for("admin.admin_dashboard"))
        
        admin_data = helper.get_admin_by_name(admin_name)
        if admin_data :
            if admin_name == admin_data["name"] and admin_pass==admin_data["password"]:
                session["user_name"] = admin_name # We are using UserName (so that no two User (admin/contractor/influncer) login at same)
                return redirect(url_for("admin.admin_dashboard"))
            else:
                flash("Please enter Correct Information !!")

        else:
            flash("Please enter Correct Information !!")

    return render_template("admin_login.html")


@admin.route("/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")



