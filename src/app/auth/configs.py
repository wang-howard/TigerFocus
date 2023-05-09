"""
Configuration values for ActiveDirectory API access.
Taken from: https://github.com/vr2amesh/COS333-API-Code-Examples/blob/master/ActiveDirectory/python/configs.py
"""

import requests
import json
import base64

class Configs:
    def __init__(self):
        self.CONSUMER_KEY = "H1xxzu_UETT85NmJ0CV7Wfnrpk8a"
        self.CONSUMER_SECRET = "hWXtSgMxC3Z3MSkpNQERswTwX4Ma"
        self.BASE_URL="https://api.princeton.edu:443/active-directory/1.0.5"
        self.USERS = "/users"
        self.USERS_BASIC = "/users/basic"
        self.USERS_FULL = "/users/full"
        self.REFRESH_TOKEN_URL="https://api.princeton.edu:443/token"
        self._refreshToken(grant_type="client_credentials")

    def _refreshToken(self, **kwargs):
        req = requests.post(
            self.REFRESH_TOKEN_URL, 
            data=kwargs, 
            headers={
                "Authorization": "Basic " + base64.b64encode(bytes(self.CONSUMER_KEY + ":" + self.CONSUMER_SECRET, "utf-8")).decode("utf-8")
            },
        )
        text = req.text
        response = json.loads(text)
        self.ACCESS_TOKEN = response["access_token"]