#//+--------------------------------------------------------------------+
#//|                      VerysVeryInc.Py3.Django.aInvoice.AWS.mysql.py |
#//|                    Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                   https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                   Since:2018.03.05 |
#//|                                  Released under the Apache license |
#//|                         https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.aInv.AWS.MySQL.py - Ver.3.91.9 Update:2021.02.08" |
#//+--------------------------------------------------------------------+
import json


### JSON.Load : fxpro_config.json ###
with open("../awsconfig.json", encoding='utf-8') as f:
    rds_dict = json.load(f)


### AWS.RDS.MySQL : Setup ###
ENDPOINT = rds_dict['host'] 	# AWS.RDS.MySQL : EndPoint
PORT = 3306         			# AWS.RDS.MySQL : Port
USR = rds_dict['user']			# AWS.RDS.MySQL : UserName
PW = rds_dict['password']		# AWS.RDS.MySQL : PassWord
DBNAME = rds_dict['database']	# AWS.RDS.MySQL : Database Name