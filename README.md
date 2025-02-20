# Integrated Rate Law Analyzer

This simple Python script automates the analysis of chemical kinetics by determining the reaction order (zero, first, or second order) based on provided time and concentration data. It applies integrated rate law transformations and performs linear regression on each possibility and selects the best model (highest R² value) to calculate the reaction rate constant k. Results are viewed both in the console and as a matplotlib plot.

## Features

- **User Input Guide:**  
  !! Accepts space-separated time values (seconds) and concentration values (mol/L).

  example: **Enter time values (in seconds) separated by spaces: 0 50 100 150 200 250**

  !! Supports only dot (`.`) as decimal separator !!!!

  example: **Enter concentration values (in mol/L) separated by spaces: 10.0 7.80 6.05 4.72 3.68 2.86**

- **Model Testing:**  
  Automatically tests zero, first, and second-order reaction models using the integrated rate laws:
  - **Zero Order:** \([A]\) vs. time 
  - **First Order:** \(ln[A]\) vs. time 
  - **Second Order:** \(1/[A]\) vs. time 

- **Best-Fit Determination:**  
  Chooses the reaction order with the highest coefficient of determination (R²).

- **Results**  
  - **On console:** Displays the determined reaction order, slope, rate constant \( k \) (with appropriate units), and R².
  - **On plot:** Generates a matplotlib graph showing the transformed data and best-fit line, with a legend including the slope, \( k \), and R².

