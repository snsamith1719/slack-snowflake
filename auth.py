import os

def is_authorized(user_id):

    allowed = os.getenv("AUTHORIZED_USERS")

    return user_id in allowed.split(",")