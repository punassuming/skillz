# Code Reviewer Quick Reference

## Review Dimensions

### 1. Project Structure
- [ ] Directory organization logical
- [ ] File naming consistent
- [ ] Configuration files present
- [ ] Entry points clear

### 2. Documentation
- [ ] Module docstrings complete
- [ ] README with installation/usage
- [ ] Function/class docstrings
- [ ] Type hints where appropriate

### 3. Logic & Bugs
- [ ] Null/None handling
- [ ] Index bounds checking
- [ ] Edge cases covered
- [ ] Error handling appropriate

### 4. Testing
- [ ] Unit tests present
- [ ] Integration tests where needed
- [ ] Test coverage adequate
- [ ] Tests independent

### 5. Code Quality
- [ ] Consistent formatting
- [ ] No code duplication
- [ ] Functions/classes appropriate size
- [ ] No dead code or unused imports

### 6. Notebooks (if applicable)
- [ ] Cells in logical order
- [ ] Markdown explanations clear
- [ ] Reproducible execution
- [ ] Visualizations labeled

## Review Output Template

### Executive Summary
```
Overall Assessment: [Excellent/Good/Fair/Needs Work]

Key Strengths:
- [Strength 1]
- [Strength 2]

Top Recommendations:
1. [Most important improvement]
2. [Second priority]
3. [Third priority]

Risk Level: [Critical/Moderate/Minor]
```

### Documentation Assessment
```
Component: [file.py]
Current: [Brief state]
Issues: [Specific problems]
Recommendation: [Specific action]
Priority: [High/Medium/Low]
```

### Logic/Bug Issues
```
Location: file.py:42 or function_name()
Type: [Bug/Logic error/Edge case]
Description: [Clear explanation]
Impact: [Consequences]
Fix: [Specific suggestion]
```

### Testing Gaps
```
Coverage: [X% line coverage]
Missing: [Specific untested areas]
Issues: [Test quality problems]
Recommendation: [Testing strategy]
```

### Code Quality Issues
```
Pattern: [Code smell type]
Locations: [Files/functions]
Impact: [Effect on maintainability]
Refactoring: [Specific approach]
```

## Priority Levels

### Critical (Fix Immediately)
- Security vulnerabilities
- Major bugs causing failures
- Data corruption risks
- Blocking issues

### High (Address Soon)
- Logic errors
- Missing essential tests
- Major documentation gaps
- Significant performance issues

### Medium (Plan to Address)
- Code quality improvements
- Minor bugs
- Style inconsistencies
- Refactoring opportunities

### Low (Nice to Have)
- Optimization opportunities
- Minor documentation enhancements
- Cosmetic improvements

## Common Code Smells

### Python
- Missing virtual environment
- No requirements.txt
- Mixing tabs and spaces
- Bare except clauses
- Mutable default arguments
- Using global variables

### R
- Inconsistent naming (mix of styles)
- Missing package documentation
- No tests with testthat
- Hard-coded file paths
- Not using tibbles/data.tables

### JavaScript
- Callback hell (not using async/await)
- No error handling in promises
- Missing package.json scripts
- console.log in production
- No ESLint configuration

### General
- Magic numbers (unexplained constants)
- Long functions (>50 lines)
- Deep nesting (>3 levels)
- Duplicate code
- Unclear variable names
- Missing error handling

## Language-Specific Checks

### Python
```python
# Good
def calculate_discount(price: float, rate: float) -> float:
    """Calculate discount amount.

    Args:
        price: Original price
        rate: Discount rate (0-1)

    Returns:
        Discount amount

    Raises:
        ValueError: If rate not in [0, 1]
    """
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * rate
```

### R
```r
# Good
#' Calculate discount amount
#'
#' @param price Numeric. Original price
#' @param rate Numeric. Discount rate (0-1)
#' @return Numeric. Discount amount
#' @export
calculate_discount <- function(price, rate) {
  if (rate < 0 || rate > 1) {
    stop("Rate must be between 0 and 1")
  }
  price * rate
}
```

### JavaScript
```javascript
// Good
/**
 * Calculate discount amount
 * @param {number} price - Original price
 * @param {number} rate - Discount rate (0-1)
 * @returns {number} Discount amount
 * @throws {Error} If rate not in [0, 1]
 */
function calculateDiscount(price, rate) {
  if (rate < 0 || rate > 1) {
    throw new Error('Rate must be between 0 and 1');
  }
  return price * rate;
}
```

## Testing Checklist

- [ ] Test file exists for each module
- [ ] Tests follow naming convention
- [ ] Happy path tested
- [ ] Edge cases tested (empty, null, boundary)
- [ ] Error conditions tested
- [ ] Tests are independent
- [ ] Tests have clear names
- [ ] Assertions are specific
- [ ] Mocks used appropriately
- [ ] Coverage >80% for critical code

## Documentation Checklist

- [ ] README with overview
- [ ] Installation instructions
- [ ] Usage examples
- [ ] API documentation
- [ ] Module docstrings
- [ ] Function/class docstrings
- [ ] Inline comments for complex logic
- [ ] Type hints (Python)
- [ ] CHANGELOG or version history
- [ ] Contributing guidelines (if open source)

## Security Checklist

- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Proper authentication/authorization
- [ ] Secure random number generation
- [ ] No eval() or exec() misuse
- [ ] Dependencies up to date
- [ ] Sensitive data properly handled

## Performance Checklist

- [ ] No N+1 queries
- [ ] Appropriate data structures
- [ ] Efficient algorithms (complexity)
- [ ] Lazy loading where appropriate
- [ ] Caching implemented
- [ ] No unnecessary loops
- [ ] Database indexes used
- [ ] Large file streaming
- [ ] Memory leaks prevented
- [ ] Resource cleanup (files, connections)

## Feedback Tone

### Do:
✓ Be specific with locations
✓ Explain rationale for changes
✓ Offer multiple solutions
✓ Acknowledge good practices
✓ Maintain constructive tone
✓ Estimate implementation effort

### Don't:
✗ Make vague criticisms
✗ Only point out negatives
✗ Demand specific solutions
✗ Ignore project context
✗ Use harsh language
✗ Overwhelm with minor issues

## Quick Review Process

1. **Scan** - Quick overview of project structure
2. **Document** - Check README and docstrings
3. **Read** - Review code logic and patterns
4. **Test** - Evaluate test coverage and quality
5. **Note** - Identify issues and strengths
6. **Prioritize** - Classify by severity
7. **Report** - Structured feedback with examples
8. **Suggest** - Actionable improvements

## Common Recommendations

### High Impact, Low Effort
- Add missing docstrings
- Fix obvious bugs
- Add basic error handling
- Remove unused imports
- Fix inconsistent formatting

### High Impact, Medium Effort
- Add critical tests
- Refactor long functions
- Improve error messages
- Add input validation
- Document complex logic

### High Impact, High Effort
- Comprehensive test suite
- Major refactoring
- Security improvements
- Performance optimization
- Complete documentation overhaul
