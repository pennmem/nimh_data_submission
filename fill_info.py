import pandas as pd

def fill_info(ed, esf, info):

    ed = ed.append(pd.DataFrame(None, index=info.index))
    esf = esf.append(pd.DataFrame(None, index=info.index))

    ed.loc[:, 'src_subject_id'] = info.subject
    esf.loc[:, 'src_subject_id'] = info.subject

    return ed, esf