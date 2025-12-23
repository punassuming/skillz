# Skills Usage Guide: Agentic Workflows with CLI Tools

This guide demonstrates how to use the example skills in this repository with modern AI CLI tools that support agentic workflows.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Using Skills with Gemini CLI](#using-skills-with-gemini-cli)
3. [Using Skills with GitHub Copilot CLI](#using-skills-with-github-copilot-cli)
4. [Using Skills with OpenAI Codex CLI](#using-skills-with-openai-codex-cli)
5. [Agentic Workflow Patterns](#agentic-workflow-patterns)
6. [Example Workflows](#example-workflows)

---

## Quick Start

### Prerequisites

1. **Install the skillz CLI** (this repository):
   ```bash
   cd /path/to/skillz
   uv pip install -e .
   ```

2. **Configure repository path**:
   ```bash
   skillz config set repository /path/to/skillz
   ```

3. **Install a CLI tool** (choose one):
   - **Gemini CLI**: `npm install -g @google/gemini-cli`
   - **Copilot CLI**: `npm install -g @github/copilot`
   - **Codex CLI**: `npm install -g @openai/codex`

### Basic Usage Pattern

```bash
# 1. List available skills
skillz list --type skill

# 2. View a skill and its examples
skillz info tdd

# 3. Install skill to your platform
skillz install tdd --platform gemini

# 4. Use the skill in your CLI tool
gemini-cli "Help me practice TDD by building a calculator"
```

---

## Using Skills with Gemini CLI

[Gemini CLI](https://geminicli.com/) is Google's open-source AI agent for command-line agentic workflows.

### Installation

```bash
npm install -g @google/gemini-cli
gemini auth login
```

### Loading Skills

Skills installed to Gemini are automatically loaded from `~/.config/gemini/skills/`.

```bash
# Install a skill
skillz install tdd --platform gemini

# Verify installation
ls ~/.config/gemini/skills/
```

### Using Skills in Workflows

#### Example 1: TDD Workflow

```bash
# Gemini CLI can automatically discover and use the TDD skill
gemini-cli "I want to practice test-driven development. 
Help me build a string calculator using the red-green-refactor cycle."
```

**What happens:**
1. Gemini CLI loads the `tdd` skill from `~/.config/gemini/skills/tdd/`
2. Reads `SKILL.md` to understand TDD principles
3. References `examples/tdd-session-string-calculator.md` for guidance
4. Guides you through writing tests first, then implementation
5. Suggests refactorings when tests are green

#### Example 2: Code Review Workflow

```bash
# Install code reviewer skill
skillz install code-reviewer --platform gemini

# Use in project directory
cd ~/my-project
gemini-cli "Review my Python data pipeline code and identify bugs"
```

**Gemini will:**
- Apply code review framework from the skill
- Check for resource leaks, security issues, test coverage
- Provide structured feedback with priorities
- Reference examples from `sample-code-review.md`

### Agentic Features in Gemini CLI

Gemini CLI supports **autonomous multi-step workflows**:

```bash
# Complex agentic workflow
gemini-cli "Use TDD to add a new feature: 
1. Write failing tests for product search
2. Implement minimal code to pass
3. Refactor for clarity
4. Run final test suite"
```

Gemini will:
- Break down the task into steps
- Execute each step (write files, run tests)
- Iterate on failures
- Provide completion report

---

## Using Skills with GitHub Copilot CLI

[GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) provides AI-powered terminal assistance with agent skills support.

### Installation

```bash
npm install -g @github/copilot
gh auth login
gh extension install github/gh-copilot
```

### Loading Agent Skills

Copilot loads skills from `.github/skills/` in your project or `~/.config/github-copilot/skills/` globally.

```bash
# Install to project
cd ~/my-project
skillz install python-optimization --platform copilot --target project

# This creates: .github/skills/python-optimization/
```

### Using Skills

#### Example 1: Python Optimization

```bash
cd ~/my-slow-project

# Invoke Copilot with natural language
gh copilot suggest "My data processing pipeline is too slow. 
Use the python-optimization skill to profile and fix it."
```

**Copilot Agent will:**
1. Load `python-optimization` skill
2. Profile code with cProfile
3. Identify bottlenecks (following skill examples)
4. Suggest vectorization with pandas
5. Implement parallel processing if needed
6. Show performance improvements

#### Example 2: Git Workflow

```bash
# Install version-control skill
skillz install version-control --platform copilot --target project

# Use for feature development
gh copilot suggest "Guide me through a professional Git workflow 
for adding a new API endpoint"
```

**Copilot will:**
- Create feature branch
- Suggest commit structure
- Guide through code review iteration
- Help with rebasing and PR creation

### Agent Mode for Autonomous Execution

```bash
# Enable agent mode for autonomous multi-step workflows
gh copilot config set agent-mode true

# Complex workflow
gh copilot agent "Optimize my data pipeline:
1. Profile to find bottlenecks
2. Vectorize slow operations
3. Add parallel processing
4. Benchmark improvements
5. Generate performance report"
```

---

## Using Skills with OpenAI Codex CLI

[Codex CLI](https://github.com/openai/codex) is OpenAI's lightweight coding agent for terminal workflows.

### Installation

```bash
npm install -g @openai/codex
codex auth login
```

### Loading Skills

Codex uses a modular skill system supporting multiple scopes:

```bash
# Install to user scope
skillz install scientific-writing --platform codex

# Or install to specific project
cd ~/research-paper
skillz install scientific-writing --platform codex --target project
```

### Using Skills

#### Example 1: Scientific Writing

```bash
cd ~/my-paper

# Codex loads skills from .codex/skills/ or ~/.config/codex/skills/
codex "Help me write a better abstract for my research paper. 
Show me before/after examples."
```

**Codex will:**
- Load scientific-writing skill
- Review your current abstract
- Apply principles from `research-paper-sections.md`
- Show weak vs strong versions
- Explain improvements

#### Example 2: Literature Review

```bash
# Install literature review skill
skillz install literature-review --platform codex

# Use for research
codex "I need to do a systematic literature review on 
machine learning for materials science. Guide me through the process."
```

**Codex will:**
- Follow PICO framework from skill
- Help develop search strings
- Guide screening process
- Assist with data extraction
- Reference `ml-materials-literature-review.md` example

### Multi-Agent Workflows

Codex supports orchestrating multiple agents with different skills:

```bash
# Define multi-agent workflow
codex agents run \
  --agent researcher:literature-review \
  --agent writer:scientific-writing \
  --task "Research ML in materials, then write introduction section"
```

---

## Agentic Workflow Patterns

### Pattern 1: Sequential Task Execution

**Use Case**: Multi-step development workflows

```bash
# Example with Gemini CLI
gemini-cli --workflow "
Step 1: Use TDD skill to write tests for calculator
Step 2: Implement calculator functions
Step 3: Use code-reviewer skill to review implementation
Step 4: Use version-control skill to commit properly
"
```

### Pattern 2: Iterative Refinement

**Use Case**: Code optimization or refactoring

```bash
# Example with Copilot
gh copilot agent "
Loop until performance target met:
1. Profile code (python-optimization skill)
2. Apply optimization
3. Benchmark
4. If <5 minutes, done. Else, continue.
"
```

### Pattern 3: Skill Composition

**Use Case**: Combining multiple skills for complex tasks

```bash
# Example with Codex
codex agents compose \
  tdd \
  code-reviewer \
  version-control \
  --task "Build new feature with full workflow"
```

---

## Example Workflows

### Workflow 1: Full-Stack Feature Development

```bash
# Using Gemini CLI with multiple skills
cd ~/my-app

# Install required skills
skillz install tdd version-control code-reviewer --platform gemini

# Execute agentic workflow
gemini-cli "
I need to add a product search feature with filters:

1. Use TDD skill to write comprehensive tests first
2. Implement the search endpoint
3. Use code-reviewer skill to check for bugs
4. Use version-control skill to commit with proper messages
5. Create pull request

Follow best practices from all loaded skills.
"
```

**Result**: Gemini autonomously:
- Writes failing tests
- Implements code
- Reviews for issues
- Commits with proper Git workflow
- Creates PR description

### Workflow 2: Research Paper Writing

```bash
# Using Codex CLI with research skills
cd ~/research-project

# Install skills
skillz install literature-review scientific-writing --platform codex

# Agentic research workflow
codex "
Write the introduction section for my paper on quantum computing:

1. Use literature-review skill to gather recent papers (2020-2024)
2. Synthesize findings into key themes
3. Use scientific-writing skill to draft introduction
4. Show before/after examples of weak vs strong writing
5. Generate properly formatted citations

Output: Introduction.md with inline citations
"
```

### Workflow 3: Performance Optimization

```bash
# Using Copilot with optimization focus
cd ~/slow-app

# Install skill
skillz install python-optimization --platform copilot --target project

# Agent-driven optimization
gh copilot agent "
My data processing takes 45 minutes. Goal: under 5 minutes.

Execute optimization workflow:
1. Profile with cProfile to find bottlenecks
2. Apply vectorization techniques (pandas/numpy)
3. Implement parallel processing where beneficial
4. Benchmark each optimization step
5. Generate performance report with speedup metrics

Reference: examples/optimization-workflow.md for proven patterns
"
```

**Result**: Copilot autonomously:
- Profiles code
- Identifies the 68% bottleneck in data loading
- Replaces loops with pandas operations
- Adds multiprocessing
- Reports 18.4× speedup achieved

### Workflow 4: AI Image Generation Campaign

```bash
# Using Gemini with creative skills
cd ~/marketing-campaign

# Install skill
skillz install image-generation --platform gemini

# Creative workflow
gemini-cli "
Create product photography prompts for our new coffee mug line:

1. Use image-generation skill's prompt templates
2. Generate 5 variations: basic, lifestyle, artistic, commercial, minimalist
3. Include all technical parameters (lighting, composition, camera settings)
4. Output: prompts.txt with organized sections

Reference: examples/prompt-examples.md for structure
"
```

---

## Advanced: Custom Skill Integration

### Creating Agentic Skill Bundles

You can create custom skill bundles that combine multiple skills:

```yaml
# .github/workflows/development-workflow.yml
name: Full Development Workflow
skills:
  - tdd
  - code-reviewer
  - version-control
  - python-optimization

triggers:
  - on: feature_request
  - on: performance_issue

workflow:
  - step: design_tests
    skill: tdd
  - step: implement
    skill: tdd
  - step: review
    skill: code-reviewer
  - step: optimize
    skill: python-optimization
    condition: performance_critical
  - step: commit
    skill: version-control
```

### Using with GitHub Actions

```yaml
# .github/workflows/ai-code-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install skills
        run: |
          pip install skillz
          skillz config set repository $GITHUB_WORKSPACE
          skillz install code-reviewer --platform copilot
      
      - name: Run AI Review
        run: |
          gh copilot agent "
          Review this PR using code-reviewer skill:
          - Check for bugs and security issues
          - Verify test coverage
          - Assess code quality
          - Generate review comments
          "
```

---

## Troubleshooting

### Skills Not Loading

```bash
# Check installed skills
skillz list --source personal

# Verify platform-specific directories
ls ~/.config/gemini/skills/
ls ~/.config/github-copilot/skills/
ls ~/.config/codex/skills/

# Reinstall if needed
skillz uninstall skill-name
skillz install skill-name --platform gemini --force
```

### Agent Not Using Skills

Most CLI tools need explicit skill references or natural language that matches skill domains:

```bash
# ❌ Too generic
gemini-cli "help me code"

# ✅ Specific skill invocation
gemini-cli "use the TDD skill to help me build a calculator"

# ✅ Natural language matching skill domain
gemini-cli "I want to practice test-driven development"
```

### Viewing Skill Content

```bash
# View skill details
skillz info skill-name

# View specific example
cat ~/.config/gemini/skills/tdd/examples/tdd-session-string-calculator.md
```

---

## Best Practices

1. **Install skills relevant to your workflow**: Don't install all skills—focus on what you actually use
2. **Reference examples in prompts**: Explicitly mention example files when you want specific guidance
3. **Use agent mode for complex workflows**: Enable autonomous execution for multi-step tasks
4. **Combine skills strategically**: Plan skill combinations for common workflows
5. **Keep skills updated**: Regularly update skills as examples improve

---

## Resources

- [Gemini CLI Documentation](https://geminicli.com/docs/)
- [GitHub Copilot CLI Guide](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [Codex CLI GitHub](https://github.com/openai/codex)
- [Agent Skills Standard](https://developers.openai.com/codex/skills)
- [Agentic Workflows on GitHub](https://githubnext.com/projects/agentic-workflows/)

---

## Contributing

Have questions or examples to share? Open an issue or PR in this repository!
