import os
import pandas as pd
import numpy as np

import pandas as pd

def process_file_specific(file_path, output_folder):
    # Attempt to detect and use the correct encoding
    encoding_to_try = ['utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
    
    header_content = []
    for encoding in encoding_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                # Assuming header is the first 9 lines plus the column names line
                for _ in range(10):
                    header_content.append(file.readline())
            # If successfully read the header, break the loop
            break
        except UnicodeDecodeError:
            # If an error is encountered, try the next encoding
            continue
    
    header_str = ''.join(header_content)
    
    # Now read the data with pandas using the successful encoding
    try:
        df = pd.read_csv(file_path, skiprows=9, header=None,
                         names=['id', 'x', 'y', 'z', 'unrolled_length', 'x2', 'y2', 'z2'],
                         na_values=['', ' ', '!!! MULTIPLE VALUES'],
                         encoding=encoding)
    except UnicodeDecodeError as e:
        print(f"Failed to read {file_path} with encoding {encoding}: {e}")
        return  # Skip this file or handle error appropriately
    
    # Process the data
    # Assuming the data structure is known and consistent with the example provided
    df = pd.read_csv(file_path, skiprows=9, header=None,
                     names=['id', 'x', 'y', 'z', 'unrolled_length', 'x2', 'y2', 'z2'],
                     na_values=['', ' ', '!!! MULTIPLE VALUES'])
    
    # Step 1: Copy "x", "y", "z" if "F", "G", "H" are blank or not numeric
    for col_target, col_source in zip(['x2', 'y2', 'z2'], ['x', 'y', 'z']):
        df[col_target] = pd.to_numeric(df[col_target], errors='coerce').fillna(df[col_source])
    
    # Step 2: Adjust "id" and "unrolled_length" as required
    for i in range(1, len(df)):
        if pd.notna(df.loc[i, 'id']) and df.loc[i, 'id'] == df.loc[i-1, 'id']:
            df.loc[i, 'id'] = 500 + df.loc[i-1, 'id']
            df.loc[i, 'unrolled_length'] = 150 + df.loc[i-1, 'unrolled_length']
    
    # Step 3: Sort by "unrolled_length"
    df_sorted = df.sort_values(by='unrolled_length', ascending=True)
    
    # Save the processed data
    output_file_path = os.path.join(output_folder, f"processed_{os.path.basename(file_path)}")
    with open(output_file_path, 'w', encoding='utf-8') as outfile:  # Ensure output is UTF-8
        outfile.write(header_str)
        df.to_csv(outfile, index=False, header=False)

# Directory containing the files
input_folder = '/home/chenting/ProgrammingCode(NewOnly)/ExpResultConvert/L150d8_5T50-Curves'
output_folder = '/home/chenting/ProgrammingCode(NewOnly)/ExpResultConvert/L150d8_5T50-CurvesR'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all files in the folder
file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# Process each file
for file_path in file_paths:
    process_file_specific(file_path, output_folder)

