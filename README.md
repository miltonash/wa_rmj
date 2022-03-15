# WA RMJ

WA RMJ collects data for the research project, "The Effect of College Students on Recreational Marijuana Sales in Washington State".

## Installation of Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

## Usage

The 'execute.py' script calls modules defined as functions from the 'functions.py' script. These modules reach out to IPEDS, collect data grouped into surveys based on parameterized years and states, extract and merge the datasets into one longitudinal data panel, update the included data dictionaries to include code labels instead of code values for better readability, and remove redundant datasets leaving behind only the merged dataset. The scripts 'NaNinOrgid_test.py' and 'NaNinOrgid_fix.py' identify data errors in dispensary-level sales data from WA state, then iterates through those files and corrects the issue.

A handful of packages are used to accomplish the tasks defined in these scripts. Some packages are included in the Python distribution by default. Those that aren't need to be installed (using requirements.txt) and imported. The following explains why each of these packages is being installed.

```python
import pandas
# work with .csv and Excel files as DataFrames
pd.read_excel('file_name.xlsx')
pd.read_csv('file_name.csv')

import requests
# send HTTP/1.1 requests
requests.get('url')

from numba import jit, cuda
# use gpu for faster processing
@jit(target='cuda') # only for gpu's with Cuda cores, commented out by default

from timeit import default_timer as timer
# time process to verify that gpu is faster than cpu
start = timer()
print(timer()-start)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
