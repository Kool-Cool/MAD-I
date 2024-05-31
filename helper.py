# helper.py
# helper functions for database

from models import User

def get_data_by_name(username):
    admin = User.query.filter_by(username=username).first()
    if admin is not None:
        return admin.to_dict()
    else:
        return None

