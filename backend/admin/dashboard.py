from model.register_information import User
from model.image import Image
from server import db


def get_users_count():
    try:
        return User.query.count()
    except Exception, e:
        print e.str
        db.session.rollback()
        return 0
