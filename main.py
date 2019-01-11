import os
import pandas as pd
import datetime as dt
from get_info import get_info
from fill_info import fill_info
from write_info import write_info

#####
# SETTINGS
#####
eeg_details_path = os.path.expanduser('~/Desktop/NIMH_Share_Jan19/eeg_details01.csv')
eeg_sub_files_path = os.path.expanduser('~/Desktop/NIMH_Share_Jan19/eeg_sub_files01.csv')
date_range_start = dt.date(year=2018, month=6, day=2)
date_range_end = dt.date(year=2019, month=1, day=15)
ltp_path = '/data/eeg/scalp/ltp/'

#####
# LOAD INFO
#####
# Load spreadsheet headers and save original column order (for when we write the CSV later)
ed = pd.read_csv(eeg_details_path, header=1, nrows=0)
esf = pd.read_csv(eeg_sub_files_path, header=1, nrows=0)
ed_col_order = ed.columns
esf_col_order = esf.columns

# Load subject and session information
sess_info = get_info(date_range_start, date_range_end, ltp_path=ltp_path)

# Fill subject and session information into the spreadsheet
ed, esf = fill_info(ed, esf, sess_info)

# Write data to spreadsheets
write_info(ed, esf)
