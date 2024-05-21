# helper.py
# helper functions for database

from models import Admin

def get_admin_by_name(name):
    admin = Admin.query.filter_by(name=name).first()
    if admin is not None:
        return admin.to_dict()
    else:
        return None

