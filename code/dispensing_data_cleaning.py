# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: dispensing_data_cleaning.py
# Author: Milton Straw

''' Description.

This script defines the necessary functions used to clean the dataset
'dispensing_combined.csv'. It is paramterized for easy changes and
repeatability.
'''
# ==============================================================================
# !!! SET DIRECTORIES !!!
wd = "/Users/Milton/Documents/GitHub/wa_rmj"
files_loc = "/Users/Milton/Documents/Data/wa_rmj/input"
# ==============================================================================

# Import packages, listed alphabetically
import glob
import numba
import os
os.chdir(wd)
import pandas as pd
import sys
sys.path.append("code")
import send_sms as sms # local
from datetime import timedelta
from numba import jit
from timeit import default_timer as timer


# @cuda.jit(nopython=True)
@jit
def dispensing_data_cleaning():

    start = timer()
    # read in the raw data
    df = pd.read_csv(os.path.join(files_loc, 'dispensing_combined.csv'),
                     dtype=object)



    df.sort_values(by=['year', 'quarter', 'month', 'week', 'day', 'orgid'])
    print('Overwriting dispensing_cleaned.csv as csv')
    os.chdir(files_loc)
    df.to_csv('dispensing_cleaned.csv', index=False)
    elapsed = timer()-start
    print("CLEANING COMPLETE! Time elasped:", str(timedelta(seconds=elapsed)),
           end='\n\n')
    sms.send_sms()


dispensing_data_cleaning()
