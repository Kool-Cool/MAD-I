# helper.py
# helper functions for database

from models import User

def get_data_by_name(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.to_dict()
    else:
        return None

