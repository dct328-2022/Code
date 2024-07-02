import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt

def process_displacement_data_modified(filename, L, visualize=False):
    # Initialize an empty list to store the derivative values at x=0 and x=L
    derivatives = []
    
    # Open the file and read it line by line
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = [float(val) for val in line.strip().split()]
            # Ignore the first value as it is the time step
            y = np.array(values[1:])
            x = np.linspace(0, L, len(y))
            
            # Fit the data to a 7-degree polynomial
            p = Polynomial.fit(x, y, 7)
            
            # Find the derivative of the polynomial
            dp = p.deriv()
            
            # Evaluate the derivative at x=0 and x=L
            deriv_at_0 = dp(0)
            deriv_at_L = dp(L)
            
            # Append the values to the derivatives list
            derivatives.append((deriv_at_0, deriv_at_L))
            
            # Visualize the fitting result if required
            if visualize:
                plt.figure(figsize=(8, 6))
                plt.plot(x, y, 'o', label='Original Data')
                plt.plot(x, p(x), '-', label='Fitted Polynomial')
                plt.xlabel('Position along specimen (x)')
                plt.ylabel('Displacement (y)')
                plt.title('Original Data vs. Fitted Polynomial')
                plt.legend()
                plt.grid(True)
                plt.show()
    
    # Save the derivatives to a txt file
    output_filename = "rotations.txt"
    with open(output_filename, 'w') as f:
        for deriv_pair in derivatives:
            f.write(f"{deriv_pair[0]} {deriv_pair[1]}\n")
    
    return output_filename

# Call the modified function with the provided filename, a sample value for L, and visualization turned on
output_file_modified = process_displacement_data_modified("NodeHorizontalDisp.out", 101.23, visualize=True)

