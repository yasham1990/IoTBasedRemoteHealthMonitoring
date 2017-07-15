from flask import request, redirect
import requests
import json
import configIhealth as ihealthfg



class iHealth():
    """ A basic class of iHealth API handler """

    def __init__(self, client_id, client_secret, redirect_uri):
        self.access_token = ''
        self.refresh_token = ''
        self.user_id = ''
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.response_type = 'code'
        self.APIName = 'OpenApiBP OpenApiUserInfo'
        self.RequiredAPIName = 'OpenApiBP OpenApiUserInfo'
        self.IsNew = 'true'
        self.auth_url = ihealthfg.AUTH_URL
        self.user_url = ihealthfg.USER_DATA_URL
        self.app_url = ihealthfg.ALL_DATA_URL

    def checkCredentials(self):
        bodyData = {'client_id': self.client_id, 'response_type': self.response_type,
                   'redirect_uri': self.redirect_uri, 'APIName': self.APIName,
                   'RequiredAPIName': self.RequiredAPIName, 'IsNew': self.IsNew}
        result = requests.get(self.auth_url, params=bodyData)
        return result

    def ihealth_auth_callback(self):
        code = self.getCode()
        grant_type = 'authorization_code'   # is currently the only supported value
        payload = {'code': code, 'client_id': self.client_id, 'grant_type': grant_type,
                   'client_secret': self.client_secret, 'redirect_uri': self.redirect_uri}
        r = requests.get(self.auth_url, params=payload)
        self.access_token, self.refresh_token = self.getTokens(r.text)
        self.user_id = self.getUserId(r.text)
        return r.text

    def getUserId(self, data):
        resp = json.loads(data)
        if resp['UserID']:
            return resp['UserID']
        else:
            return None

    def getBp(self,dateStart):
        if dateStart is not '':
            base_url = self.user_url+str(self.user_id)+'/bp/?START_TIME='+dateStart
        else:
            base_url = self.user_url+str(self.user_id)+'/bp/'
        bp = ihealthfg.DATA_TYPES['OpenApiBP']
        bodyData = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': bp['sc'], 'sv': bp['sv']}
        result = requests.get(base_url, params=bodyData)
        return result.text
        
    def getCode(self):
        if 'code' not in request.args:
            return None
        return request.args['code']

    def getTokens(self, data):
        resp = json.loads(data)
        if resp['AccessToken'] and resp['RefreshToken']:
            return resp['AccessToken'], resp['RefreshToken']
        else:
            return None, None

