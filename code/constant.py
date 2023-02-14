# library
import pandas as pd
import numpy as np
import math
import copy
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from datetime import date, timedelta

# constant
MAX_STATION = 518
MAX_STATION_INDEX = 26
DEFAULT_START_DATE = date(1999, 1, 1)
MIN_YEAR=1999
MAX_YEAR=2022

# function
# convert date to string
def date_to_int(time):
  return (date(time.year, time.month, time.day) - DEFAULT_START_DATE).days

def int_to_date(days):
  return DEFAULT_START_DATE + timedelta(days = days)

# creating multi color option for plot
def color(count):
  return cm.rainbow(np.linspace(0, 1, count)) 
