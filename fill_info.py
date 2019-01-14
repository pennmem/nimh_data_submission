import pandas as pd


def fill_info(ed, esf, info):

    ed = fill_eeg_details(ed, info)
    esf = fill_eeg_sub_files(esf, info)

    return ed, esf


def fill_eeg_details(ed, info):

    ed = ed.append(pd.DataFrame(None, index=info.index))
    ed.loc[:, 'subjectkey'] = info.subjectkey  # Subject GUID
    ed.loc[:, 'src_subject_id'] = info.subject  # Subject ID
    ed.loc[:, 'interview_date'] = info.date  # Session date (MM/DD/YYYY)
    ed.loc[:, 'interview_age'] = info.age_in_months  # Participant's age in months
    ed.loc[:, 'gender'] = info.gender  # Participant's gender
    ed.loc[:, 'site'] = info.location  # Session location
    ed.loc[:, 'visit'] = info.session  # Session number
    ed.loc[:, 'eeg001'] = 1  # 1 if EEG was used, 0 if no EEG
    ed.loc[:, 'eeg003b'] = info.hand_throw  # Handedness for throwing a ball (1-5)
    ed.loc[:, 'eeg003d'] = info.hand_toothbrush # Handedness for brushing teeth (1-5)
    ed.loc[:, 'eeg003e'] = info.hand_scissors  # Handedness for using scissors (1-5)
    ed.loc[:, 'eeg003g'] = info.hand_write  # Handedness for writing (1-5)
    ed.loc[:, 'eeg008c'] = info.sleep  # Hours of sleep
    ed.loc[:, 'eeg008d'] = info.alertness  # Alertness (1-5)
    ed.loc[:, 'eeg013'] = info.start_time  # Start time of EEG recording
    ed.loc[:, 'head_circum'] = info.head_circum  # Participant's head circumference (in cm)
    ed.loc[:, 'eeg015'] = info.cap_size  # Size of cap used (PM, PL, AS, AM, AML, AL, AXL)
    ed.loc[:, 'eeg022'] = info.end_time  # End time of EEG recording
    ed.loc[:, 'eeg026'] = 0  # 1 if task included faces, 0 if not
    ed.loc[:, 'eeg027'] = 0  # 1 if task involved resting with eyes closed, 0 if not
    ed.loc[:, 'eeg028'] = 0  # 1 if a cognitive flanker task, 0 if not
    ed.loc[:, 'eeg029'] = 0  # 1 if task involved resting with eyes open, 0 if not
    ed.loc[:, 'eeg_4'] = 1  # 1 if participant had normal or correct-to-normal vision

    return ed


def fill_eeg_sub_files(esf, info):

    esf = esf.append(pd.DataFrame(None, index=info.index))
    esf.loc[:, 'subjectkey'] = info.subjectkey  # Subject GUID
    esf.loc[:, 'src_subject_id'] = info.subject  # Subject ID
    esf.loc[:, 'interview_date'] = info.date  # Session date (MM/DD/YYYY)
    esf.loc[:, 'interview_age'] = info.age_in_months  # Participant's age in months
    esf.loc[:, 'gender'] = info.gender  # Participant's gender
    esf.loc[:, 'ofc'] = info.head_circum  # Participant's head circumference (in cm)
    esf.loc[:, 'experiment_id'] = info.experiment_id  # Experiment's ID number
    esf.loc[:, 'data_file1'] = info.data_file1  # Data file 1 (typically EEG recording)
    esf.loc[:, 'data_file1_type'] = info.data_file1_type  # File type of file 1 (typically "EEG")
    esf.loc[:, 'data_file2'] = info.data_file2  # Data file 2 (typically events file or session log)
    esf.loc[:, 'data_file2_type'] = info.data_file2_type  # File type of file 2 (typically "Behavioral")
    esf.loc[:, 'data_file3'] = info.data_file3  # Data file 3 (extra file, e.g. sync pulse log or second EEG recording)
    esf.loc[:, 'data_file3_type'] = info.data_file3_type  # File type of file 3
    esf.loc[:, 'data_file4'] = info.data_file4  # Data file 4 (extra file, e.g. sync pulse log or second EEG recording)
    esf.loc[:, 'data_file4_type'] = info.data_file4_type  # File type of file 4
    esf.loc[:, 'head_circum'] = info.head_circum  # Participant's head circumference (in cm)
    esf.loc[:, 'visit'] = info.session  # Session number

    return esf
