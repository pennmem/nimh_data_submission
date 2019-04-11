def write_info(ed, eeg_details_path, ed_col_order, esf, eeg_sub_files_path, esf_col_order):
    """
    Writes the eeg_details01.csv and eeg_sub_files01.csv files using the information in the provided data frames.

    :param ed: A data frame containing the complete eeg_details01 information.
    :param eeg_details_path: The path at which to save the eeg_details01 spreadsheet.
    :param ed_col_order: A list containing the proper ordering of the eeg_details01 columns.
    :param esf: A data frame containing the complete eeg_sub_files01 information.
    :param eeg_sub_files_path: The path at which to save the eeg_sub_files01 spreadsheet
    :param esf_col_order: A list containing the proper ordering of the eeg_sub_files01 columns.
    :return: None
    """
    # Write data frame to spreadsheet and add eeg_details header back on
    ed.to_csv(eeg_details_path, index=False, columns=ed_col_order)
    with open(eeg_details_path, 'r+') as f:
        s = f.readlines()
        top_header = 'eeg_details,1' + ',' * (s[1].count(',') - 1) + '\n'
        s.insert(0, top_header)
        f.seek(0)
        f.writelines(s)

    # Write data frame to spreadsheet and add eeg_sub_files header back on
    esf.to_csv(eeg_sub_files_path, index=False, columns=esf_col_order)
    with open(eeg_sub_files_path, 'r+') as f:
        s = f.readlines()
        top_header = 'eeg_sub_files,1' + ',' * (s[1].count(',') - 1) + '\n'
        s.insert(0, top_header)
        f.seek(0)
        f.writelines(s)
