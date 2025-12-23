# Git Workflow: Feature Development Session

Complete example of professional Git workflow for developing a new feature.

## Scenario Context

**Project**: E-commerce API  
**Feature**: Add product search endpoint  
**Timeline**: 3-day sprint  

---

## Day 1: Feature Branch Creation

### 1. Start with Updated Main

```bash
git checkout main
git pull origin main
```

### 2. Create Feature Branch

```bash
git checkout -b feature/product-search-filters
```

### 3. Implement and Commit

```bash
git add src/api/endpoints/search.py
git commit -m "feat: Add product search endpoint structure

- Create search.py with FastAPI router
- Define endpoint with query parameters
- Add type hints and documentation

Relates to #123"
```

---

## Day 2: Code Review Iteration

### Address Review Comments

```bash
git add src/api/endpoints/search.py
git commit -m "fix: Add validation and pagination

- Validate min_price <= max_price
- Add pagination support
- Improve error handling

Addresses review feedback"
```

---

## Day 3: Merge

```bash
# Clean up history
git rebase -i HEAD~3

# Push and create PR
git push -u origin feature/product-search-filters
```

---

## Key Takeaways

- Keep commits atomic and focused
- Write clear commit messages
- Use feature branches for all work
