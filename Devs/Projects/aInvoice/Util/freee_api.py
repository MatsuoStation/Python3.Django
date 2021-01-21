#//+--------------------------------------------------------------------+
#//|                          VerysVeryInc.Py3.Django.aInvoice.Forms.py |
#//|                    Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                   https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                   Since:2018.03.05 |
#//|                                  Released under the Apache license |
#//|                         https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.aInv.Util.Freee_API.py - Ver.3.91.3 Update:2021.01.21" |
#//+--------------------------------------------------------------------+
# Freee_API
from requests_oauthlib import OAuth2Session
import requests
import json


### Freee_API ###
def Freee_Account(self):

    ### Def.API.Authorization.Code
    AUTH_CODE = 'f0e1b5ace7ecc8d60f720aac89de95c7a7bde2a9b6fd86a992ed95f21c6438b7'
    JS_TOKEN = '4f5fe0f08401d42493eca89a00d8b2809efef8147226102af82b4f8e571521c4'

    ### (GET) PlusFreee_Config.Json
    with open("../plusfreee_config.json") as fc:
        fc_data = json.load(fc)

    # 事務所一覧.取得用API.URL
    COMPANY_API_URL = fc_data['company_api_url']

    ### (GET) PlusFreee_Token.Json
    with open("../plusfreee_token.json") as ft:
        ft_data = json.load(ft)

    REFRESH_TOKEN = ft_data['refresh_token']
    ACCESS_TOKEN = ft_data['access_token']

    ## (GET) PlusFreee.Connect
    # Freee.Session.Setup
    FreeeOAuth = OAuth2Session()
    FreeeOAuth.headers['accept'] = 'application/json'

    ## REFRESH_TOKEN : True
    if REFRESH_TOKEN:
        r_code, a_code = Get_A_Token(REFRESH_TOKEN, ACCESS_TOKEN)
        # COMPANY_ID = 'True'

        # Freee.Session : Headers
        FreeeOAuth.headers['Authorization'] = 'Bearer ' + a_code
        # FreeeOAuth.headers['Authorization'] = 'Bearer ' + JS_TOKEN
        FreeeOAuth.headers['X-Api-Version'] = '2020-06-15'

        # Freee.Session : Company_ID
        rc = FreeeOAuth.get(COMPANY_API_URL)

        # 正常受信 : 200
        if rc.status_code == 200:
            data_company = json.loads(rc.text)

            COMPANY_ID = data_company['companies'][0]['id']

        # 受信エラー : != 200
        else:
            ErrorCode = rc.status_code
            GET_Data = ErrorCode

            COMPANY_ID = str(GET_Data) + " - "

    ## REFRESH_TOKEN : False
    else:
        r_code, a_code = Get_A_Token("", AUTH_CODE)
        COMPANY_ID = "None"

    return a_code, r_code, COMPANY_ID


### Get_A_Token ###
def Get_A_Token(r_code, a_code):

    ## JSON.Load : plusfreee_config.json
    with open("../plusfreee_config.json", encoding='utf-8') as fc:
        fc_data = json.load(fc)

    ## PlusFreee : Setup
    CLIENT_ID = fc_data['client_id']
    CLIENT_SECRET = fc_data['client_secret']
    REDIRECT_URI = fc_data['redirect_uri']
    # CLIENT_ID = 123456

    ## Freee.API.URL
    # 認証トークン.取得用API.URL
    AUTHORIZE_API_URL = fc_data['authorize_api_url']

    ## (GET) Access.Token
    # Freee.OAuth.SetUp
    FreeeOAuth = OAuth2Session()
    FreeeOAuth.headers['cache-control'] = 'no-cache'
    FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    ## REFRESH_TOKEN : True
    if r_code:
        # Freee.OAuth.SetUp
        # FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        ## Refresh.Token : Params
        params = {
            'grant_type'    : 'refresh_token',
            'client_id'     : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
            'refresh_token' : r_code,
            'redirect_uri'  : REDIRECT_URI
        }

        ## FreeeAPI.OAuth2.POST
        r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

        # 正常受信 : 200
        if r.status_code == 200:
            data = json.loads(r.text)

            ACCESS_TOKEN = data['access_token']
            REFRESH_TOKEN = data['refresh_token']

            # (READ) PlusFreee_Token.Json
            R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

            ### Refresh.Token.Write ###
            fw = open('../plusfreee_token.json', 'w')
            fw.write(R_Text)
            fw.close()

        # 受信エラー : != 200
        else:
            ACCESS_TOKEN = 'None'
            REFRESH_TOKEN = 'None'

    ### REFRESH_TOKEN.False
    else:
        # 1st.Access.Params
        # Freee.OAuth.SetUp
        # FreeeOAuth.headers['Content-Type'] = 'application/json'

        ## Access.Token : Params
        params = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': a_code,
            'redirect_uri': REDIRECT_URI
        }

        ## FreeeAPI.OAuth2.POST
        r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

        # 正常受信 : 200
        if r.status_code == 200:
            data = json.loads(r.text)

            ACCESS_TOKEN = data['access_token']
            REFRESH_TOKEN = data['refresh_token']

            # (READ) FreeeToken.Json
            R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

            ### Refresh.Token.Write ###
            fw = open('../plusfreee_token.json', 'w')
            fw.write(R_Text)
            fw.close()

        # 受信エラー : != 200
        else:
            ACCESS_TOKEN = 'None'
            REFRESH_TOKEN = 'None'

    # a_code = AUTHORIZE_API_URL
    # r_code = 2

    return REFRESH_TOKEN, ACCESS_TOKEN

