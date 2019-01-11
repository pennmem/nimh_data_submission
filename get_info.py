import os
import numpy as np
import pandas as pd
import datetime as dt
from glob import glob

# Mapping of month names to numbers
month_dict = dict(
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
exp_dict = dict(
    pyFR=596,
    ltpFR=597,
    ltpFR2=599,
    SFR=748,
    FR1_scalp=748,
    VFFR=np.nan
)


def get_info(start_date, end_date, ltp_path='/data/eeg/scalp/ltp/'):

    # Load subject and session info
    sess_info = get_sess_info(start_date, end_date, ltp_path)
    subj_info = get_subj_info(ltp_path)

    # Add experiment name and subject info into session info
    for exp in sess_info:
        exp_id = exp_dict[exp]
        sess_info[exp]['experiment'] = pd.Series([exp for _ in range(len(sess_info[exp]))], index=sess_info[exp].index)
        sess_info[exp]['experiment_id'] = pd.Series([exp_id for _ in range(len(sess_info[exp]))], index=sess_info[exp].index)
        sess_info[exp]['birth_year'] = pd.Series(None, index=sess_info[exp].index)
        sess_info[exp]['gender'] = pd.Series(None, index=sess_info[exp].index)
        sess_info[exp]['age_in_months'] = pd.Series(None, index=sess_info[exp].index)
        for i, sess_data in sess_info[exp].iterrows():
            subj = subj_info[sess_data.subject]
            sess_info[exp].loc[i, 'birth_year'] = subj['birth']
            sess_info[exp].loc[i, 'gender'] = subj['gender']
            sess_info[exp].loc[i, 'age_in_months'] = calculate_age_in_months(sess_data, subj['birth'])

    # Merge session info from all experiments into a single frame
    info = None
    for exp in sess_info:
        if info is None:
            info = sess_info[exp]
        else:
            info = info.merge(sess_info[exp], how='outer')

    return info


def get_sess_info(start_date, end_date, ltp_path='/data/eeg/scalp/ltp/'):

    # Find the cmldb_sess_info file for each experiment
    info_files = glob(os.path.join(ltp_path, '*/cmldb_sess_info_*.txt'))

    # For each experiment/file, find all sessions that fall within the specified date range
    data = {}
    for f in info_files:
        info = pd.read_csv(f, delimiter='\t')
        mask = np.zeros(len(info), dtype=bool)
        # Check whether each session falls within the date range
        for i, sess in info.iterrows():
            sess_date = dt.date(sess.year, month_dict[sess.month], sess.day)
            if start_date <= sess_date <= end_date:
                mask[i] = True
        # Keep only the sessions that fall within the date range
        if mask.sum() > 0:
            exp_name = os.path.basename(os.path.splitext(f)[0])[16:]
            data[exp_name] = info.loc[mask]

    return data


def get_subj_info(ltp_path='/data/eeg/scalp/ltp/'):

    # Find the cmldb_subj_info file for each experiment
    info_files = glob(os.path.join(ltp_path, '*/cmldb_subj_info_*.txt'))

    # Load subject data for each experiment/file and enter it into a dictionary
    data = {}
    for f in info_files:
        info = pd.read_csv(f, delimiter='\t')
        for i, subj in info.iterrows():
            data[subj.subject] = {'educ': subj.education_years, 'birth': subj.birth_year, 'gender': subj.gender}

    return data


def calculate_age_in_months(sess_data, year, month=1, day=1):
    """
    Given session information and a date of birth, calculate the participant's age in months at the time of the session.

    :param sess_data: A dictionary or data frame containing the year, month, and day of a session.
    :param year: An integer indicating the year the participant was born.
    :param month: An integer or 3-letter string indicating the month the participant was born (Default=1).
    :param day: An integer indicating the day the participant was born (Default=1).
    :return: The age of the participant (in months) at the time of the session.
    """

    month = month_dict[month] if type(month) == str else month  # Convert string abbreviations for months into integers
    date_of_birth = dt.date(year, month, day)
    date_of_sess = dt.date(sess_data['year'], sess_data['month'], sess_data['day'])
    age = date_of_sess - date_of_birth  # Calculate age at time of session
    age = age.years * 12 + age.months + int(round(age.days / 31.))  # Convert age to months

    return age