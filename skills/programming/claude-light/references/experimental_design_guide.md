# Experimental Design Guide for Claude-Light

Complete guide to designing and conducting experiments with the Claude-Light instrument.

## Overview

Claude-Light provides a 3-input (R, G, B), 10-output (spectral channels) experimental system perfect for learning:
- Statistical analysis and reproducibility
- Regression modeling (linear and nonlinear)
- Optimization and inverse problems
- Design of experiments methodologies
- Machine learning on real data

## Experimental Methodologies

### 1. Statistics and Reproducibility

**Objective**: Quantify measurement precision and understand variability.

**Approach**:
1. Select fixed input conditions (e.g., R=0.5, G=0.5, B=0.5)
2. Repeat measurement 20-50 times
3. Calculate descriptive statistics
4. Assess normality of distribution
5. Compute confidence intervals

**Metrics**:
- Mean, median, mode
- Standard deviation
- Coefficient of variation (CV%)
- 95% confidence intervals
- Normality tests (Shapiro-Wilk, Anderson-Darling)

**Interpretation**:
- CV < 5%: Excellent precision
- CV 5-10%: Good precision
- CV > 10%: Consider averaging or background subtraction

### 2. Linear Regression (Single Variable)

**Objective**: Establish input-output relationship for one channel.

**Design**:
- **Grid Sampling**: 10-15 evenly spaced points from 0 to 1
- **Replication**: 3-5 measurements per point for noise reduction
- **Control**: Keep other inputs constant (typically 0)

**Analysis**:
1. Fit linear model: y = mx + b
2. Calculate R², RMSE, MAE
3. Quantify parameter uncertainties
4. Check residuals for systematic patterns
5. Validate predictions on held-out data

**Validation**:
- Use model to predict inputs for target outputs
- Experimentally verify predictions
- Calculate prediction error

### 3. Multivariate Regression

**Objective**: Model multiple inputs affecting multiple outputs.

**Sampling Strategies**:

**Grid Design** (simple but expensive):
```python
# Full factorial: 3³ = 27 experiments
for R in [0, 0.5, 1]:
    for G in [0, 0.5, 1]:
        for B in [0, 0.5, 1]:
            # Experiment
```

**Latin Hypercube** (space-filling, efficient):
```python
from scipy.stats import qmc
sampler = qmc.LatinHypercube(d=3)
samples = sampler.random(n=20)
samples = qmc.scale(samples, [0,0,0], [1,1,1])
```

**Random Sampling** (simple):
```python
n = 25
samples = np.random.random((n, 3))
```

**Analysis**:
- Multiple linear regression
- Coefficient interpretation
- Interaction terms (polynomial features)
- Cross-validation for generalization

### 4. Optimization

**Objective**: Find inputs that produce desired outputs.

**Methods**:

**Gradient-Free (recommended for noisy systems)**:
- Nelder-Mead Simplex
- Powell's method
- Bayesian optimization

**Gradient-Based** (if gradients can be estimated):
- L-BFGS-B
- Sequential Least Squares

**Example**:
```python
from scipy.optimize import minimize

def objective(inputs):
    R, G, B = np.clip(inputs, 0, 1)
    data = get_measurement(R, G, B)
    actual = data['out']['515nm']
    target = 30000
    return (actual - target)**2

result = minimize(objective, [0.5, 0.5, 0.5],
                 bounds=[(0,1), (0,1), (0,1)],
                 method='Nelder-Mead')
```

**Multi-Objective**:
```python
def multi_objective(inputs):
    data = get_measurement(*inputs)
    error_515 = (data['out']['515nm'] - target_515)**2
    error_630 = (data['out']['630nm'] - target_630)**2
    return error_515 + error_630  # or weighted sum
```

### 5. Design of Experiments (DOE)

**Objective**: Maximize information from minimum experiments.

**Classical Designs**:

**Full Factorial**:
- Test all combinations of factor levels
- 3 factors × 3 levels = 27 experiments
- Complete information about main effects and interactions

**Fractional Factorial**:
- Test subset of combinations
- Trade some interaction information for efficiency
- Useful for screening many factors

**Central Composite Design**:
- Factorial points + center points + axial points
- Good for response surface modeling
- Detects curvature in responses

**Modern Designs**:

**Latin Hypercube Sampling**:
- Space-filling design
- Good coverage of input space
- Flexible sample size

**Sobol Sequences**:
- Low-discrepancy sampling
- Better than random for integration
- Good for sensitivity analysis

**Adaptive Designs**:
- Bayesian optimization
- Active learning
- Sequential experimentation

### 6. Uncertainty Quantification

**Sources of Uncertainty**:
1. Measurement noise
2. Model inadequacy (e.g., assuming linear when nonlinear)
3. Parameter estimation uncertainty
4. Ambient conditions (temperature, background light)

**Methods**:

