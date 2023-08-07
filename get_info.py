import os
import numpy as np
import pandas as pd
import datetime as dt
from glob import glob

# Mapping of month names to numbers
MONTH_DICT = dict(
    Jan=1,
    Feb=2,
    Mar=3,
    Apr=4,
    May=5,
    Jun=6,
    Jul=7,
    Aug=8,
    Sep=9,
    Oct=10,
    Nov=11,
    Dec=12
)

# Dictionary of Experiment ID numbers
EXP_DICT = dict(
    pyFR=596,
    ltpFR=597,
    ltpFR2=599,
    SFR=748,
    FR1_scalp=748,
    VFFR=1183,
    ltpDelayRepFRReadOnly=2321
)

# List of subject info fields to load from ltp/<exp>/cmldb_subj_info_<exp>.csv (names must match column headers)
CMLDB_SUBJ_FIELDS = ('gender',)

# List of subject info fields to load from participant questionnaire ltp/SubjectInfo/subject_info.csv
SUBJ_INFO_FIELDS = ('hand_throw', 'hand_toothbrush', 'hand_scissors', 'hand_write')


def get_info(start_date, end_date, ltp_path='/data/eeg/scalp/ltp/'):
    """
    Loads information about all sessions (from the cmldb_sess_info_<exp>.txt files) and subjects (from the
    cmldb_subj_info_<exp>.txt files). Then, selects only the sessions which occurred in the specified date range.
    Finally, adds subject information to each session and returns it as a data frame.

    Information handled by this function includes the subject, date, time, experiment, session number, hours of sleep,
    alertness, and gender associated with each session.

    To be added: handedness information.

    :param start_date: A datetime date object indicating earliest date to include sessions from (inclusive).
    :param end_date: A datetime date object indicating latest date to include sessions from (inclusive).
    :param ltp_path: The path to the standard LTP directory on Rhino (/data/eeg/scalp/ltp/).
    :return: A data frame containing one row for each session.
    """
    # Load subject and session info
    sess_info = get_sess_info(start_date, end_date, ltp_path)
    subj_info = get_subj_info(ltp_path)

    for exp in sess_info:
        # Add experiment name and ID to session info
        exp_id = EXP_DICT[exp]
        sess_info[exp]['experiment'] = pd.Series([exp for _ in range(len(sess_info[exp]))], index=sess_info[exp].index)
        sess_info[exp]['experiment_id'] = pd.Series([exp_id for _ in range(len(sess_info[exp]))], index=sess_info[exp].index)
        # Create fields for subject info in data frame
        for key in CMLDB_SUBJ_FIELDS:
            sess_info[exp][key] = pd.Series(None, index=sess_info[exp].index)
        for key in SUBJ_INFO_FIELDS:
            sess_info[exp][key] = pd.Series(None, index=sess_info[exp].index)
        # Add subject info from CMLDB and subject info questionnaire to each session
        for i, sess_data in sess_info[exp].iterrows():
            subj = subj_info[sess_data.subject]
            for key in CMLDB_SUBJ_FIELDS:
                sess_info[exp].loc[i, key] = subj[key] if key in subj else np.nan
            for key in SUBJ_INFO_FIELDS:
                sess_info[exp].loc[i, key] = subj[key] if key in subj else np.nan

    # Merge session info from all experiments into a single frame
    info = None
    for exp in sess_info:
        if info is None:
            info = sess_info[exp]
        else:
            info = info.merge(sess_info[exp], how='outer')

    return info


def get_sess_info(start_date, end_date, ltp_path='/data/eeg/scalp/ltp/'):
    """
    Loads information about all sessions from the cmldb_sess_info_<exp>.txt files present in each experiment's LTP
    directory. Only returns data from sessions that took place in the specified date range.

    :param start_date: A datetime date object indicating earliest date to include sessions from (inclusive).
    :param end_date: A datetime date object indicating latest date to include sessions from (inclusive).
    :param ltp_path: The path to the standard LTP directory on Rhino (/data/eeg/scalp/ltp/).
    :return: A dictionary mapping experiment names to data frames containing one row for each session.
    """
    # Find the cmldb_sess_info file for each experiment
    info_files = glob(os.path.join(ltp_path, '*/cmldb_sess_info_*.txt'))

    # For each experiment/file, find all sessions that fall within the specified date range
    data = {}
    for f in info_files:
        info = pd.read_csv(f, delimiter='\t')
        mask = np.zeros(len(info), dtype=bool)
        # Check whether each session falls within the date range
        for i, sess in info.iterrows():
            info.loc[i, 'month'] = MONTH_DICT[sess.month]
            sess_date = dt.date(sess.year, info.loc[i, 'month'], sess.day)
            if start_date <= sess_date <= end_date:
                mask[i] = True
        # Keep only the sessions that fall within the date range, and for those sessions create a MM/DD/YYYY date field
        if mask.sum() > 0:
            exp_name = os.path.basename(os.path.splitext(f)[0])[16:]
            data[exp_name] = info.loc[mask]
            data[exp_name]['date'] = pd.Series(None, index=data[exp_name].index)
            for i, sess in data[exp_name].iterrows():
                sess_date = dt.date(sess.year, sess.month, sess.day)
                data[exp_name].loc[i, 'date'] = sess_date.strftime('%m/%d/%Y')

    return data


def get_subj_info(ltp_path='/data/eeg/scalp/ltp/'):
    """
    Loads information about all subjects from the cmldb_sess_info_<exp>.txt files present in each experiment's LTP
    directory. Then load information from the participant information questionnaire (ltp/SubjectInfo/subject_info.csv).

    :param ltp_path: The path to the standard LTP directory on Rhino (/data/eeg/scalp/ltp/).
    :return: A dictionary mapping subject IDs to dictionaries of subject information.
    """
    # Find the cmldb_subj_info file for each experiment
    info_files = glob(os.path.join(ltp_path, '*/cmldb_subj_info_*.txt'))  # Subject info files from CMLDB
    info_spreadsheet = os.path.join(ltp_path, 'SubjectInfo/subject_info.csv')  # Answers from subject info questionnaire

    # Load CMLDB subject data for each experiment/file and enter it into a dictionary
    data = {}
    for f in info_files:
        info = pd.read_csv(f, delimiter='\t')
        for i, subj in info.iterrows():
            data[subj.subject] = {}
            for key in CMLDB_SUBJ_FIELDS:
                data[subj.subject][key] = subj[key]

    # Load information from subject info questionnaire and add it to each participant's dictionary
    info = pd.read_csv(info_spreadsheet, delimiter=',')
    for i, subj in info.iterrows():
        names = subj.snum.split(';')
        for name in names:
            if name in data:
                for key in SUBJ_INFO_FIELDS:
                    data[name][key] = subj[key]

    return data
