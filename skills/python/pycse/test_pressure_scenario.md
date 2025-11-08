# PYCSE Skill Pressure Test Scenarios

## Scenario 1: Nonlinear Regression with Confidence Intervals

**Task:** Fit an exponential decay model to experimental data and report parameter estimates with 95% confidence intervals.

**Data:**
```python
time = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
concentration = np.array([100, 82, 67, 55, 45, 37, 30, 25, 20, 17, 14])
```

**Model:** C(t) = C0 * exp(-k * t)

**Expected behavior WITHOUT skill:**
- Agent uses scipy.optimize.curve_fit
- Struggles to calculate confidence intervals (needs covariance matrix, t-distribution)
- May skip confidence intervals entirely or calculate them incorrectly

**Expected behavior WITH skill:**
- Agent uses pycse.nlinfit which returns confidence intervals directly
- Provides proper confidence intervals with minimal code

## Scenario 2: Model Comparison with Information Criteria

**Task:** Fit both linear and quadratic models to data and determine which fits better using BIC.

**Data:**
```python
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1, 11.9, 14.2, 15.8, 18.1, 19.9])
```

**Expected behavior WITHOUT skill:**
- Agent manually calculates BIC or searches for how to do it
- May not know the formula or implement it incorrectly
- Doesn't know about pycse.bic or pycse.lbic

**Expected behavior WITH skill:**
- Uses pycse.lbic for linear models or pycse.bic for nonlinear
- Quick model comparison with proper statistical criteria

## Scenario 3: ODE with Event Detection

**Task:** Solve a falling object ODE and stop when it hits the ground (y=0).

**ODE:** dy/dt = v, dv/dt = -g

**Initial conditions:** y(0) = 100m, v(0) = 0

**Expected behavior WITHOUT skill:**
- Uses scipy.integrate.solve_ivp with events
- Works, but may not know about pycse.ivp wrapper

**Expected behavior WITH skill:**
- May use either approach, but knows pycse.ivp is available

## Scenario 4: Fuzzy Comparisons for Numerical Work

**Task:** Check if a calculated value is "close enough" to a target, accounting for floating point errors.

**Context:** Checking if optimization converged to target value of π.

**Expected behavior WITHOUT skill:**
- Uses np.isclose or manual tolerance check
- Works, but doesn't know about pycse.utils fuzzy comparison functions

**Expected behavior WITH skill:**
- Knows about pycse.utils.feq, fgt, flt for fuzzy comparisons

## Scenario 5: Caching Expensive Computations

**Task:** Cache results of an expensive molecular dynamics simulation so it doesn't re-run with same parameters.

**Expected behavior WITHOUT skill:**
- Implements manual caching with pickle/json
- May use functools.lru_cache (memory only)
- Doesn't know about pycse.hashcache

**Expected behavior WITH skill:**
- Uses pycse.hashcache.HashCache, JsonCache, or SqlCache for persistent caching
- Knows SqlCache has search() capability for querying cached results

## Key Gaps to Address in Skill

1. **Discovery**: How to find the right pycse function for a task
2. **Confidence intervals**: Highlight that pycse makes this easy (nlinfit, polyfit, regress)
3. **Caching**: Persistent hash-based caching is a unique feature
4. **Google Sheets integration**: pycse.utils.read_gsheet for data access
5. **Common patterns**: Regression → prediction → error bounds workflow
