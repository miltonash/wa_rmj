###############################################################################
'''
Define functions to be used for solving NaNinOrgid problem in dispensary data.
'''

# Import packages
import pandas as pd
import os
###############################################################################


os.chdir('../input')
with os.scandir() as it:
    for entry in it:
        if entry.name.endswith(".csv") and entry.is_file():

            # Open .csv, make list of orgid errors, extra intersection to make sure we're targeting the patterned issue only
            data = pd.read_csv(entry, dtype=object)
            myList1 = list(data.index[data['strain'] == 'GRAND DADDY PURPLE GREEN PHENO'])
            myList2 = list(data.index[data[['description', 'thc', 'thca', 'cbd', 'totalthc', 'price', 'quantity']].isna().all(1)])
            intersectionList = set.intersection(set(myList1), set(myList2))

            # Updating the column value/data
            for i in intersectionList:

                data.at[i, 'description'] = data.at[i+1, 'location']
                data.at[i, 'thc'] = data.at[i+1, 'inventoryid']
                data.at[i, 'thca'] = data.at[i+1, 'wholesaler']
                data.at[i, 'cbd'] = data.at[i+1, 'usableweight']
                data.at[i, 'totalthc'] = data.at[i+1, 'inventorytype']
                data.at[i, 'price'] = data.at[i+1, 'productname']
                data.at[i, 'quantity'] = data.at[i+1, 'strain']
                data.at[i, 'wholesalecost'] = data.at[i+1, 'description']
                data.at[i, 'localtax'] = data.at[i+1, 'thc']
                data.at[i, 'statetax'] = data.at[i+1, 'thca']
                data.at[i, 'taxinclusiveprice'] = data.at[i+1, 'cbd']
                data.at[i, 'year'] = data.at[i+1, 'totalthc']
                data.at[i, 'quarter'] = data.at[i+1, 'price']
                data.at[i, 'month'] = data.at[i+1, 'quantity']
                data.at[i, 'week'] = data.at[i+1, 'wholesalecost']
                data.at[i, 'date'] = data.at[i+1, 'localtax']
                data.at[i, 'inventoryparentid'] = data.at[i+1, 'statetax']
                data.at[i, 'parentid_transfers'] = data.at[i+1, 'taxinclusiveprice']
                data.at[i, 'parentid'] = data.at[i+1, 'year']
                data.at[i, 'entrydate'] = data.at[i+1, 'quarter']
                data.at[i, 'exitdate'] = data.at[i+1, 'month']
                data.at[i, 'day'] = data.at[i+1, 'week']

            for i in intersectionList:
                data = data.drop(i+1)

            # Writing into the file
            data.to_csv(entry.name, index=False)
            print(entry.name)

print("All done!")
