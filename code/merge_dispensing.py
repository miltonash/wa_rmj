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
# !!! SET WORKING DIRECTORY !!!
wd = "/Volumes/My Passport/"
# ==============================================================================

# Import packages, listed alphabetically
import glob
import os
import pandas as pd
import sys
sys.path.append("code")
import send_sms as sms # local
from timeit import default_timer as timer


def merge_dispensing():
    ''' Merge.

    Merge WA-state dispensary weekly datasets into one all-inclusive
    data panel.
    '''

    # setting the path for joining multiple files
    files = os.path.join(wd, "dispensing*.csv")
    # list of merged files returned
    files = glob.glob(files)
    print("Merging...")
    start = timer()
    # joining files with concat and read_csv
    # df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    print("MERGE COMPLETE! It took: ", timer()-start , " seconds.")
    sms.send_sms()
