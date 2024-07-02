import os
from scipy.optimize import minimize

# OpenSees original file
fn = "ColumnBucklingSectionFullDispLoads.tcl"

# OpenSees new file
fnr = "ColumnBucklingSectionFullDispLoads-r.tcl"

# How many values do you have in time list (or load list)?
LengthList = 12

# ========================= Begin here ==================================================
ic = 0
def modify_tcl_script(input_filename, output_filename, num_values, M1_value, M2_value):
    global ic
    # Read the input TCL file
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    # Modify the script lines
    modified_lines = []
    for line in lines:
        # Check if the line is one of the specific list definitions
        if line.startswith(("set timelist", "set loadlist", "set M1", "set M2")):
            # Split each line by space
            parts = line.split(maxsplit=2)  # Splitting only into 3 parts
            
            # Take the desired number of values from the list enclosed in quotes
            current_values = parts[2].replace('"', '').split()
            selected_values = " ".join(current_values[:num_values])
            
            # Update the value for M1 or M2 if the line corresponds to them
            if line.startswith("set M1"):
                selected_values = selected_values.split()
                selected_values[num_values - 1] = str(M1_value)
                selected_values = " ".join(selected_values)
            elif line.startswith("set M2"):
                selected_values = selected_values.split()
                selected_values[num_values - 1] = str(M2_value)
                selected_values = " ".join(selected_values)
            
            if line.startswith(("set loadlist")):
                maxload = float(selected_values.split()[-1])
            
            # Construct the modified line using updated values
            modified_line = f'{parts[0]} {parts[1]} "{selected_values}"'
            modified_lines.append(modified_line)
            
            if 'timelist' in line:
                new_time_value = int(float(selected_values.split()[-1]))  # Store the last value of selected values for timetotal as integer
        elif "set timetotal" in line:
            # Modify the timetotal line
            modified_lines.append(f'set timetotal {new_time_value}')
            timetotal = new_time_value
        else:
            # Keep the original line
            modified_lines.append(line.strip())

    # Write the modified content to the output TCL file
    with open(output_filename, 'w') as f:
        f.write("\n".join(modified_lines))
    return [timetotal, maxload]

def compute_squared_difference(input_file_disp, input_file_exp, line_number, target_load_value, tolerance=0.1):
    """
    Read values from NodeHorizontalDisp.out and ExpResultsCurves.txt files.
    Determine the absolute values of the two lists.
    Compute the sum of squared differences between the values of the two lists.
    Return the computed sum of squared differences.
    """
    
    # Extracting values from NodeHorizontalDisp.out
    with open(input_file_disp, 'r') as f:
        lines = f.readlines()
    disp_values = [float(val) for val in lines[line_number].split()[1:]]
    
    # Extracting matching values from ExpResultsCurves.txt
    with open(input_file_exp, 'r') as f:
        lines = f.readlines()
    for line in lines[1:]:  # Skipping the "Location" line
        values = line.split()
        load_value = float(values[0])
        if abs(abs(load_value) - abs(target_load_value)) < tolerance:
            exp_values = [float(val) for val in values[1:]]
            break
    else:
        exp_values = []
    
    # Compute absolute values of the lists
    abs_disp_values = [abs(val) for val in disp_values]
    abs_exp_values = [abs(val) for val in exp_values]
    
    # Compute the sum of squared differences
    diff = [d - e for d, e in zip(abs_disp_values, abs_exp_values)]
    sum_of_squares = sum([d**2 for d in diff])
    
    return sum_of_squares

def trymoment(fn, fnr, FEresult, Expresult, num_values, M1try, M2try):
    timetotal, maxload = modify_tcl_script(fn, fnr, num_values, M1try, M2try)
    p1 = os.system("../OpenSees ColumnBucklingSectionFullDispLoads-r.tcl")
    if p1 == 0:
        squared_difference = compute_squared_difference(FEresult, Expresult, timetotal-1, maxload, tolerance=0.1)
        return squared_difference
    else:
        return 99999
        
def modify_M1_M2(input_filename, output_filename, i, a, b):
    """
    Modify the i-th value of lists M1 and M2 in a TCL file and save the revised content to a new file.
    
    Parameters:
    - input_filename: Path to the original TCL file
    - output_filename: Path to the output (revised) TCL file
    - i: Index of the value to change (0-based index)
    - a: New value for the i-th element of M1
    - b: New value for the i-th element of M2
    """
    
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    # Modify the values of M1 and M2
    modified_lines = []
    for line in lines:
        if line.startswith("set M1"):
            parts = line.split(maxsplit=2)
            values = parts[2].replace('"', '').split()
            values[i] = str(a)
            modified_line = f'{parts[0]} {parts[1]} "{" ".join(values)}"'
            modified_lines.append(modified_line)
        elif line.startswith("set M2"):
            parts = line.split(maxsplit=2)
            values = parts[2].replace('"', '').split()
            values[i] = str(b)
            modified_line = f'{parts[0]} {parts[1]} "{" ".join(values)}"'
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line.strip())

    # Save the modified content to the output file
    with open(output_filename, 'w') as f:
        f.write("\n".join(modified_lines))



# Initial guess
initial_guess = [17000, -17000]

# Perform optimization

optimal_value = []
error_value = []
for ic in range(2, LengthList+1):
    def objective(params):
        M1try, M2try = params
        return trymoment(fn, fnr, "NodeHorizontalDisp.out", "ExpResultsCurves.txt", ic, M1try, M2try)
    result = minimize(objective, initial_guess, method='Nelder-Mead')
    print("Optimal values:", result.x)
    optimal_value.append(result.x)
    error_value.append(result.fun)
    modify_M1_M2(fn, fn, ic - 1, result.x[0], result.x[1])
    initial_guess = result.x

# Display the results
print("Optimal values:", optimal_value)
print("Errors:", error_value)


