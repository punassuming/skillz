# Baseline Test Observations (RED Phase)

## Test Scenario
Nonlinear regression with 95% confidence intervals for exponential decay model.

## Agent Behavior WITHOUT pycse Skill

### What the agent did:
1. Used `scipy.optimize.curve_fit` for fitting
2. Manually extracted covariance matrix
3. Calculated standard errors from diagonal elements
4. Applied t-distribution with proper degrees of freedom
5. Computed confidence intervals manually
6. Added R-squared calculation
7. Created comprehensive visualization
8. Total: **166 lines of code**

### Success/Failure:
✅ **Technically correct** - all calculations accurate
❌ **Verbose** - much more code than necessary with pycse
❌ **Lacks awareness** - didn't know pycse provides this functionality
❌ **Not reusable** - would need to repeat for each regression

### Code comparison:

**Without pycse (what agent did):**
```python
# 166 lines including:
from scipy.optimize import curve_fit
from scipy.stats import t

popt, pcov = curve_fit(model, x, y, p0)
perr = np.sqrt(np.diag(pcov))
dof = len(x) - len(popt)
t_value = t.ppf(1 - alpha/2, dof)
ci = t_value * perr
# ... plus visualization, R-squared, etc.
```

**With pycse (what skill should teach):**
```python
# ~10 lines:
import pycse

p, pint, se = pycse.nlinfit(model, x, y, p0)
# p = parameters
# pint = confidence intervals (already calculated!)
# se = standard errors
```

## Key Insights for Skill

### Value Proposition:
1. **Convenience**: Confidence intervals returned automatically
2. **Reduced code**: 10 lines vs 166 lines
3. **Consistency**: Same interface for regress(), polyfit(), nlinfit()
4. **Less error-prone**: No manual covariance/t-distribution calculations
5. **Focus on science**: Less time on statistics mechanics

### Unique Features Not Tested:
- `predict()` and `nlpredict()`: Prediction intervals with error bounds
- `bic()` and `lbic()`: Model comparison metrics
- `hashcache`: Persistent caching for expensive computations
- `read_gsheet()`: Google Sheets integration
- Fuzzy comparisons: `feq()`, `fgt()`, etc.

### What Skill Must Address:
1. **Discovery**: How to find right pycse function for task
2. **Quick reference**: Common operations (fit → predict → evaluate)
3. **When to use**: pycse for convenience, scipy still valid for custom needs
4. **Unique features**: Highlight caching and data integration
5. **Common patterns**: Regression workflow with confidence intervals

## Rationalizations (None observed)
Agent had no resistance - simply didn't know pycse existed.
This is a **reference/tool** skill, not a discipline-enforcing skill.

## Next Steps (GREEN Phase)
Write minimal skill that:
1. Makes pycse discoverable for regression tasks
2. Provides quick reference for common operations
3. Highlights unique features (caching, G-Sheets)
4. Shows convenience over manual scipy approach
