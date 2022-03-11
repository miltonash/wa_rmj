# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: execute.py
# Author: Milton Straw

''' Description.

This script puts together a five-year data panel (longitudinal data), using
public data available from the US Department of Education, by calling functions
defined in 'functions.py'. It then cleans up '/ouput' directory to remove
redundant files resulting from the collection process. This script holds
parameters for other scripts in this project. This is a convenient, organized
way to set parameters that might need to be changed in the future.
'''
# ==============================================================================
# !!! SET WORKING DIRECTORY !!!
wd = "/Users/Milton/Documents/GitHub/wa_rmj"
# !!! SET SCRIPT LOCATION (directory where 'functions.py' is located) !!!
func_loc = "/Users/Milton/Documents/GitHub/wa_rmj/code"
# ==============================================================================


# Import packages
import sys
sys.path.append(func_loc)
import functions as f # local
import os


# Parameters
# ==============================================================================
years = [2013, 2014, 2015, 2016, 2017]


# Setup 'output' directory for functions to place files into
output_loc = wd + '/output'
isExist = os.path.exists(output_loc)
if not isExist:
    os.mkdir(os.path.join(wd, 'output'))
os.chdir(output_loc)


'''
--------------------------------------------------------------------------------
Collect IPEDS Data: HD{}, Institutional Characteristics
--------------------------------------|-----------------------------------------
Call the 'collect_hd()' function from 'functions.py' imported above.
--------------------------------------------------------------------------------
'''
if input("Collect IPEDS data for Institutional Characteristics? (y/n)") == "y":
    f.collect_hd(years)
else:
    print("skipped collect_hd()")


'''
--------------------------------------------------------------------------------
Collect IPEDS Data: EFFY{}, 12-Month Enrollment
--------------------------------------|-----------------------------------------
Call the 'collect_effy()' function from 'functions.py' imported above.
--------------------------------------------------------------------------------
'''
if input("Collect IPEDS data for 12-Month Enrollment? (y/n)") == "y":
    f.collect_effy(years)
else:
    print("skipped collect_effy()")


'''
--------------------------------------------------------------------------------
Merge IPEDS Survey Data
--------------------------------------|-----------------------------------------
Call the 'merge()' function from 'functions.py' imported above.
--------------------------------------------------------------------------------
'''
if input("Merge datasets? (y/n)") == "y":
    f.merge()
else:
    print("skipped merge()")


'''
--------------------------------------------------------------------------------
Cleanup 'Output' Directory
--------------------------------------|-----------------------------------------
Call the 'cleanup_dir()' function from 'functions.py' imported above.
--------------------------------------------------------------------------------
'''
if input("Cleanup output directory? (y/n)") == "y":
    f.cleanup_dir(wd)
else:
    print("skipped cleanup_dir()")
