# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: merge_dispensing.py
# Author: Milton Straw

''' Description.

This script defines the necessary functions used to put together a five-year
data panel (longitudinal data) using using two surveys from IPEDS: (1) HD{}: Institutional Characteristics, (2) EFFY{}: 12-Month Enrollment. This script will be called by 'execute.py'.
'''
# ==============================================================================
# !!! SET DIRECTORIES !!!
# files_loc = "/Volumes/My Passport"
wd = "/Users/Milton/Documents/GitHub/wa_rmj"
files_loc = "/Users/Milton/Documents/Data/wa_rmj"
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
from numba import jit
from timeit import default_timer as timer


# @cuda.jit(nopython=True)
@jit
def merge_dispensing():
    ''' Merge.

    Merge WA-state dispensary weekly datasets into one all-inclusive
    data panel.
    '''

    # setting the path for joining multiple files
    files = os.path.join(files_loc, "dispensing*.dta.csv")
    # list of merged files returned
    files = glob.glob(files)
    print(files, end='\n\n')
    print("Merging...")
    start = timer()
    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.sort_values(by=['year', 'quarter', 'month', 'week', 'day', 'orgid'])
    os.chdir(files_loc)
    df.to_csv('dispensing_combined.csv', index=False)
    print("MERGE COMPLETE! It took:", timer()-start , "seconds.")
    sms.send_sms()


merge_dispensing()
