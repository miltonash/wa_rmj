# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-

''' Description.

This script was used to test merging options using pandas.
'''

import pandas as pd
# ==============================================================================


df1 = pd.DataFrame(
    {
        "unitid": [1001, 1001, 1001, 1002, 1002, 1002],
        "year": [2013, 2014, 2015, 2013, 2014, 2015],
        "data": [0, 1, 2, 7, 8, 9]
    }
)
print("\n DataFrame 1 \n", df1)


df2 = pd.DataFrame(
    {
        "unitid": [1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002],
        "year": [2013, 2013, 2013, 2014, 2014, 2014, 2015, 2015, 2015, 2013, 2013, 2013, 2014, 2014, 2014, 2015, 2015, 2015],
        "effylev": ["allstudents", "undergrad", "grad", "allstudents", "undergrad", "grad", "allstudents", "undergrad", "grad", "allstudents", "undergrad", "grad", "allstudents", "undergrad", "grad", "allstudents", "undergrad", "grad"]
    }
)
print("\n DataFrame2 \n", df2)


df3 = pd.merge_ordered(df1, df2, fill_method="ffill", left_by=["unitid",
                                                                "year"])
print("\n Merged Data \n", df3)
