import numpy as np
import pandas as pd

def create_excel_file_corrected(file1, file2, load_values, M1, M2):
    # Read the files
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()

    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    # Check the conditions
    if len(lines1) != len(lines2):
        raise ValueError("The number of lines in both files are not equal.")
    if len(lines1) != 5 * len(load_values):
        raise ValueError("The number of lines in the first file is not equal to five times the length of the load list.")

    # Create the dataframe
    df = pd.DataFrame(columns=['MidDisplacement', 'Rotation1', 'Rotation2', 'Load', 'M1', 'M2'])
    
    # Fill in the values from the files
    for i, (line1, line2) in enumerate(zip(lines1, lines2)):
        val1 = float(line1.strip().split()[-1])  
        val2, val3 = map(float, line2.strip().split()[0:2])
        df.loc[i] = [val1, val2, val3, None, None, None]
    
    # Fill in the load values
    for i, load in enumerate(load_values):
        df.at[5 * i + 4, 'Load'] = np.abs(load)
    for i, M1v in enumerate(M1):
        df.at[5 * i + 4, 'M1'] = np.abs(M1v)
    for i, M2v in enumerate(M2):
        df.at[5 * i + 4, 'M2'] = np.abs(M2v)
        
    # Interpolate the load values
    #df['Load'].iloc[0] = 0
    df['Load'] = df['Load'].interpolate()
    df['M1'] = df['M1'].interpolate()
    df['M2'] = df['M2'].interpolate()
    
    df['Load'].iloc[0] = df['Load'].iloc[4]/5
    df['Load'].iloc[1] = df['Load'].iloc[4]/5*2
    df['Load'].iloc[2] = df['Load'].iloc[4]/5*3
    df['Load'].iloc[3] = df['Load'].iloc[4]/5*4
    
    df['M1'].iloc[0] = df['M1'].iloc[4]/5
    df['M1'].iloc[1] = df['M1'].iloc[4]/5*2
    df['M1'].iloc[2] = df['M1'].iloc[4]/5*3
    df['M1'].iloc[3] = df['M1'].iloc[4]/5*4
    
    df['M2'].iloc[0] = df['M2'].iloc[4]/5
    df['M2'].iloc[1] = df['M2'].iloc[4]/5*2
    df['M2'].iloc[2] = df['M2'].iloc[4]/5*3
    df['M2'].iloc[3] = df['M2'].iloc[4]/5*4
    
    if df['Load'].gt(0).sum() > df['Load'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['Load'] = df['Load']*factor
    
    if df['M1'].gt(0).sum() > df['M1'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['M1'] = df['M1']*factor
    
    if df['M2'].gt(0).sum() > df['M2'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['M2'] = df['M2']*factor
    
    if df['MidDisplacement'].gt(0).sum() > df['MidDisplacement'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['MidDisplacement'] = df['MidDisplacement']*factor
    
    if df['Rotation1'].gt(0).sum() > df['Rotation1'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['Rotation1'] = df['Rotation1']*factor
    
    if df['Rotation2'].gt(0).sum() > df['Rotation2'].lt(0).sum():
        factor = 1
    else:
        factor = -1
    df['Rotation2'] = df['Rotation2']*factor

    # Save to Excel
    output_file_reordered = "collected_data.xlsx"
    df.to_excel(output_file_reordered, index=False)
    
    return output_file_reordered

# Test the corrected function
load_list = [-2683.624889, -3483.778412, -4064.839957, -4653.543564, -5679.360585, -6865.088651, -8042.045414, -8926.916147, -9463.329092, -9640.139054, -10655.186, -11387.28409]
M1_list = [9241.35812068326, 11398.64252888241, 13630.713745235502, 15634.219601912813, 19543.021215467892, 25418.36198277987, 28748.666342988105, 33351.81025315735, 35199.51274512394, 36345.2607338425, 17189.406244941005, -4140.876138467681]
M2_list = [-8841.296054743936, -11955.246314087814, -14440.978646630907, -16059.463428603409, -20561.91495280287, -26410.76740999839, -30271.09191198639, -34757.5224195502, -36914.18327351163, -36659.404799974436, -55172.8656253011, -76048.00791423014]
output_file_corrected = create_excel_file_corrected('MidDisplacement.out', 'rotations.txt', load_list, M1_list, M2_list)
output_file_corrected

