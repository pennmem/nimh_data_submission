import os
import glob
import pandas as pd
from __future__ import print_function


def get_filepaths(info, ltp_path='/data/eeg/scalp/ltp/', protocols_path='/protocols/ltp/'):
    """
    Identifies the EEG and behavioral data files for each session listed in the input data frame. File paths are
    identified based on the experiment name, subject ID, and session number listed within each session's info in the
    data frame. Note that different experiments use different helper functions based on which files are needed and how
    they are organized.

    :param info: Data frame containing one row for each session's information.
    :param ltp_path: The path to the standard LTP directory on Rhino (/data/eeg/scalp/ltp/).
    :param protocols_path: The path the processed LTP directory on Rhino (/protocols/ltp/).
    :return: The session info data frame with paths to the data files added.
    """
    info['data_file1'] = pd.Series(None, index=info.index)
    info['data_file1_type'] = pd.Series(None, index=info.index)
    info['data_file2'] = pd.Series(None, index=info.index)
    info['data_file2_type'] = pd.Series(None, index=info.index)
    info['data_file3'] = pd.Series(None, index=info.index)
    info['data_file3_type'] = pd.Series(None, index=info.index)
    info['data_file4'] = pd.Series(None, index=info.index)
    info['data_file4_type'] = pd.Series(None, index=info.index)
    total_size = 0

    for i, sess_data in info.iterrows():

        # Identify session directories
        exp = sess_data.experiment
        subj = sess_data.subject
        sess = sess_data.session
        sess_path = os.path.join(ltp_path, '%s/%s/session_%s' % (exp, subj, sess))
        db_path = os.path.join(protocols_path, 'subjects/%s/experiments/%s/sessions/%s' % (subj, exp, sess))

        # Determine the file paths and file types for the current session
        if exp == 'pyFR':
            filepaths = get_filepaths_pyFR(sess_path, db_path)
        elif exp == 'ltpFR2':
            filepaths = get_filepaths_ltpFR2(sess_path, db_path)
        elif exp in ('SFR', 'FR1_scalp'):
            filepaths = get_filepaths_SFR(sess_path, ltp_path, exp, subj)
        elif exp == 'VFFR':
            filepaths = get_filepaths_VFFR(sess_path, db_path)
        else:
            filepaths = ['' for _ in range(8)]

        # Add file information to the data frame
        info.loc[i, ('data_file1', 'data_file1_type', 'data_file2', 'data_file2_type',
                     'data_file3', 'data_file3_type', 'data_file4', 'data_file4_type')] = filepaths

        for j, path in enumerate(filepaths):
            if j in (0, 2, 4, 6) and path != '':
                total_size += os.path.getsize(path)

    total_size /= 1073741824.
    print('Total Upload Size: %s GB' % total_size)

    return info


def get_filepaths_pyFR(sess_path):
    """
    Finds file paths for the EEG file(s), MATLAB events file, and sync pulse log for a pyFR session. If events are not
    available, uses the session log instead.

    :param sess_path: The path to the directory for a specific pyFR session.
    :return: An 8-item list containing up to four file paths and their file types, to be filled into the spreadsheet.
    """
    eeg_files = glob.glob(os.path.join(sess_path, 'eeg', '*.bdf')) + \
                glob.glob(os.path.join(sess_path, 'eeg', '*.bdf.bz2'))
    eeg_files = [''] if len(eeg_files) == 0 else eeg_files
    events_file = os.path.join(sess_path, 'events.mat')
    session_log = os.path.join(sess_path, 'session.log')
    sync_file = os.path.join(sess_path, 'eeg.eeglog')

    filepaths = ['' for _ in range(8)]
    filepaths[0] = eeg_files[0]
    filepaths[1] = 'EEG' if filepaths[0] != '' else ''
    filepaths[2] = events_file if os.path.exists(events_file) else session_log
    filepaths[3] = 'Behavioral' if os.path.exists(events_file) else 'Session Log'
    filepaths[4] = sync_file if os.path.exists(sync_file) else ''
    filepaths[5] = 'Sync Pulse Log' if filepaths[4] != '' else ''
    filepaths[6] = eeg_files[1] if len(eeg_files) > 1 else ''
    filepaths[7] = 'EEG' if filepaths[6] != '' else ''

    return filepaths


