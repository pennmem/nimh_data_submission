import os
import glob


def get_filepaths(info, ltp_path='/data/eeg/scalp/ltp/', protocols_path='/protocols/ltp/'):

    for i, sess_data in info.iterrows():

        # Identify session directories
        exp = sess_data.experiment
        subj = sess_data.subject
        sess = sess_data.session
        sess_path = os.path.join(ltp_path, exp, subj, '/session_' + sess)
        db_path = os.path.join(protocols_path, 'subjects', subj, 'experiments', exp, 'sessions', sess)

        # Determine the filepaths and file types for the current session
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
        pass

    return info


def get_filepaths_pyFR(sess_path):

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

    filepaths = ['' for _ in range(8)]

    return filepaths