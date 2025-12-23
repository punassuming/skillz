# TDD Session: Building a String Calculator

Complete Test-Driven Development session demonstrating the red-green-refactor cycle.

## Session Context

**Goal**: Build a simple string calculator that can add numbers from a string  
**Approach**: Strict TDD with red-green-refactor cycle  
**Language**: Python with pytest  
**Duration**: ~45 minutes  

---

## Iteration 1: Empty String Returns 0

### RED - Write Failing Test

```python
# test_calculator.py
def test_empty_string_returns_zero():
    """Empty string should return 0."""
    from calculator import add
    
    result = add("")
    assert result == 0
```

**Run test**: `pytest test_calculator.py`
```
ERROR: cannot import name 'add' from 'calculator'
Test fails ✓
```

### GREEN - Minimal Implementation

```python
# calculator.py
def add(numbers: str) -> int:
    """Add numbers from a string."""
    return 0
```

**Run test**: All tests pass ✓

### REFACTOR

No refactoring needed yet.

**Commit**: `git commit -m "TDD: Empty string returns 0"`

---

## Key Takeaways

1. **Trust the Cycle**: Red-Green-Refactor produces clean, tested code
2. **Small Steps**: Each iteration adds one small capability
3. **Tests as Spec**: Tests document intended behavior clearly

