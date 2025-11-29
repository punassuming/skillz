# Claude-Light Experimental Skill

Expert assistant for conducting remote experiments with Claude-Light - a web-accessible RGB LED and spectral sensor instrument for hands-on learning of statistics, regression, optimization, and experimental design.

## What This Skill Does

This skill enables Claude to help you:
- Design and conduct experiments with the Claude-Light remote instrument
- Perform statistical analysis of measurement data
- Build regression models (linear and nonlinear)
- Optimize inputs to achieve target outputs
- Apply design of experiments methodologies
- Use machine learning for prediction and modeling
- Quantify uncertainties in measurements and predictions
- Visualize experimental results

## What is Claude-Light?

Claude-Light is a Raspberry Pi-based remote laboratory instrument that:
- **Controls**: RGB LEDs with continuous inputs (R, G, B from 0 to 1)
- **Measures**: Light intensity across 10 spectral channels (8 wavelengths + clear + NIR)
- **Provides**: Web interface and REST API for remote access
- **Enables**: Hands-on experimental learning without physical hardware

**Key Features:**
- No special software installation required
- Accessible via web browser or Python
- Automatic logging of all experiments
- Camera documentation of LED states
- Multiple complexity levels (web forms → API → scripting)

## When to Use This Skill

Use this skill when you need to:
- Learn experimental methods and data science concepts
- Conduct statistical analysis of sensor data
- Build predictive models from experimental data
- Optimize system parameters
- Design efficient experiments
- Practice machine learning on real hardware
- Test regression and uncertainty quantification methods
- Develop Python skills with real API interactions

## Quick Start

### 1. Basic Requirements

```bash
# Minimal setup
pip install requests numpy pandas matplotlib

# Full analysis stack
pip install requests numpy pandas matplotlib scipy scikit-learn
```

### 2. Test the API

```python
import requests

# Send a simple experiment
response = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0.5, 'G': 0.3, 'B': 0.8})

# Get the results
data = response.json()
print(data)

# Access specific wavelength
print(f"515nm intensity: {data['out']['515nm']}")
```

### 3. Your First Experiment

```python
import requests
import numpy as np

# Measure red LED response
R_values = np.linspace(0, 1, 11)
red_outputs = []

for R in R_values:
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': 0, 'B': 0})
    data = resp.json()
    red_outputs.append(data['out']['630nm'])  # Red wavelength

# Simple analysis
print(f"Minimum: {min(red_outputs)}")
print(f"Maximum: {max(red_outputs)}")
print(f"Range: {max(red_outputs) - min(red_outputs)}")
```

## API Reference

### Endpoint

```
https://claude-light.cheme.cmu.edu/api
```

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| R | float | 0.0 - 1.0 | Red LED intensity |
| G | float | 0.0 - 1.0 | Green LED intensity |
| B | float | 0.0 - 1.0 | Blue LED intensity |

### Response Format

```json
{
  "R": 0.5,
  "G": 0.3,
  "B": 0.8,
  "out": {
    "415nm": 12345,
    "445nm": 15678,
    "480nm": 18901,
    "515nm": 22345,
    "555nm": 25678,
    "590nm": 28901,
    "630nm": 32345,
    "680nm": 35678,
    "clear": 45678,
    "nir": 8901
  }
}
```

### Spectral Channels

- **415nm** - Violet
- **445nm** - Blue
- **480nm** - Cyan
- **515nm** - Green
- **555nm** - Yellow-green
- **590nm** - Yellow
- **630nm** - Red
- **680nm** - Deep red
- **clear** - Total intensity across all wavelengths
- **nir** - Near-infrared

## Experimental Workflows

### 1. Statistics & Reproducibility

Test measurement precision by repeating experiments and calculating statistics.

```python
# Repeat measurement 30 times
measurements = []
for i in range(30):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0.5, 'G': 0.5, 'B': 0.5})
    measurements.append(resp.json()['out']['515nm'])

# Calculate statistics
import numpy as np
print(f"Mean: {np.mean(measurements):.2f}")
print(f"Std Dev: {np.std(measurements):.2f}")
```

### 2. Linear Regression

Map input-output relationships and build predictive models.

```python
from scipy.stats import linregress

# Collect data
R_values = np.linspace(0, 1, 11)
outputs = []
for R in R_values:
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': 0, 'B': 0})
    outputs.append(resp.json()['out']['630nm'])

# Fit model
slope, intercept, r_value, p_value, std_err = linregress(R_values, outputs)
print(f"R² = {r_value**2:.4f}")
```

### 3. Optimization

Find inputs that produce desired outputs.

