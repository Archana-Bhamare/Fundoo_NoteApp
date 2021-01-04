import datetime

from FundooNote_Project.settings.dev import SECRET_KEY

import jwt


def token_activation(username, password=None):
    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now() + datetime.timedelta(days=1)
    }

    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return token
