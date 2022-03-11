###############################################################################
'''
Look for 'NaNinOrgid' problem in dispensary data.
'''

# Import packages
import pandas as pd
import os
###############################################################################


os.chdir('../input')
with os.scandir() as it:
    for entry in it:
        if entry.name.endswith(".csv") and entry.is_file():

            # Open .csv, look for orgid errors
            df = pd.read_csv(entry, dtype=object)
            if df['orgid'].isna().all():
                print("NaNinOrgid")
            else:
                continue



print("All done!")