def get_filepaths_ltpFR2(sess_path, db_path):
    """
    Finds file paths for the EEG file(s), JSON events file, and sync pulse log for a pyFR session. If events are not
    available, uses the session log instead.

    :param sess_path: The path to the LTP directory for a specific ltpFR2 session.
    :param db_path: The path to the protocols directory for a specific ltpFR2 session.
    :return: An 8-item list containing up to four file paths and their file types, to be filled into the spreadsheet.
    """
    eeg_files = glob.glob(os.path.join(db_path, 'ephys', 'current_processed', '*.bdf'))
    eeg_files = [''] if len(eeg_files) == 0 else eeg_files
    events_file = os.path.join(db_path, 'behavioral', 'current_processed', 'all_events.json')
    session_log = os.path.join(sess_path, 'session.log')
    sync_file = os.path.join(sess_path, 'eeg.eeglog')

    filepaths = ['' for _ in range(8)]
    filepaths[0] = eeg_files[0]
    filepaths[1] = 'EEG' if filepaths[0] != '' else ''
    filepaths[2] = events_file if os.path.exists(events_file) else session_log
    filepaths[3] = 'Behavioral' if os.path.exists(events_file) else 'Session Log'
    filepaths[4] = sync_file if os.path.exists(sync_file) else ''
    filepaths[5] = 'Sync Pulse Log' if filepaths[4] != '' else ''
    filepaths[6] = eeg_files[1] if len(eeg_files) > 1 else ''
    filepaths[7] = 'EEG' if filepaths[6] != '' else ''

    return filepaths


def get_filepaths_SFR(sess_path, ltp_path, exp, subj):
    """
    Finds file paths for the JSON events and session log of an SFR session.

    :param sess_path: The path to the LTP directory for a specific ltpFR2 session.
    :param ltp_path: The path to the standard LTP directory on Rhino (/data/eeg/scalp/ltp).
    :param exp: The experiment name for the session ('SFR' vs 'FR1_scalp').
    :param subj: The subject ID for the session.
    :return: An 8-item list containing up to four file paths and their file types, to be filled into the spreadsheet.
    """
    events_file = glob.glob(os.path.join(sess_path, '*.json'))
    events_file = '' if len(events_file) == 0 else events_file[0]
    data_file = os.path.join(ltp_path, '%s/behavioral/data/beh_data__%s.json' % (exp, subj))

    filepaths = ['' for _ in range(8)]
    filepaths[0] = events_file
    filepaths[1] = 'Session Log'
    filepaths[2] = data_file if os.path.exists(data_file) else ''
    filepaths[3] = 'Behavioral' if filepaths[2] != '' else ''

    return filepaths


def get_filepaths_VFFR(sess_path, db_path):
    """
    Finds file paths for the EEG file(s) and JSON events file for a VFFR session. If events are not available, uses the
    session log instead.

    :param sess_path: The path to the LTP directory for a specific VFFR session.
    :param db_path: The path to the protocols directory for a specific VFFR session.
    :return: An 8-item list containing up to four file paths and their file types, to be filled into the spreadsheet.
    """
    eeg_files = glob.glob(os.path.join(db_path, 'ephys', 'current_processed', '*.bdf'))
    eeg_files = [''] if len(eeg_files) == 0 else eeg_files
    events_file = os.path.join(db_path, 'behavioral', 'current_processed', 'task_events.json')
    session_log = os.path.join(sess_path, 'session.jsonl')

    filepaths = ['' for _ in range(8)]
    filepaths[0] = eeg_files[0]
    filepaths[1] = 'EEG' if filepaths[0] != '' else ''
    filepaths[2] = events_file if os.path.exists(events_file) else session_log
    filepaths[3] = 'Behavioral' if os.path.exists(events_file) else 'Session Log'
    filepaths[4] = eeg_files[1] if len(eeg_files) > 1 else ''
    filepaths[5] = 'EEG' if filepaths[4] != '' else ''
    filepaths[6] = eeg_files[2] if len(eeg_files) > 2 else ''
    filepaths[7] = 'EEG' if filepaths[6] != '' else ''

    return filepaths
