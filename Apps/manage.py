#//+------------------------------------------------------------------+
#//|                            VerysVeryInc.Python3.Django.Manage.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Python3.Django.Manage.py - Ver.3.0.1 Update:2018.03.07" |
#//+------------------------------------------------------------------+
#!/usr/bin/env python
import os
import sys

### MatsuoStation.Com : AWS.RDS.MySQL ###
import pymysql
pymysql.install_as_MySQLdb()

if __name__ == "__main__":

    ### MatsuoStation.Com ###
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Apps.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