**Bootstrap**:
```python
def bootstrap_uncertainty(X, y, n_boot=1000):
    predictions = []
    for _ in range(n_boot):
        idx = np.random.choice(len(X), len(X), replace=True)
        model.fit(X[idx], y[idx])
        predictions.append(model.predict(X_new))
    return np.percentile(predictions, [2.5, 97.5], axis=0)
```

**Prediction Intervals**:
- Quantify uncertainty in predictions
- Wider than confidence intervals
- Account for both parameter and measurement uncertainty

**Sensitivity Analysis**:
- Vary inputs systematically
- Quantify output sensitivity to each input
- Identify most important factors

### 7. Machine Learning

**When to Use ML**:
- Nonlinear relationships
- Complex interactions
- Large datasets (50+ points)
- Black-box modeling acceptable

**Model Selection**:

**Linear Models** (interpretable):
- LinearRegression, Ridge, Lasso
- Good baseline
- Interpretable coefficients

**Tree-Based** (handle nonlinearity):
- RandomForest, GradientBoosting
- Feature importance
- Robust to outliers

**Neural Networks** (flexible):
- MLPRegressor
- Universal approximators
- Require more data

**Workflow**:
1. Train/test split (80/20)
2. Try multiple models
3. Cross-validation for model selection
4. Hyperparameter tuning
5. Evaluate on test set
6. Check for overfitting

## Best Practices

### Data Collection

1. **Randomize Order**: Prevent temporal confounding
2. **Replicate**: At least 3 measurements per condition
3. **Background**: Measure ambient (R=G=B=0) regularly
4. **Validation**: Reserve 20% data for testing
5. **Documentation**: Record all conditions

### Quality Control

1. **Check Linearity**: Plot residuals vs. fitted
2. **Normality**: Histogram of residuals
3. **Homoscedasticity**: Constant variance across range
4. **Outliers**: Identify and investigate
5. **Reproducibility**: Repeat key experiments

### Analysis

1. **Visualize First**: Always plot before modeling
2. **Simple First**: Start with linear models
3. **Validate**: Use held-out data
4. **Quantify Uncertainty**: Report confidence/prediction intervals
5. **Physical Constraints**: Ensure predictions are feasible (0-1 range)

### Reporting

Include in reports:
- Experimental design (how many points, sampling strategy)
- Data visualization
- Model equations with parameters
- Goodness of fit metrics (R², RMSE)
- Uncertainty quantification
- Validation results
- Conclusions and recommendations

## Example Workflows

### Workflow 1: Characterize One Channel

```
1. Statistics (30 repeats at R=0.5)
2. Single-variable sweep (11 points, R: 0→1)
3. Linear regression
4. Validate predictions (3 new points)
5. Report: mean, std, R², equation
```

### Workflow 2: Multi-Channel Optimization

```
1. Latin hypercube (25 points)
2. Multivariate regression for each output
3. Define objective function
4. Optimize using scipy.minimize
5. Validate optimal solution
```

### Workflow 3: Machine Learning

```
1. Collect 50+ data points (LHS)
2. Train/test split (40/10)
3. Compare models (Linear, RF, MLP)
4. Cross-validation
5. Select best model
6. Evaluate on test set
7. Feature importance analysis
```

## Common Pitfalls

1. **Too Few Points**: At least 10× number of parameters
2. **Poor Sampling**: All points in corner of space
3. **No Validation**: Overfitting not detected
4. **Ignoring Uncertainty**: Point estimates without intervals
5. **Over-Interpretation**: Correlation ≠ causation
6. **No Replication**: Cannot assess precision
7. **Temporal Effects**: Not randomizing order
8. **Extrapolation**: Predicting outside measured range

## Resources

- **DOE**: Montgomery, "Design and Analysis of Experiments"
- **Regression**: Draper & Smith, "Applied Regression Analysis"
- **ML**: Hastie et al., "Elements of Statistical Learning"
- **Optimization**: Nocedal & Wright, "Numerical Optimization"
- **Python**: scikit-learn, scipy, statsmodels documentation

## Metrics Reference

### Regression Metrics

**R² (Coefficient of Determination)**:
- Range: -∞ to 1 (1 is perfect)
- Interpretation: Fraction of variance explained
- Can be negative for bad models

**RMSE (Root Mean Squared Error)**:
- Same units as output
- Penalizes large errors
- Lower is better

**MAE (Mean Absolute Error)**:
- Same units as output
- Robust to outliers
- Lower is better

**Adjusted R²**:
- Accounts for number of parameters
- Use for model comparison
- Prevents overfitting

### Model Selection

**AIC (Akaike Information Criterion)**:
- Lower is better
- Balances fit and complexity
- Good for comparing models

**BIC (Bayesian Information Criterion)**:
- Similar to AIC
- Stronger penalty for complexity
- Prefers simpler models

**Cross-Validation Score**:
- Out-of-sample performance
- Most reliable for prediction
- Computationally expensive
