import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

directory = "/home/chenting/ProgrammingCode(NewOnly)/ExpResultConvert/L200e3_8T50-Curves"
length = 200.0
TxtFileName = "ExpResultsCurves.txt"
InflectionPointsName = "ExpInflectionPoints.txt"
plotdiagrams = True

outputw = open(directory + "/" + TxtFileName, 'w')
switch = 0
countn = 0
fnsavelist = []
InfPointsFile = open(directory + "/" + InflectionPointsName, 'w')

def extract_float_from_filename_corrected(filename):
    """Corrected function to extract the floating number from the filename based on the given pattern."""
    pattern = r'_(\d+(\.\d+)?)\s*s\.csv$'
    match = re.search(pattern, filename)
    if match:
        return float(match.group(1))
    return None
    
def read_load_value(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return float(lines[6].split(",")[0])

def process_csv_file(file_path, length):
    global outputw
    global switch
    global fnsavelist
    global InfPointsFile
    # Import data with multiple possible delimiters
    data = pd.read_csv(file_path, sep=r'[ ,;\t]', engine='python', skiprows=8)
    
    # Extracting the relevant columns
    data = data[['x', 'y', 'z', 'unrolled_length']]
    
    # Convert to numeric and sort by 'unrolled_length'
    for col in ['x', 'y', 'z', 'unrolled_length']:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.sort_values(by='unrolled_length', ascending=True)
    
    # Extract point data
    points = data[['x', 'y', 'z']].to_numpy()

    # Fit the plane
    A = np.c_[points[:, 0], points[:, 1], np.ones(points.shape[0])]
    C, _, _, _ = np.linalg.lstsq(A, points[:, 2], rcond=None)
    normal = np.array([C[0], C[1], -1])
    normal /= np.linalg.norm(normal)

    # Calculate the rotation matrix to align the normal with the Z-axis
    axis = np.cross([0, 0, 1], normal)
    theta = np.arccos(np.dot(normal, [0, 0, 1]))
    axis = axis/np.linalg.norm(axis)
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * np.dot(K, K)
    rotated_points_new = points.dot(R.T)

    # Translate points so the first point is at the origin
    translated_points = rotated_points_new - rotated_points_new[0]
    
    # Rotate the translated points so the last point is on the X-axis
    angle = -np.arctan2(translated_points[-1, 1], translated_points[-1, 0])
    R2D = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
    aligned_points = translated_points[:, :2].dot(R2D.T)
    maxdisp = max(np.abs(aligned_points[:,1]))

    # Fit the aligned points to a 7th degree polynomial
    p = np.polyfit(aligned_points[:, 0], aligned_points[:, 1], 7)
    poly = np.poly1d(p)
    
    # Generate x values for plotting
    x_values = np.linspace(min(aligned_points[:, 0]), max(aligned_points[:, 0]), 500)
    y_values = poly(x_values)
    
    x_values1 = np.linspace(min(aligned_points[:, 0]), max(aligned_points[:, 0]), 21)
    y_values1 = poly(x_values1)
    
    if switch == 0:
    	switch = 1
    	outputw.write(' '.join(map(str, x_values1)))
    	outputw.write("\n")
    
    if max(np.abs(y_values1)) >= 0.2:
    	outputw.write(' '.join(map(str, y_values1)))
    	outputw.write("\n")
    	fnm = file_path.split('/')[-1]
    	fnsavelist.append(fnm)

    # Plotting
    if plotdiagrams:
        plt.figure(figsize=(10, 6))
        plt.plot(aligned_points[:, 0], aligned_points[:, 1], 'o', label='Data Points')
        plt.plot(x_values, y_values, 'r-', label='Fitted Curve')
        plt.title(f"Fitted Curve for {os.path.basename(file_path)}")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # Calculate the first derivative of the fitted polynomial
    poly_prime = poly.deriv()
    poly_curva = poly_prime.deriv()
    
    # Evaluate the first derivative at the first and last points
    derivative_first_point = poly_prime(aligned_points[0, 0])
    derivative_last_point = poly_prime(aligned_points[-1, 0])
    
    roots = np.roots(poly_curva)
    roots = roots.real[abs(roots.imag)<1e-5]
    roots = list(filter(lambda x: x >= 0 and x <= length, roots))
    
    if len(roots) == 0:
        InfPointsFile.write("N/A N/A\n")
    elif len(roots) == 1:
        if roots[0] < length/2:
            InfPointsFile.write("%f N/A\n"%roots[0])
        else:
            InfPointsFile.write("N/A %f\n"%roots[0])
    else:
        roots = sorted(roots)
        InfPointsFile.write("%f %f\n"%(roots[0], roots[1]))
    
    return [maxdisp, derivative_first_point, derivative_last_point, file_path]

                           
def sort_lists_based_on_first(main_list, *other_lists):
    # Combine the lists
    combined = list(zip(main_list, *other_lists))
    
    # Sort by the first list
    combined_sorted = sorted(combined, key=lambda x: x[0])
    
    # Unzip the combined sorted list
    sorted_lists = list(zip(*combined_sorted))
    
    return sorted_lists

def process_files_with_data_check(directory, length):
    all_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    files_with_numbers = [(f, extract_float_from_filename_corrected(f)) for f in all_files]
    valid_files = [(f, n) for f, n in files_with_numbers if n is not None]
    sorted_files = sorted(valid_files, key=lambda x: x[1])
    
    results = []
    skipped_files_data = []
    load_values = {}
    
    for f, n in sorted_files:
        file_path_current = os.path.join(directory, f)
        try:
            load_values[f] = read_load_value(file_path_current)
            results.append(process_csv_file(file_path_current, length))
        except Exception as e:
            skipped_files_data.append(f)
            continue
    
    skipped_files_pattern = [f for f, n in files_with_numbers if n is None]
    all_skipped_files = list(set(skipped_files_pattern + skipped_files_data))
    
    return results, all_skipped_files, load_values

# ============ Main Program ====================
results_ordered_updated, skipped_files_list_updated, load_values_updated = process_files_with_data_check(directory, length)

print("Skipped files are listed below")
print(skipped_files_list_updated)

# Organize the data into a pandas DataFrame
df_results = pd.DataFrame({
    'File Name': [result[3] for result in results_ordered_updated],
    'maxdisp': [result[0] for result in results_ordered_updated],
    'derivative_first_point': [result[1] for result in results_ordered_updated],
    'derivative_last_point': [result[2] for result in results_ordered_updated],
    'Load Value': [load_values_updated[os.path.basename(result[3])] for result in results_ordered_updated]
})

outputw.close()

# Specify the path for the Excel output
output_file_path = os.path.join(directory, "processed_results.xlsx")

# Export the DataFrame to an Excel file
df_results.to_excel(output_file_path, index=False)

loadlist = list(load_values_updated.values())
filem = open(directory + "/" + TxtFileName, 'r')
lines = filem.readlines()

# Step 2: Prepend each number from 'a' to the corresponding line
lines[0] = "Location " + lines[0]
for i, obj in enumerate(fnsavelist):
    lines[i+1] = str(load_values_updated[str(obj)]) + " " + lines[i+1]

# Step 3: Write the modified lines back to the txt file
with open(directory + "/" + TxtFileName, 'w') as file:
    file.writelines(lines)

InfPointsFile.close()
print(f"Results have been saved to: {output_file_path}")

        

