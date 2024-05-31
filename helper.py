# helper.py
# helper functions for database

from models import User

def get_admin_by_name(name):
    admin = User.query.filter_by(name=name).first()
    if admin is not None:
        return admin.to_dict()
    else:
        return None

