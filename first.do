/* =============================================================================
File Name: first.do
Author: Milton Straw

Description.

Lorem ipsum.
============================================================================= */


// Log and clear
capture log close
log using first.log, replace
clear all


/* =============================================================================
IMPORT DATA
============================================================================= */
* Import IPEDS data
* import delimited "~/Documents/GitHub/wa_rmj/output/all_data.csv"


* Import sales data
* Step 1: Define .csv files
local filepath "~/Documents/Data/wa_rmj" // Save path to folder in a local
di "`filepath'" // Display path to folder
local files : dir "`filepath'" files "dispensing*.csv" // Save name of all files in folder ending with .csv in a local
di `"`files'"' // Display list of files to import data from

* Step 2: Loop over files
tempfile master
save `master', replace empty
foreach x of local files {
  di "`x'" // Display file name
  qui: import delimited "`x'", delimiter(",") case(preserve) clear // Import csv file
  qui: gen id = subinstr("`x'", ".dta.csv", "", .) // Generate id variable (same as file name but without .dta.csv)
  append using `master'
  save `master', replace
}

* Step 3: Export final data set
order id, first
sort id Segment
outsheet using dispensing_combined.csv , comma replace







/* =============================================================================
SAVE CLEANED DATA
============================================================================= */
* cd "~/Documents/GitHub/wa_rmj/output"
* outsheet using all_data_clean.csv , comma replace
