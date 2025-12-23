# Python Optimization Example: Data Processing Pipeline

Complete workflow for identifying and fixing performance bottlenecks.

---

## Scenario

**Context**: Processing customer analytics data (1M records)  
**Problem**: Pipeline takes 45 minutes  
**Goal**: Reduce to <5 minutes  

---

## Initial Code (Slow)

```python
def load_data(filename):
    """Load data - SLOW VERSION."""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            data.append({
                'customer_id': parts[0],
                'amount': float(parts[1]),
                'date': parts[2]
            })
    return data
```

**Runtime**: 1823 seconds (30 minutes)

---

## Step 1: Profile with cProfile

```python
import cProfile
profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()
```

**Output**:
```
load_data:    1823s (68% of runtime)
calculate:     745s (28%)
classify:       82s (3%)
```

**Finding**: Data loading is the bottleneck!

---

## Step 2: Optimize Loading (67% improvement)

### Use pandas

```python
def load_data(filename):
    """Load data using pandas."""
    return pd.read_csv(
        filename,
        dtype={
            'customer_id': 'str',
            'amount': 'float32',
            'date': 'str',
            'category': 'category'
        }
    )
```

**New Runtime**: 604 seconds (10 minutes)  
**Improvement**: 3.0× faster

---

## Step 3: Vectorize Calculations (90% improvement)

### BEFORE (745s)
```python
for record in data:
    customer_id = record['customer_id']
    # Manual aggregation...
```

### AFTER (74s)
```python
metrics = df.groupby('customer_id').agg({
    'amount': ['sum', 'count', 'mean']
})
```

**Improvement**: 10.1× faster

---

## Step 4: Parallel Processing

```python
from multiprocessing import Pool

def parallel_process(df, n_workers=4):
    """Process using multiple cores."""
    with Pool(n_workers) as pool:
        results = pool.map(process_chunk, chunks)
    return pd.concat(results)
```

**Final Runtime**: 142 seconds (2.4 minutes) ✅  
**Total Speedup**: **18.4×**

---

## Performance Summary

| Stage | Original | Optimized | Speedup |
|-------|----------|-----------|---------|
| Load | 1823s | 604s | 3.0× |
| Calculate | 745s | 74s | 10.1× |
| Classify | 82s | 33s | 2.5× |
| **Total** | **2654s** | **142s** | **18.4×** |

---

## Key Lessons

1. **Profile First**: Measure before optimizing
2. **Vectorize**: Replace loops with pandas/numpy
3. **Use Right Tools**: pandas for data, not Python lists
4. **Parallel When Possible**: Leverage multiple cores

---

## Tools Reference

```bash
# Profile code
python -m cProfile script.py

# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py

# Memory profiling
pip install memory_profiler
python -m memory_profiler script.py
```
