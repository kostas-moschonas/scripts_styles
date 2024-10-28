import pandas as pd
import os
import re

def import_from_1cmr(relative_file_path,
                     df_name=None,
                     output_path=None):
    """
    Imports separate CSV files from 1CMR output, cleans them,
    and combines them into a single dataset. 
    Valid on 1CMR output on 15/09/2024

    Args:
      relative_file_path: The relative path to the directory containing the CSV files.
      df_name: The desired name for the output DataFrame.
               Defaults to "volumes_df".
      output_path: The path where the combined DataFrame will be saved
                   as a CSV file in the working directory.
                   Defaults to "<df_name>.csv".

    Returns:
      None. Saves the combined DataFrame to a CSV file.
    """

    if df_name is None:
        df_name = "volumes_df"
    if output_path is None:
        output_path = f"{df_name}.csv"

    file_pattern = "^MHCM\\d+.*\\.csv$"  # Regular expression for file pattern
    csv_files = [f for f in os.listdir(relative_file_path) if re.match(file_pattern, f)]

    data_list = []
    for file in csv_files:
        path = os.path.join(relative_file_path, file)
        df = pd.read_csv(path)
        df['Scan_Date'] = pd.to_numeric(df['Scan_Date'])
        df['Analysis_Date'] = pd.to_numeric(df['Analysis_Date'])
        data_list.append(df)

    combined_df = pd.concat(data_list, ignore_index=True)

    combined_df = combined_df.drop(columns=[
        'Patient_ID',
        'Patient_DoB', 'LGE', 'Cardiac_Native_T1', 'Cardiac_ECV',
        'Liver_Native_T1', 'Liver_ECV', 'Spleen_Native_T1', 'Spleen_ECV', 'T2'
    ])

    combined_df['Scan_Date'] = pd.to_datetime(combined_df['Scan_Date'], format='%Y%m%d')
    combined_df['Analysis_Date'] = pd.to_datetime(combined_df['Analysis_Date'], format='%Y%m%d')

    combined_df = combined_df.rename(columns={
        'Patient_Name': 'record_id',
        'Scan_Date': 'date_cmr',
        'Analysis_Date': 'date_analysis',
        'LVEDV': 'lvedv',
        'LVESV': 'lvesv',
        'LVSV': 'sv',
        'LVEF': 'lvef',
        'LVM_Mass': 'mass',
        'MWT': 'mwt',
        'LV_Length': 'lv_length',
        'trLVEDV': 'lvedv_tr',
        'trLVESV': 'lvesv_tr',
        'trLVSV': 'sv_tr',
        'trLVEF': 'lvef_tr',
        'trLVM_Mass': 'mass_tr',
        'RVEDV': 'rvedv',
        'RVESV': 'rvesv',
        'RVSV': 'rvsv',
        'RVEF': 'rvef',
        'MAPSE_Lat': 'mapse_lat',
        'MAPSE_Sep': 'mapse_sep',
        'TAPSE': 'tapse',
        'LA_Area': 'la_area',
        'RA_Area': 'ra_area'
    })

    combined_df.to_csv(output_path, index=False)