#//+------------------------------------------------------------------+
#//|                            VerysVeryInc.Python3.Django.Manage.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Python3.Django.Manage.py - Ver.1.0.1 Update:2018.03.08" |
#//+------------------------------------------------------------------+
#//|                                           https://qiita.com/aion |
#//|               https://qiita.com/aion/items/ca375efac5b90deed382/ |
#//+------------------------------------------------------------------+
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    ### MatsuoStation.Com ###
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Devs.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
