import pandas as pd
import datetime as dt


def get_extra_info(info, extra_info_path):

    # Read in extra info and organize into a dictionary
    data = {}
    with open(extra_info_path, 'r') as f:
        text = f.readlines()
        text = [line.replace('\n', '').split('\t') for line in text]
    # Create dictionary mapping participant ID to date of birth, head circumference, and cap size
    for line in text:
        dob = line[1].split('/')
        data[line[0]] = dict(
            year=int(dob[2]),
            month=int(dob[0]),
            day=int(dob[1]),
            head_circum=float(line[2]),
            cap_size=line[3],
            guid=line[4]
        )

    # Add extra info to data frame
    info['head_circum'] = pd.Series(None, index=info.index)
    info['cap_size'] = pd.Series(None, index=info.index)
    info['age_in_months'] = pd.Series(None, index=info.index)
    info['subjectkey'] = pd.Series(None, index=info.index)
    for i, sess_data in info.iterrows():
        subj = sess_data.subject
        d = data[subj]
        info.loc[i, 'age_in_months'] = calculate_age_in_months(sess_data, d['year'], d['month'], d['day'])
        info.loc[i, 'head_circum'] = data[subj]['head_circum']
        info.loc[i, 'cap_size'] = data[subj]['cap_size']
        info.loc[i, 'subjectkey'] = data[subj]['guid']

    return info


def calculate_age_in_months(sess_data, year, month=1, day=1):
    """
    Given session information and a date of birth, calculate the participant's age in months at the time of the session.

    :param sess_data: A dictionary or data frame containing the year, month, and day of a session.
    :param year: An integer indicating the year the participant was born.
    :param month: An integer or 3-letter string indicating the month the participant was born (Default=1).
    :param day: An integer indicating the day the participant was born (Default=1).
    :return: The age of the participant (in months) at the time of the session.
    """
    date_of_birth = dt.date(year, month, day)
    date_of_sess = dt.date(sess_data['year'], sess_data['month'], sess_data['day'])
    age = date_of_sess - date_of_birth  # Calculate age at time of session
    age = int(round(age.days / 31.))  # Convert age to months

    return age
