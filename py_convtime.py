# PYTHON scripts that calls py_jdutil.py to convert time from/to (M)JD/date

"""
A few examples and functions of time conversions from:
https://gist.github.com/jiffyclub/1294443#file-jdutil-py renamed py_jdutil.py
"""

from py_jdutil import jd_to_date
from py_jdutil import mjd_to_jd
from py_jdutil import date_to_jd
from py_jdutil import hmsm_to_days
from py_jdutil import days_to_hmsm
from py_jdutil import jd_to_mjd

MJD_value=58970.01875000   # manual time value

JD_value=2458970.5         # manual time value

Date_value=(2020,5,1)

Day_time_HMSM=(00,25,45.073)  # Start time of Swift obs

print("Swift obs /  JD  =",mjd_to_jd(MJD_value))

print("Swift obs / date =",jd_to_date(mjd_to_jd(MJD_value)))

print("Swift obs /  JD  =",date_to_jd(*Date_value))

# Calculating exact start time:

Date_start=date_to_jd(*Date_value)+hmsm_to_days(*Day_time_HMSM)

print("Start obs /  JD  =",Date_start)
