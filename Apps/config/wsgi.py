#//+------------------------------------------------------------------+
#//|                              VerysVeryInc.Python3.Django.Wsgi.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|       "VsV.Python3.Django.Wsgi.py - Ver.3.0.1 Update:2018.03.07" |
#//+------------------------------------------------------------------+
#//|                                           https://qiita.com/aion |
#//|               https://qiita.com/aion/items/ca375efac5b90deed382/ |
#//+------------------------------------------------------------------+
"""
WSGI config for Apps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

### MatsuoStation.Com ###
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Apps.settings")

application = get_wsgi_application()
