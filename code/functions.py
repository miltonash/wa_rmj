# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: functions.py
# Author: Milton Straw

''' Description.

This script defines the necessary functions used to put together a five-year
data panel (longitudinal data) using using two surveys from IPEDS: (1) HD{}: Institutional Characteristics, (2) EFFY{}: 12-Month Enrollment. This script will be called by 'execute.py'.
'''
# ==============================================================================


# Import packages, listed alphabetically
import glob
import io
import os
import pandas as pd
import requests
import shutil
import sys
import zipfile
from numba import jit, cuda
from timeit import default_timer


''' Add more surveys.

To add more surveys in the future, replicate function steps ONE through FOUR. Replace all instances of IPEDS survey abbreviation (ex: HD{} or EFFY{}). Add the new survey data to step SIX.
'''


# Define function to collect HD{}, Institutional Characteristics
def collect_hd(years):
    # I use the ipeds prefix because the data comes from the:
    # [I]ntegrated [P]ostsecondary [E]ducation [D]ata [S]ystem
    ipeds_locs = 'https://nces.ed.gov/ipeds/datacenter/data/'
    ipeds_fils_hd = 'HD{}.zip'
    ipeds_dict_hd = 'HD{}_Dict.zip'
    # ================================================================= STEP ONE
    # Collect and extract data HD{}
    for yr in years:
        print('GETTING FILES FROM {}'.format(yr))
        rdata_hd = requests.get(ipeds_locs + ipeds_fils_hd.format(yr))
        rdict_hd = requests.get(ipeds_locs + ipeds_dict_hd.format(yr))
        rdata_hd_zip = zipfile.ZipFile(io.BytesIO(rdata_hd.content))
        rdict_hd_zip = zipfile.ZipFile(io.BytesIO(rdict_hd.content))

        print('Extracting {} files from zip archive:'.format(yr))
        rdata_hd_zip.printdir()
        rdict_hd_zip.printdir()
        rdata_hd_zip.extractall()
        rdict_hd_zip.extractall()

        print('Saving zip archive to disk.')
        open(ipeds_fils_hd.format(yr), 'wb').write(rdata_hd.content)
        open(ipeds_dict_hd.format(yr), 'wb').write(rdict_hd.content)

    # ================================================================= STEP TWO
    for yr in years:
        print('Replacing Code Values with Code Labels for HD{}.')

        # Extract frequencies tab the data dictionary (hdYYYY.xlsx)
        freqs_hd = pd.read_excel('hd{}.xlsx'.format(yr),
                                 sheet_name='Frequencies')
        # Put institutional data into a data frame (df)
        df_hd = pd.read_csv('hd{}.csv'.format(yr), encoding='ISO-8859-1')

        # Get list of categorical variable names
        cat_colms_hd = set(freqs_hd['varname'])

        # Remove fips code to prevent its modification
        cat_colms_hd.remove('FIPS')

        # Loop through categorical columns
        for col in cat_colms_hd:
            # Get map keys (code values)
            code_values_hd = freqs_hd[freqs_hd['varname'] == col]['codevalue']
            # Convert map keys to int where appropriate
            code_values_hd = [int(i) if str(i).isdigit()
                              else i for i in code_values_hd]
            # Get map value (ValueLabels)
            code_labels_hd = freqs_hd[freqs_hd['varname'] == col]['valuelabel']
            var_map_hd = dict(zip(code_values_hd, code_labels_hd))
            # Apply mapping dictionary to categorical column
            df_hd[col] = df_hd[col].map(var_map_hd)

    # =============================================================== STEP THREE
        # Create time index for panel specification
        df_hd['year'] = yr

        print('Writing hd{}.csv as csv'.format(yr))
        df_hd.columns = [i.lower() for i in df_hd.columns]
        df_hd.to_csv('hd{}.csv'.format(yr), index=False)
        print('Done!', end='\n\n')

    # ================================================================ STEP FOUR
    print('Sort hd_data.csv by unitid and year; keep only states of interest')

    hd_data = {}
    for yr in years:
        hd_data[yr] = pd.read_csv('hd{}.csv'.format(yr))

    df_hd = pd.concat(hd_data).sort_values(['unitid',
                                            'year']).set_index(['unitid',
                                                                'year'])
    print('Writing hd_data.csv as csv')
    df_hd.to_csv('hd_data.csv')
    print('DONE WITH HD{} SURVEY!', end='\n\n')


