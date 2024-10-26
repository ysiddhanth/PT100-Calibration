import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# Load training and validation data
data = np.genfromtxt('training_data.txt', delimiter=' ')
data1 = np.genfromtxt('validation_data.txt', delimiter=' ')
temperature, voltage = data[:, 0], data[:, 1]
vtemperature, vvoltage = data1[:, 0], data1[:, 1]

# Denoise temperature data using Random Forest
denoise_model = RandomForestRegressor(n_estimators=1000, random_state=0)
denoise_model.fit(voltage.reshape(-1, 1), temperature)
temperature_denoised = denoise_model.predict(voltage.reshape(-1, 1))
vtemperature_denoised = denoise_model.predict(vvoltage.reshape(-1, 1))
# Perform Least Squares Polynomial Fit on denoised temperature data
X_train = np.vstack([np.ones(voltage.shape), temperature_denoised, temperature_denoised**2]).T
coefficients = np.linalg.lstsq(X_train, voltage, rcond=None)[0]

# Generate predictions for plotting
x_vals = np.linspace(min(temperature_denoised), max(temperature_denoised), 100)
y_vals = coefficients[0] + coefficients[1] * x_vals + coefficients[2] * x_vals**2

# Validation predictions
X_val = np.vstack([np.ones(vvoltage.shape), vtemperature_denoised, vtemperature_denoised**2]).T
y_val = X_val @ coefficients
print(coefficients)
realcoefficients = (5*coefficients/1023)
print(realcoefficients[0])
print(realcoefficients[1]/realcoefficients[0])
print(realcoefficients[2]/realcoefficients[0])
# Plot Training Data with Denoised Temperature and Polynomial Fit
plt.figure(figsize=(10, 6))
plt.plot(temperature, voltage, 'k.', label='Noisy Training Data')
plt.plot(temperature_denoised, voltage, 'b.', label='Denoised Training Data')
plt.plot(x_vals, y_vals, 'r-', label='Least Squares Polynomial Fit')
plt.xlabel('Denoised Temperature (°C)')
plt.ylabel('Analog Input (A0)')
plt.legend()
plt.grid(True)
plt.title('Training Data with Least Squares Polynomial Fit')
plt.savefig('../figs/train_fit.png')
plt.show()

# Plot Validation Data with Denoised Temperature and Polynomial Fit
plt.figure(figsize=(10, 6))
plt.plot(vtemperature, vvoltage, 'k.', label='Noisy Validation Data')
plt.plot(vtemperature_denoised, vvoltage, 'b.', label='Denoised Validation Data')
plt.plot(x_vals, y_vals, 'r-', label='Least Squares Fit (Validation)')
plt.xlabel('Denoised Temperature (°C)')
plt.ylabel('Analog Input (A0)')
plt.legend()
plt.grid(True)
plt.title('Validation Data with Least Squares Polynomial Fit')
plt.savefig('../figs/valid_fit.png')
plt.show()

