import numpy as np
import matplotlib.pyplot as plt

# Define the generating function (simplified for numerical computation)
def bivariate_generating_function(z, q1, q2, q3, max_width):
    """
    Compute the generating function terms for a range of widths and area coefficients.
    Args:
        z: The width variable.
        q1, q2, q3: Coefficients for A_xy, A_yz, A_xz respectively.
        max_width: Maximum width to compute.

    Returns:
        A dictionary containing results for each width.
    """
    results = {}
    for n in range(max_width + 1):
        # For simplicity, assume contributions from the three areas scale with q1, q2, q3
        # This is a heuristic numerical approximation
        term = z**n * (q1**n + q2**n + q3**n)
        results[n] = term
    return results

# Parameters for the generating function
z = 0.5  # Width variable
q1, q2, q3 = 1.1, 1.05, 0.9  # Area coefficients for A_xy, A_yz, A_xz
max_width = 20  # Maximum width to compute

# Compute the results
results = bivariate_generating_function(z, q1, q2, q3, max_width)

# Extract values for plotting
widths = list(results.keys())
values = [np.real(results[w]) for w in widths]  # Take the real part for plotting

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(widths, values, marker='o', label="Generating Function Terms")
plt.title("Numerical Results from Bivariate Generating Function")
plt.xlabel("Width (n)")
plt.ylabel("Generating Function Value")
plt.grid()
plt.legend()
plt.show()

# Display numerical values for confirmation
for width, value in results.items():
    print(f"Width {width}: Generating Function Value = {value}")
