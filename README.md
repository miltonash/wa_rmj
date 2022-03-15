# WA RMJ

WA RMJ collects and analyzes data for research, "The Effect of College Students on Recreational Marijuana Sales in Washington State".

## Installation of Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

## Usage

Some packages are included in the Python distribution by default. Those that aren't need to be installed (using requirements.txt) and imported. The following explains why each of these packages is being installed.

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
# wa_rmj
