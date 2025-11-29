# Code Reviewer Skill

A comprehensive skill for systematic code review and analysis across multiple dimensions of software quality, maintainability, and best practices.

## Overview

This skill transforms Claude into a thorough code reviewer, evaluating software projects with structured analysis covering documentation, logic, testing, code quality, and language-specific best practices. It provides actionable feedback to improve code quality while supporting developer growth.

## Core Review Framework

### 1. **Project Structure Assessment**
- Directory organization and file naming
- Configuration files and entry points
- Standard project layout patterns

### 2. **Documentation Review**
- Module and function docstrings
- README and API documentation
- Inline comments and change logs
- Consistent documentation style

### 3. **Logic and Bug Detection**
- Common bug patterns (null handling, index errors, type mismatches)
- Algorithm correctness and edge cases
- Error handling and performance considerations

### 4. **Testing Assessment**
- Unit, integration, and end-to-end test coverage
- Test quality and independence
- Mock usage and parametrization
- Test organization and naming

### 5. **Code Quality and Consistency**
- Code style and formatting
- Naming conventions and organization
- Code smells (duplication, long functions, dead code)
- Import management

### 6. **Jupyter Notebook Review**
- Cell organization and reproducibility
- Narrative quality and documentation
- Data science best practices
- Visualization quality

## When to Use This Skill

- **Code review requests** - Systematic evaluation of pull requests or code changes
- **Project audits** - Comprehensive assessment of entire codebases
- **Quality assurance** - Pre-deployment code quality checks
- **Refactoring planning** - Identifying improvement opportunities
- **Documentation review** - Ensuring adequate documentation coverage
- **Bug investigation** - Finding logic errors and edge cases
- **Testing strategy** - Evaluating test coverage and quality
- **Notebook review** - Assessing Jupyter notebooks for data analysis

## Key Capabilities

1. **Structured Analysis** - Systematic review across 6 dimensions
2. **Language-Specific Expertise** - Python, R, JavaScript, and more
3. **Bug Detection** - Identifying common patterns and edge cases
4. **Test Evaluation** - Assessing coverage, quality, and strategy
5. **Documentation Assessment** - Evaluating completeness and clarity
6. **Code Quality Analysis** - Detecting code smells and inconsistencies
7. **Notebook Review** - Specialized Jupyter notebook evaluation
8. **Actionable Feedback** - Specific, prioritized improvement recommendations
9. **Constructive Tone** - Professional, supportive feedback
10. **Security Awareness** - Identifying potential vulnerabilities

## Review Output Structure

### Executive Summary
- Overall code quality assessment
- Top 3-5 priority recommendations
- Notable strengths
- Risk level classification

### Detailed Analysis
Structured feedback across:
- Documentation gaps and improvements
- Logic errors and bug patterns
- Testing coverage and quality
- Code quality issues and refactoring suggestions

### Improvement Roadmap
Prioritized action items:
1. **Critical** - Security vulnerabilities, major bugs
2. **High** - Logic errors, missing tests, documentation gaps
3. **Medium** - Code quality, minor bugs, style issues
4. **Low** - Optimizations, minor enhancements

## Language-Specific Support

### Python
- PEP 8 compliance
- Virtual environment and dependency management
- Package structure and imports
- Exception handling patterns

### R
- Coding style conventions
- Package documentation (NAMESPACE, DESCRIPTION)
- Roxygen2 function documentation
- testthat testing framework

### JavaScript/Node.js
- ES6+ modern features
- Package.json management
- ESLint compliance
- Async/await patterns

### General Best Practices
- Version control patterns
- Configuration management
- Security considerations
- Performance optimization

## Feedback Guidelines

### Constructive Criticism
- Specific locations and code references
- Clear rationale for changes
- Multiple solution alternatives
- Context-aware recommendations

### Positive Recognition
- Acknowledge good practices
- Recognize improvements
- Appreciate design decisions

### Actionable Recommendations
Each suggestion includes:
- Clear problem description
- Specific code changes
- Expected benefits
- Implementation effort estimate

## Review Process Checklist

- [ ] Check all files in scope
- [ ] Verify code can run/import
- [ ] Review test files
- [ ] Check documentation completeness
- [ ] Identify security/performance concerns
- [ ] Provide specific, actionable feedback
- [ ] Prioritize recommendations
- [ ] Maintain constructive tone

## Example Usage

```
User: "Review this Python module for code quality"
Claude: [Activates code-reviewer skill]
- Analyzes project structure
- Reviews documentation
- Checks for bugs and logic errors
- Evaluates test coverage
- Assesses code quality
- Provides prioritized recommendations
```

## Best Practices

1. **Be Thorough** - Review all aspects systematically
2. **Be Specific** - Reference exact locations and code
3. **Be Constructive** - Explain why changes improve code
4. **Be Contextual** - Consider project constraints
5. **Be Actionable** - Provide clear implementation guidance
6. **Be Balanced** - Recognize strengths and weaknesses
7. **Be Professional** - Maintain supportive tone

## File Organization

- `SKILL.md` - Complete skill specification
- `README.md` - This overview document
- `QUICK_REFERENCE.md` - Quick reference guide

This skill ensures comprehensive, fair, and actionable code reviews that improve software quality while supporting developer growth and learning.
