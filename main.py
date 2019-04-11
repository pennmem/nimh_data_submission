import os
import pandas as pd
import datetime as dt
from get_info import get_info
from get_extra_info import get_extra_info
from get_filepaths import get_filepaths
from fill_info import fill_info
from write_info import write_info

#####
# SETTINGS
#####
ltp_path = os.path.expanduser('~/rhino_mount/data/eeg/scalp/ltp/')  # Path to ltp data directory on Rhino
protocols_path = os.path.expanduser('~/rhino_mount/protocols/ltp/')  # Path to ltp protocols directory on Rhino
eeg_details_path = os.path.expanduser('~/Desktop/NIMH_Share_Jan19/eeg_details01.csv')  # Path to eeg_details file
eeg_sub_files_path = os.path.expanduser('~/Desktop/NIMH_Share_Jan19/eeg_sub_files01.csv')  # Path to eeg_sub_files file
extra_info_path = os.path.expanduser('~/Desktop/NIMH_Share_Jan19/extra_data.txt')  # Path to manually-compiled info
date_range_start = dt.date(year=2018, month=6, day=2)  # Earliest session date to include (inclusive)
date_range_end = dt.date(year=2019, month=1, day=15)  # Latest session date to include (inclusive)

#####
# PIPELINE
#####
if __name__ == "__main__":

    # Load spreadsheet headers and save original column order (for when we write the CSV later)
    ed = pd.read_csv(eeg_details_path, header=1, nrows=0)
    esf = pd.read_csv(eeg_sub_files_path, header=1, nrows=0)
    ed_col_order = ed.columns
    esf_col_order = esf.columns

    # Load subject and session information into a data frame
    info = get_info(date_range_start, date_range_end, ltp_path=ltp_path)

    # Load extra manually-compiled information (date of birth, head circumference, cap size) into the data frame
    info = get_extra_info(info, extra_info_path)

    # Identify data file paths for each session, and add them to the data frame
    info = get_filepaths(info, ltp_path=ltp_path, protocols_path=protocols_path)

    # Fill out the two spreadsheets with
    ed, esf = fill_info(ed, esf, info)

    # Write data to spreadsheets
    write_info(ed, eeg_details_path, ed_col_order, esf, eeg_sub_files_path, esf_col_order)
