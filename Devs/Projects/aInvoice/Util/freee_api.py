#//+--------------------------------------------------------------------+
#//|                          VerysVeryInc.Py3.Django.aInvoice.Forms.py |
#//|                    Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                   https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                   Since:2018.03.05 |
#//|                                  Released under the Apache license |
#//|                         https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.aInv.Util.Freee_API.py - Ver.3.91.6 Update:2021.01.27" |
#//+--------------------------------------------------------------------+
# Freee_API
from requests_oauthlib import OAuth2Session
import requests
import json
import collections as cl
# import pandas as pd
# from pandas.io.json import json_normalize
import csv
from datetime import datetime


### Freee_API ###
## Wallet Txns ###
def Wallet_Txns(self):

    ### Def.API.Authorization.Code ###
    AUTH_CODE = '175a5f4b9994560e73f32cb19b451c99aed60e2c464b704ed028880d546d7b15'

    # 明細一覧.取得用API.URL
    with open("../plusfreee_config.json") as fc:
        fc_data = json.load(fc)
    WALLET_TXNS_URL = fc_data['wallet_txns_url']
    company_id = fc_data['company_id']

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
    ## REFRESH_TOKEN : False
    else:
        r_code, a_code = Get_A_Token("", AUTH_CODE)

    ## (GET) PlusFreee.Connect
    # Freee.Session.Setup
    FreeeOAuth = OAuth2Session()
    FreeeOAuth.headers['accept'] = 'application/json'

    # Freee.Session : Headers
    FreeeOAuth.headers['Authorization'] = 'Bearer ' + a_code
    FreeeOAuth.headers['X-Api-Version'] = '2020-06-15'

    # 明細一覧.取得.Params
    offset = 0

    params = {
        'company_id': company_id,
        'offset': offset,
        'limit': 100,
    }

    # Freee.Session : Wallet_Txns
    rw = FreeeOAuth.get(WALLET_TXNS_URL, params=params)

    # 正常受信 : 200
    if rw.status_code == 200:
        data_wallet_txns = json.loads(rw.text)

        # Json : 再構築
        wTxns_Json = {}
        wTxns_Data = []

        # wTxns_Json = cl.OrderedDict()

        Wallet_Txns_List = data_wallet_txns['wallet_txns']
        for w in Wallet_Txns_List:
            del w['company_id']
            del w['due_amount']
            print(Wallet_Txns_List)

            # CSV : 出力
            # wTxns_id = w['id']
            # wTxns_des = w['description']
            # wTxns_Json.update({'id': wTxns_id, 'description': wTxns_des})
            # print(wTxns_Json)

            wt_id = w['id']
            wt_date = datetime.strptime(w['date'], "%Y-%m-%d")
            wt_wl = w['walletable_id']
            wt_des = w['description']
            wt_en = w['entry_side']
            wt_am = w['amount']
            wt_bl = w['balance']
            wTxns_Data.append([wt_id, wt_date, wt_wl, wt_des, wt_en, wt_am, wt_bl])

            with open('PlusFreee_CSV/' + str(offset) + '.csv', 'w', newline='') as csvFile:
            # with open('20210127.csv', 'w', newline='') as csvFile:
                out_csv = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                # out_csv.writerow(['id'])
                for d in wTxns_Data:
                    out_csv.writerow(d)

            # with open('20210127.csv', 'w', newline='') as csvFile:
            #    csv_write = csv.DictWriter(csvFile, fi)


                # print(wTxns_Json)
                # csv_write = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                # csv_write.writerow(['id', 'description'])

                # for wt in wTxns_Json:
                #    csv_write.writerow(wt)



        # df_json = json_normalize(Wallet_Txns_List)
        # df_json.to_csv("2021.csv", encoding='utf-8')



        # df = pd.read_json(Wallet_Txns_List)
        # df.to_csv("PlusFreee_CSV/" + offset + ".csv")


        # Wallet_Txns_List = Wallet_Txns_List.pop('due_amount')
        # del Wallet_Txns_List['due_amount']
        # print(Wallet_Txns_List)

        # wTxns_Json = Wallet_Txns_List
        # for i in wTxns_Json:
        #    del i['id']

        # wTxns_Json = json.dumps(wTxns_Json)

        # for i in Wallet_Txns_List:
        #     wTxns_Json.update(['id']) = i['id']
        # print(wTxns_Json)





        # WT_List = list()
        # for i in Wallet_Txns_List:
        #     WT_List.append(i['id'])
        # wTxns = WT_List

        wTxns = Wallet_Txns_List
        # wTxns = wTxns_Json

    # 受信エラー : != 200
    else:
        ErrorCode = rw.status_code
        GET_Data = ErrorCode

        wTxns = str(GET_Data) + " - "

    # wTxns = company_id

    return a_code, r_code, company_id, wTxns


## Freee_Account ##
def Freee_Account(self):

    ### Def.API.Authorization.Code
    AUTH_CODE = '621d534b60c04e941486a56685cffa07811a2cf4ae83a668f5bb39cb38ad672e'
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