```python
from scipy.optimize import minimize

def objective(inputs):
    R, G, B = np.clip(inputs, 0, 1)
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    actual = resp.json()['out']['515nm']
    target = 30000
    return (actual - target)**2

result = minimize(objective, [0.5, 0.5, 0.5], bounds=[(0,1), (0,1), (0,1)])
print(f"Optimal RGB: {result.x}")
```

### 4. Machine Learning

Use advanced models for prediction and analysis.

```python
from sklearn.ensemble import RandomForestRegressor

# Train model on collected data
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
```

### 5. Design of Experiments

Efficient sampling strategies for maximum information.

```python
from scipy.stats import qmc

# Latin hypercube sampling
sampler = qmc.LatinHypercube(d=3)
samples = sampler.random(n=20)
samples = qmc.scale(samples, [0,0,0], [1,1,1])

# Run experiments
for R, G, B in samples:
    # Conduct experiment
    pass
```

## Files in This Skill

- `SKILL.md` - Complete skill instructions for Claude
- `README.md` - This file (overview and quick start)
- `QUICK_REFERENCE.md` - Quick syntax reference
- `examples/statistics_experiments.py` - Statistical analysis examples
- `examples/regression_experiments.py` - Regression modeling examples
- `examples/optimization_experiments.py` - Optimization workflows
- `examples/ml_experiments.py` - Machine learning examples
- `examples/doe_experiments.py` - Design of experiments
- `references/statistical_methods.md` - Statistical analysis guide
- `references/regression_guide.md` - Regression methodology
- `references/optimization_guide.md` - Optimization approaches

## Common Use Cases

1. **Learning Statistics**: "Help me design an experiment to test measurement reproducibility"
2. **Regression Analysis**: "Build a linear model relating R input to 630nm output"
3. **Optimization**: "Find the RGB values that produce 25,000 intensity at 515nm"
4. **Machine Learning**: "Train a random forest to predict spectral outputs from RGB inputs"
5. **DOE**: "Design a Latin hypercube experiment with 20 samples"
6. **Data Analysis**: "Analyze the collected data and plot response curves"

## Tips and Best Practices

### Data Management

- Save experiments to CSV or JSON for later analysis
- Use pandas DataFrames for structured data
- Cache results to avoid redundant API calls
- Document experimental conditions

### Measurement Quality

- Take multiple measurements and average for noise reduction
- Measure background (R=G=B=0) and subtract from readings
- Use consistent measurement protocols
- Check for temporal drift in ambient conditions

### Experimental Design

- Start with simple single-variable experiments
- Use appropriate sampling strategies (grid, random, Latin hypercube)
- Consider interaction effects in multivariable experiments
- Validate models with held-out test data

### Analysis

- Always visualize your data before modeling
- Check model assumptions (normality, linearity, etc.)
- Quantify uncertainties (confidence intervals, prediction intervals)
- Cross-validate machine learning models

## Troubleshooting

**Connection timeout**
- Check internet connection
- Increase timeout in requests: `timeout=30`
- The instrument may be temporarily unavailable

**Unexpected results**
- Verify parameter ranges (0 to 1)
- Check for ambient light interference
- Perform background subtraction
- Average multiple measurements

**Poor model fit**
- Try nonlinear models
- Add polynomial features
- Check for interaction terms
- Collect more data points

## Resources

- **GitHub**: https://github.com/jkitchin/claude-light
- **API Endpoint**: https://claude-light.cheme.cmu.edu/api
- **Web Interface**: https://claude-light.cheme.cmu.edu/rgb
- **Green Machine** (single input): https://claude-light.cheme.cmu.edu/gm

## Learning Objectives

This skill helps you learn:
- **Statistics**: Mean, variance, distributions, confidence intervals
- **Regression**: Linear, polynomial, multivariate modeling
- **Optimization**: Gradient methods, global optimization, constraints
- **Machine Learning**: sklearn models, cross-validation, feature engineering
- **Experimental Design**: DOE, sampling strategies, factorial designs
- **Data Science**: Python, pandas, visualization, reproducible workflows
- **Scientific Method**: Hypothesis testing, validation, uncertainty quantification

## Advanced Topics

- Bayesian optimization with scikit-optimize
- Gaussian process regression
- Active learning strategies
- Multi-objective optimization
- Time series analysis (temporal variations)
- Transfer learning across wavelengths
- Ensemble methods and model stacking

## Version Information

- Skill created for Claude-Light API (2024)
- Compatible with Python 3.8+
- Tested with requests, numpy, scipy, scikit-learn latest versions
