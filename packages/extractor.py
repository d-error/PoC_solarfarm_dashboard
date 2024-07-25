import pandas as pd




def extract_from_caleb_excel(path):
    cols_range = "K:KCF"
    sheet_name = "tracker data"

    raw_tracker_data = pd.read_excel(
        path, 
        usecols=cols_range, 
        skiprows=1, 
        sheet_name=sheet_name, 
        na_values=['NA', 'n/a']
        ).dropna(subset='Timestamp')
    return raw_tracker_data