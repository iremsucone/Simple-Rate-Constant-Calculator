import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def transform_data(time, concentration, order):
    """
    Transforms the concentration data based on the reaction order:
      - Order 0: [A] vs. time (slope = -k)
      - Order 1: ln[A] vs. time (slope = -k)
      - Order 2: 1/[A] vs. time (slope = k)
    """
    time = np.array(time)
    concentration = np.array(concentration)
    
    if order == 0:
        y = concentration
        ylabel = "[A] (M)"
        sign_factor = -1  # because slope = -k
    elif order == 1:
        if np.any(concentration <= 0):
            raise ValueError("All concentration values must be positive for ln[A].")
        y = np.log(concentration)
        ylabel = "ln[A]"
        sign_factor = -1  # because slope = -k
    elif order == 2:
        if np.any(concentration <= 0):
            raise ValueError("All concentration values must be positive for 1/[A].")
        y = 1 / concentration
        ylabel = "1/[A] (1/M)"
        sign_factor = 1   # because slope = k
    else:
        raise ValueError("Order must be 0, 1, or 2.")
    
    return time, y, ylabel, sign_factor

def determine_best_order(time, concentration):
    """
    Tests orders 0, 1, and 2, performs linear regression on the transformed data,
    and returns the order with the best (highest) R² value along with the regression details.
    """
    orders = [0, 1, 2]
    best_order = None
    best_r2 = -np.inf
    best_details = None  # will store tuple: (slope, intercept, transformed y, ylabel, sign_factor)
    
    for order in orders:
        try:
            t, y, ylabel, sign_factor = transform_data(time, concentration, order)
            slope, intercept, r_value, _, _ = linregress(t, y)
            r2 = r_value ** 2
            # Choose the order with the highest R²
            if r2 > best_r2:
                best_r2 = r2
                best_order = order
                best_details = (slope, intercept, y, ylabel, sign_factor)
        except Exception:
            # Skip this order if transformation fails
            continue
    
    if best_order is None:
        raise ValueError("Unable to fit any reaction order with the provided data.")
    
    return best_order, best_r2, best_details

def plot_best_fit(time, y, ylabel, slope, intercept, best_order, best_r2, sign_factor):
    """
    Plots the transformed data with its best-fit line and includes the rate constant k in the plot.
    """
    time = np.array(time)
    fit_line = intercept + slope * time
    # Calculate the rate constant based on the sign factor.
    rate_constant = sign_factor * slope
    plt.figure(figsize=(6,4))
    plt.scatter(time, y, color='blue', label='Data')
    plt.plot(time, fit_line, color='red', 
             label=f'Fit: slope = {slope:.4f}, k = {rate_constant:.4e}, R² = {best_r2:.4f}')
    plt.xlabel("Time (s)")
    plt.ylabel(ylabel)
    plt.title(f"Integrated Rate Law Fit (Order {best_order})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Print the analysis results to the console.
    print(f"Determined Reaction Order: {best_order}")
    print(f"Slope value: {slope:.4f}")
    print(f"Rate constant k = {rate_constant:.4e}")
    print(f"R² = {best_r2:.4f}")

if __name__ == '__main__':
    # Get time and concentration values from user input.
    time_input = input("Enter time values (in seconds) separated by spaces: ").strip()
    conc_input = input("Enter concentration values (in mol/L) separated by spaces: ").strip()
    
    try:
        # Replace commas with dots to handle decimal separators and convert to float.
        time_data = list(map(lambda x: float(x.replace(',', '.')), time_input.split()))
        concentration_data = list(map(lambda x: float(x.replace(',', '.')), conc_input.split()))
        if len(time_data) != len(concentration_data):
            raise ValueError("The number of time points must match the number of concentration values.")
    except Exception as e:
        print(f"Input error: {e}")
        exit(1)
    
    try:
        best_order, best_r2, details = determine_best_order(time_data, concentration_data)
        slope, intercept, transformed_y, ylabel, sign_factor = details
        plot_best_fit(time_data, transformed_y, ylabel, slope, intercept, best_order, best_r2, sign_factor)
    except Exception as e:
        print(f"Error during analysis: {e}")
