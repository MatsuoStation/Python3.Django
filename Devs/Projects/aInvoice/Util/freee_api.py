#//+--------------------------------------------------------------------+
#//|                          VerysVeryInc.Py3.Django.aInvoice.Forms.py |
#//|                    Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                   https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                   Since:2018.03.05 |
#//|                                  Released under the Apache license |
#//|                         https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.aInv.Util.Freee_API.py - Ver.3.91.9 Update:2021.02.08" |
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
import mysql.connector as mConn

from ..AWS import mysql as rdsSession


### AWS.MySQL.Session : Setup ###
ENDPOINT = rdsSession.ENDPOINT
USER = rdsSession.USR
PW = rdsSession.PW
PORT = rdsSession.PORT
DBNAME = rdsSession.DBNAME

### AWS.MySQL.DB : Connect ###
'''try:
    conn = mConn.connect(host=ENDPOINT, user=USER, passwd=PW, port=PORT, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)

except Exception as e:
    print("Database Connection Failed due to {}".format(e))
'''




### Freee_API ###
## Wallet_Txns.Json ##
def Wallet_Txns_Json(self):
    ### Def.API.Authorization.Code ###
    AUTH_CODE = 'e8359697eca39fffd5d58bc916a178efbf09552ec37f43450af4615e0201b8dd'

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
        # List : 再構築
        wTxns_Data = []

        Wallet_Txns_List = data_wallet_txns['wallet_txns']
        for w in Wallet_Txns_List:
            del w['company_id']
            del w['due_amount']

            # Json : 出力
            wj_id = w['id']
            wj_date = w['date']
            wj_wl = w['walletable_id']
            wj_des = w['description']
            wj_en = w['entry_side']
            wj_am = w['amount']
            wj_bl = w['balance']
            wj_wt = w['walletable_type']
            wTxns_Json.update(
                {"id": wj_id, "m_datetime": wj_date, "wallet_id": wj_wl, "description": wj_des, "entry_side": wj_en, \
                 "amount": wj_am, "balance": wj_bl, "wallet_type": wj_wt})
            # wTxns_Json.update({'id': wj_id, 'm_datetime': wj_date, 'wallet_id': wj_wl, 'description': wj_des, 'entry_side': wj_en, \
            #                   'amount': wj_am, 'balance': wj_bl, 'wallet_type': wj_wt})
            # print(wTxns_Json)

            # List : 出力
            wt_id = w['id']
            wt_date = datetime.strptime(w['date'], "%Y-%m-%d")
            wt_wl = w['walletable_id']
            wt_des = w['description']
            wt_en = w['entry_side']
            wt_am = w['amount']
            wt_bl = w['balance']
            wt_wt = w['walletable_type']
            wTxns_Data.append([wt_id, wt_date, wt_wl, wt_des, wt_en, wt_am, wt_bl, wt_wt])

        ### JSON to MySQL : INSERT INTO ###
        try:
            cnx = mConn.connect(host=ENDPOINT, user=USER, passwd=PW, port=PORT, database=DBNAME)
            cur = cnx.cursor(buffered=True, dictionary=True)
            # cur = conn.cursor()


            # sql = "SELECT now();"
            sql = ("""INSERT INTO DevDB.PlusFreee_wJson VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")
            # sql = ("""INSERT INTO PlusFreee_wJson VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")
            # sql = ("INSERT INTO PlusFreee_wJson VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            # sql = 'INSERT INTO PlusFreee_wJson VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            # sql = 'INSERT INTO DevDB.PlusFreee_wJson VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            # sql = 'INSERT INTO DevDB.PlusFreee_wJson VALUES ("121", "2021-02-01", "121", "Test", "income", 1200, 0, "bank_account");'

            # cur.execute(sql, ("125", "2021-02-01", 125, "Test", "income", 1200, 500, "bank_account")).fetchone()
            # cur.execute(sql, ("125", "2021-02-01", "125", "Test", "income", "1200", "500", "bank_account"))
            # cur.fetchone()
            # cur.fetchall()
            # wj_data = (wj_id, wj_date, wj_wl, wj_des, wj_en, wj_am, wj_bl, wj_wt)
            # cur.execute(sql, wj_data)
            # cur.fetchone()

            # cur.execute(sql, (json.dumps(wTxns_Json)))
            # sql_params = [dict({'id': j_id, 'm_datetime': j_date, 'wallet_id': j_wl, 'description': j_des, 'entry_side': j_en, 'amount': j_am, 'balance': j_bl, 'wallet_type': j_wt}) for j_id, j_date, j_wl, j_des, j_en, j_am, j_bl, j_wt in wTxns_Json.items()]
            # sql_data = [tuple(e.items() for e in wTxns_Json)]
            # sql_data = [tuple(e.values() for e in wTxns_Json)]
            # sql_data = [json.loads(t[0]) for t in wTxns_Json]
            # sql_data = [json.loads(wTxns_Json.read())]
            # print(sql_data)
            # for j in wTxns_Json:
            #    sql_data = (j['id'], j['m_datetime'], j['wallet_id'], j['description'], j['entry_side'], j['amount'], j['balance'], j['wallet_type'])
                # sql_data = [tuple(j['id'], j['m_datetime'], j['wallet_id'], j['description'], j['entry_side'], j['amount'], j['balance'], j['wallet_type'])]
                # cur.executemany(sql, sql_data)

            # cur.executemany(sql, (wTxns_Json,))

            cur.executemany(sql, wTxns_Data)



            # cur.executemany(sql, sql_data)

            # json_obj = wTxns_Json.json()
            # for j in wTxns_Json:
            #    wj_data = (j['id'], j['m_datetime'], j['wallet_id'], j['description'], j['entry_side'], j['amount'], j['balance'], j['wallet_type'])
            #    cur.execute(sql, wj_data)

            cnx.commit()

            cur.close()
            cnx.close()


            # row = cur.fetchone()
            # while row is None:
            #    break

            # while True:
            #    row = cur.fetchall()
                # row = cur.fetchone()
            #    if row is None:
            #        break


            # query_results = cur.fetchall
            # print(query_results)
            # cur.close()
            # conn.commit()
            # conn.close()


            # cur.execute("""SELECT now()""")
            # query_results = cur.fetchall()
            # print(query_results)

            # sql = """INSERT INTO DevDB.PlusFreee_wJson VALUES ('121', '2021-02-01', '121', 'Test', 'income', '1200', '0', 'bank_account')"""
            # sql = "INSERT INTO DevDB.PlusFreee_wJson (id, m_datetime, wallet_id, description, entry_side, amount, balance, wallet_type) VALUES (121, '2021-02-01', 121, 'Test', 'income', 1200, 0, 'bank_account');"
            # cur.execute(sql)
            # query_results = cur.fetchall()
            # print(query_results)
            # cur.executemany(sql)

        except Exception as e:
            print("Wallet_Txns_Json Database MySQL Table Connection Failed due to {}".format(e))

        # cur.executemany("INSERT INTO PlusFreee_wJson (id, m_datetime, wallet_id, description, entry_side, amount, balance, wallet_type) VALUES (121, '2021-02-01', 121, 'income', 1200, 0, 'bank_account')")
        # print(ENDPOINT, USER, PW, PORT, DBNAME)

        wTxns = Wallet_Txns_List

    # 受信エラー : != 200
    else:
        ErrorCode = rw.status_code
        GET_Data = ErrorCode

        wTxns = str(GET_Data) + " - "

    return a_code, r_code, company_id, wTxns

## Wallet Txns ###
def Wallet_Txns(self):

    ### Def.API.Authorization.Code ###
    AUTH_CODE = 'abdcb06a28ce9b4faf2e6834a9d633186a423ea4fd4edcd02b9e8fc08711193c'

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

        # CSV : 再構築
        wTxns_Data = []

        # wTxns_Json = cl.OrderedDict()

        Wallet_Txns_List = data_wallet_txns['wallet_txns']
        for w in Wallet_Txns_List:
            del w['company_id']
            del w['due_amount']
            # print(Wallet_Txns_List)

            # CSV : 出力
            wt_id = w['id']
            wt_date = datetime.strptime(w['date'], "%Y-%m-%d")
            wt_wl = w['walletable_id']
            wt_des = w['description']
            wt_en = w['entry_side']
            wt_am = w['amount']
            wt_bl = w['balance']
            wt_wt = w['walletable_type']
            wTxns_Data.append([wt_id, wt_date, wt_wl, wt_des, wt_en, wt_am, wt_bl, wt_wt])

            with open('PlusFreee_CSV/' + datetime.now().strftime("%Y%m%d") + '_' + str(offset) + '.csv', 'w', newline='') as csvFile:
            # with open('PlusFreee_CSV/' + str(offset) + '.csv', 'w', newline='') as csvFile:
            # with open('20210127.csv', 'w', newline='') as csvFile:
                out_csv = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                # out_csv.writerow(['id'])
                for d in wTxns_Data:
                    out_csv.writerow(d)

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

