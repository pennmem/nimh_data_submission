def write_info(ed, eeg_details_path, ed_col_order, esf, eeg_sub_files_path, esf_col_order):

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
