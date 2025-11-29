# Claude-Light Quick Reference

## API Basics

### Endpoint
```
https://claude-light.cheme.cmu.edu/api
```

### Simple Request
```python
import requests

resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                   params={'R': 0.5, 'G': 0.3, 'B': 0.8})
data = resp.json()
```

### Parameters
- `R`: 0.0 to 1.0 (red LED)
- `G`: 0.0 to 1.0 (green LED)
- `B`: 0.0 to 1.0 (blue LED)

### Response Structure
```python
{
    'R': 0.5, 'G': 0.3, 'B': 0.8,
    'out': {
        '415nm': value,
        '445nm': value,
        '480nm': value,
        '515nm': value,
        '555nm': value,
        '590nm': value,
        '630nm': value,
        '680nm': value,
        'clear': value,
        'nir': value
    }
}
```

## Common Patterns

### Single Measurement
```python
resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                   params={'R': 0.5, 'G': 0, 'B': 0})
intensity = resp.json()['out']['630nm']
```

### Repeated Measurements
```python
measurements = []
for i in range(10):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0.5, 'G': 0.5, 'B': 0.5})
    measurements.append(resp.json()['out']['515nm'])
```

### Sweep Single Variable
```python
import numpy as np

R_values = np.linspace(0, 1, 11)
outputs = []

for R in R_values:
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': 0, 'B': 0})
    outputs.append(resp.json()['out']['630nm'])
```

### Grid Sampling
```python
for R in [0, 0.5, 1]:
    for G in [0, 0.5, 1]:
        for B in [0, 0.5, 1]:
            resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                               params={'R': R, 'G': G, 'B': B})
            data = resp.json()
            # Process data
```

### All Spectral Channels
```python
resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                   params={'R': 0.5, 'G': 0.5, 'B': 0.5})
spectrum = resp.json()['out']

for wavelength, intensity in spectrum.items():
    print(f"{wavelength}: {intensity}")
```

## Statistics

### Basic Statistics
```python
import numpy as np

# Mean and std dev
mean = np.mean(measurements)
std = np.std(measurements)

# Confidence interval (95%)
ci = np.percentile(measurements, [2.5, 97.5])

# Median
median = np.median(measurements)
```

### Histogram
```python
import matplotlib.pyplot as plt

plt.hist(measurements, bins=20)
plt.xlabel('Intensity')
plt.ylabel('Count')
plt.show()
```

## Regression

### Linear Regression
```python
from scipy.stats import linregress

slope, intercept, r_value, p_value, std_err = linregress(x, y)
print(f"R² = {r_value**2:.4f}")
```

### Polynomial Fit
```python
import numpy as np

coefficients = np.polyfit(x, y, degree=2)
poly_func = np.poly1d(coefficients)
predictions = poly_func(x_new)
```

### sklearn Linear Model
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X.reshape(-1, 1), y)
predictions = model.predict(X_new.reshape(-1, 1))
```

### Multivariate Regression
```python
from sklearn.linear_model import LinearRegression

# X is (n_samples, n_features)
model = LinearRegression()
model.fit(X, y)

print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")
print(f"R² score: {model.score(X, y):.4f}")
```

## Optimization

### Scipy Minimize
```python
from scipy.optimize import minimize

def objective(inputs):
    R, G, B = np.clip(inputs, 0, 1)
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    actual = resp.json()['out']['515nm']
    target = 30000
    return (actual - target)**2

result = minimize(objective, [0.5, 0.5, 0.5],
                 bounds=[(0, 1), (0, 1), (0, 1)])
print(f"Optimal: {result.x}")
```

### Grid Search
```python
best_error = float('inf')
best_params = None

for R in np.linspace(0, 1, 10):
    for G in np.linspace(0, 1, 10):
        resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                           params={'R': R, 'G': G, 'B': 0})
        actual = resp.json()['out']['515nm']
        error = abs(actual - target)

        if error < best_error:
            best_error = error
            best_params = (R, G)
```

## Machine Learning

### Random Forest
```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
```

### Neural Network
```python
from sklearn.neural_network import MLPRegressor

model = MLPRegressor(hidden_layer_sizes=(50, 30), max_iter=1000)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print(f"Mean score: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## Design of Experiments

### Latin Hypercube
```python
from scipy.stats import qmc

sampler = qmc.LatinHypercube(d=3)  # 3 dimensions
samples = sampler.random(n=20)
samples = qmc.scale(samples, [0, 0, 0], [1, 1, 1])

for R, G, B in samples:
    # Run experiment
    pass
```

### Factorial Design
```python
from itertools import product

levels = [0, 0.5, 1]
experiments = list(product(levels, repeat=3))

for R, G, B in experiments:
    # Run experiment
    pass
```

## Visualization

### Plot Spectrum
```python
import matplotlib.pyplot as plt

wavelengths = [415, 445, 480, 515, 555, 590, 630, 680]
intensities = [data['out'][f'{wl}nm'] for wl in wavelengths]

plt.plot(wavelengths, intensities, 'o-')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.show()
```

### Plot Response Curve
```python
plt.plot(R_values, outputs, 'o-')
plt.xlabel('R Input')
plt.ylabel('Output at 630nm')
plt.grid(True)
plt.show()
```

### Scatter Plot
```python
plt.scatter(predictions, actual)
plt.plot([0, max(actual)], [0, max(actual)], 'r--')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
```

## Data Management

### Save to CSV
```python
import pandas as pd

df = pd.DataFrame(experiments)
df.to_csv('experiments.csv', index=False)
```

### Load from CSV
```python
df = pd.read_csv('experiments.csv')
X = df[['R', 'G', 'B']].values
y = df['output'].values
```

### Save to JSON
```python
import json

with open('data.json', 'w') as f:
    json.dump(experiments, f, indent=2)
```

### Pickle Objects
```python
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

## Utility Functions

### Background Subtraction
```python
def get_background():
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0, 'G': 0, 'B': 0})
    return resp.json()['out']

bg = get_background()

def corrected_measurement(R, G, B):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()
    return {wl: data['out'][wl] - bg[wl] for wl in data['out']}
```

### Averaging
```python
def averaged_measurement(R, G, B, n=5):
    measurements = []
    for _ in range(n):
        resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                           params={'R': R, 'G': G, 'B': B})
        measurements.append(resp.json()['out'])

    avg = {}
    for wl in measurements[0]:
        avg[wl] = np.mean([m[wl] for m in measurements])
    return avg
```

### Error Handling
```python
def safe_experiment(R, G, B, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                               params={'R': R, 'G': G, 'B': B},
                               timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == retries - 1:
                raise
            continue
```

## Metrics

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```

### Residual Analysis
```python
residuals = y_true - y_pred

plt.scatter(y_pred, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.show()
```

## Tips

- Always clip inputs to [0, 1] range
- Use `timeout` parameter in requests
- Cache results to avoid redundant calls
- Average multiple measurements for noise reduction
- Perform background subtraction
- Validate models on held-out data
- Visualize before modeling
- Check for nonlinear relationships