# Define function to collect EFFY{}, 12-Month Enrollment
def collect_effy(years):
    # I use the ipeds prefix because the data comes from the:
    # [I]ntegrated [P]ostsecondary [E]ducation [D]ata [S]ystem
    ipeds_locs = 'https://nces.ed.gov/ipeds/datacenter/data/'
    ipeds_fils_effy = 'EFFY{}.zip'
    ipeds_dict_effy = 'EFFY{}_Dict.zip'
    # ================================================================= STEP ONE
    # Collect and extract data for EFFY{}
    for yr in years:
        print('GETTING FILES FROM {}'.format(yr))
        rdata_effy = requests.get(ipeds_locs + ipeds_fils_effy.format(yr))
        rdict_effy = requests.get(ipeds_locs + ipeds_dict_effy.format(yr))
        rdata_effy_zip = zipfile.ZipFile(io.BytesIO(rdata_effy.content))
        rdict_effy_zip = zipfile.ZipFile(io.BytesIO(rdict_effy.content))

        print('Extracting {} files from zip archive:'.format(yr))
        rdata_effy_zip.printdir()
        rdict_effy_zip.printdir()
        rdata_effy_zip.extractall()
        rdict_effy_zip.extractall()

        print('Saving zip archive to disk.')
        open(ipeds_fils_effy.format(yr), 'wb').write(rdata_effy.content)
        open(ipeds_dict_effy.format(yr), 'wb').write(rdict_effy.content)

    # ================================================================= STEP TWO
    for yr in years:
        print('Replacing Code Values with Code Labels for EFFY{}.')

        # Extract frequencies tab the data dictionary (effyYYYY.xlsx)
        freqs_effy = pd.read_excel('effy{}.xlsx'.format(yr),
                                   sheet_name='Frequencies')
        # Put institutional data into a data frame (df)
        df_effy = pd.read_csv('effy{}_rv.csv'.format(yr), encoding='ISO-8859-1')

        # Get list of categorical variable names
        cat_colms_effy = set(freqs_effy['varname'])

        # Loop through categorical columns
        for col in cat_colms_effy:
            # Get map keys (code values)
            code_values_effy = freqs_effy[freqs_effy['varname'] ==
                                          col]['codevalue']
            # Convert map keys to int where appropriate
            code_values_effy = [int(i) if str(i).isdigit()
                                else i for i in code_values_effy]
            # Get map value (ValueLabels)
            code_labels_effy = freqs_effy[freqs_effy['varname'] ==
                                          col]['valuelabel']
            var_map_effy = dict(zip(code_values_effy, code_labels_effy))
            # Apply mapping dictionary to categorical column
            df_effy[col] = df_effy[col].map(var_map_effy)

    # =============================================================== STEP THREE
        # Create time index for panel specification
        df_effy['year'] = yr

        print('Writing effy{}_rv.csv as csv'.format(yr))
        df_effy.columns = [i.lower() for i in df_effy.columns]
        df_effy.to_csv('effy{}_rv.csv'.format(yr), index=False)
        print('Done!', end='\n\n')

    # ================================================================ STEP FOUR
    print('Sort effy_data.csv by unitid and year; keep only states of interest')

    effy_data = {}
    for yr in years:
        effy_data[yr] = pd.read_csv('effy{}_rv.csv'.format(yr))

    df_effy = pd.concat(effy_data).sort_values(['unitid',
                                                'year']).set_index(['unitid',
                                                                    'year'])
    print('Writing effy_data.csv as csv')
    df_effy.to_csv('effy_data.csv')
    print('DONE WITH EFFY{} SURVEY!', end='\n\n')


def merge():
    ''' Merge.

    Merge datasets generated from surveys across years into one all-inclusive
    data panel.
    '''

    # Check to see if the necessary files exist
    # mergeFiles = ["hd_data.csv", "effy_data.csv"];
    # mergeExist = [f for f in mergeFiles if os.path.isfile(f)];
    # mergeNonExist = list(set(mergeExist) ^ set(mergeFiles))
    if not os.path.exists(os.path.join(os.getcwd(), "hd_data.csv")):
        raise Exception('Oops! It looks like hd_data.csv does not exist. Try running collect_hd() first.')
    if not os.path.exists(os.path.join(os.getcwd(), "effy_data.csv")):
        raise Exception('Oops! It looks like effy_data.csv does not exist. Try running collect_effy() first.')


    print('Reading in hd_data.csv to DataFrame')
    hd_data = pd.read_csv('hd_data.csv', low_memory=False)
    # Optionally, print .head
    # print("\n HD Data \n", hd_data.head(n=20))

    print('Reading in effy_data.csv to DataFrame')
    effy_data = pd.read_csv('effy_data.csv', low_memory=False)
    # Optionally, print .head
    # print("\n EFFY Data \n", effy_data.head(n=20))

    print('Merging DataFrames and filling')
    start = timer()
    # @jit(target='cuda')
    all_data = pd.merge_ordered(hd_data, effy_data, fill_method="ffill",
                                left_by=["unitid", "year"])
    print("without GPU:", timer()-start)
    # Optionally, print .head to verify correct merge behavior
    # print("\n MERGED Data \n", all_data.head(n=50))

    # Keep only observations from states of interest
    print('Dropping unnecessary states')
    all_data[all_data["stabbr"].str.contains("Idaho|Oregon|Washington")==True]

    print('Writing all_data.csv as csv')
    all_data.to_csv('all_data.csv', index=False)
    print('DONE MERGING DATASETS!', end='\n\n')


def cleanup_dir(wd):
    # Cleanup output directory by deleting redundant files

    dir = os.path.join(wd, 'output')
    os.chdir(dir)

    if dir==os.getcwd():
        # Listing directory
        print("BEFORE--", os.getcwd(), "contains: %s" %os.listdir(os.getcwd()))
        for file in os.scandir(dir):
            if not file.name.startswith("all_data") and not file.name.endswith(".xlsx") and file.is_file():
                os.remove(os.path.join(dir, file))
                # Listing directory after file removal
                print("%s has been removed successfully" %file)
            else:
                continue

    # folder path and destination
    new_folder = 'dictionaries'
    dict_path = dir + '/dictionaries'
    dictExist = os.path.exists(dict_path)
    if not dictExist:
        os.mkdir(os.path.join(dir, new_folder))

    # loop through the directory to move all the files
    for filename in os.listdir(dir):
        # move all the files
        f = os.path.basename(os.path.join(dir, filename))
        if filename.endswith(".xlsx"):
            src = os.path.join(dir, f)  # file source
            dst = os.path.join(dir+'/'+new_folder, f)  # file destination
            os.rename(src, dst) # move file
        else:
            continue

    print("AFTER--", os.getcwd(), "contains: %s" %os.listdir(os.getcwd()))
