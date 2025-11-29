# Literature Review Quick Reference Guide

## PICO/PEO Question Template

```
Research Question: [Start with "What is..." or "How does..."]

Population (P): [Who/what is the focus?]
  Example: Adult patients with [condition]
  Example: Specific organisms, systems, or methodologies

Intervention (I): [What is being studied?]
  Example: Treatment or therapy
  Example: Technique, technology, or methodology

Comparison (C): [What alternative?] (optional)
  Example: Standard treatment, alternative approach, or no intervention

Outcome (O): [What results matter?]
  Example: Effectiveness, efficiency, safety, validity

Experience (E): [For qualitative research - what are perspectives?] (optional)
  Example: Patient experiences, researcher perspectives

Final PICO Question:
"In [Population], what is the effectiveness of [Intervention]
compared to [Comparison] for [Outcome]?"
```

## Database Quick Selection

| Database | Strengths | Best For | Coverage |
|----------|-----------|----------|----------|
| **PubMed** | Complete biomedical | Medicine, biology, health | 1966-present |
| **arXiv** | Preprints, methods | Physics, math, CS | 1991-present |
| **Web of Science** | Citation metrics, impact | Multidisciplinary | 1900s-present |
| **Scopus** | Large multidisciplinary | Broad academic searches | 1966-present |
| **IEEE Xplore** | Engineering quality | Engineering, CS | 1950s-present |
| **ACM DL** | CS rigor | Computer science depth | 1947-present |
| **Google Scholar** | Broadest coverage | Initial exploration | All years |
| **Domain repos** | Emerging research | Preprints in field | Varies |

## Boolean Search Operators

### Basic Operators
```
AND       - All terms must appear
           "deep learning" AND "medical imaging"

OR        - Any term can appear
           "neural network" OR "deep learning"

NOT       - Exclude terms
           "cancer" NOT "pediatric"

( )       - Group concepts
           ("deep learning" OR "neural network") AND "diagnosis"
```

### Field Operators (database-specific)
```
Title search:     TITLE:("deep learning")
Abstract search:  ABSTRACT:("medical imaging")
Author search:    AUTHOR:(Smith)
Publication year: YEAR:(2020-2025)
Journal name:     JOURNAL:("Nature Medicine")
```

### Wildcards and Truncation
```
*         - Replace multiple characters
           "learn*" matches: learning, learner, learned

?         - Replace single character
           "neur?l" matches: neural, neuroal

""        - Exact phrase
           "deep learning" (in quotes for exact match)
```

## Search Query Templates by Domain

### Medical/Clinical Research
```
Basic template:
[Condition] AND ([Treatment] OR [Intervention])
AND ([Outcome] OR [Measurement])

Example:
("depression" OR "major depressive disorder") AND
("cognitive behavioral therapy" OR "CBT") AND
("remission" OR "symptom reduction")

Advanced template:
([Specific condition]) AND ([Intervention type]) AND
([Outcome measure]) NOT ([Exclusion criteria])

Example:
("type 2 diabetes") AND ("metformin") AND
("hemoglobin A1c" OR "glycemic control")
NOT ("gestational diabetes")
```

### Computer Science/Technology
```
Basic template:
([Technology] OR [Method]) AND ([Application] OR [Task])
AND ([Metric] OR [Benchmark])

Example:
("transformer model*" OR "attention mechanism*") AND
("natural language processing" OR "NLP") AND
("accuracy" OR "BLEU score")

Advanced template:
([Core technology]) AND ([Application domain]) AND
([Performance aspect]) AND ([Year range]) NOT ([Excluded approach])

Example:
("neural architecture search" OR "NAS") AND
("computer vision" OR "image classification") AND
("energy efficiency" OR "latency" OR "inference time")
2018:2025 NOT ("toy dataset*")
```

### Materials Science
```
Basic template:
[Property] AND ([Material] OR [Composition]) AND
([Method] OR [Technique])

Example:
("thermal conductivity") AND
("graphene" OR "carbon nanotubes") AND
("molecular dynamics" OR "first principles")

Advanced template:
([Property of interest]) AND ([Material class]) AND
([Computational/experimental method]) AND
([Application]) NOT ([Excluded condition])

Example:
("band gap") AND
("perovskite*" OR "halide perovskite*") AND
("density functional theory" OR "DFT") AND
("solar cell*" OR "photovoltaic*")
NOT ("lead-free" only for finding lead-containing)
```

### Social Sciences
```
Basic template:
([Concept]) AND ([Population]) AND ([Context]) AND
([Method])

Example:
("social media") AND ("adolescent*" OR "teenager*") AND
("mental health" OR "depression" OR "anxiety") AND
("qualitative" OR "interview*")

Advanced template:
([Core concept]) AND ([Study population]) AND
([Outcome/impact]) NOT ([Excluded population/approach])

Example:
("remote work" OR "telework") AND
("employee*" OR "worker*") AND
("productivity" OR "burnout" OR "job satisfaction")
NOT ("COVID-19" if wanting non-pandemic data)
```

## Inclusion/Exclusion Criteria Template

```
INCLUSION CRITERIA
✓ Study design: [Specify types]
  Example: Randomized controlled trials, cohort studies

✓ Population: [Define target population]
  Example: Adults (18-75 years), diagnosed with condition X

✓ Intervention: [What must be studied]
  Example: [Specific treatment, technique, or methodology]

✓ Outcomes: [Must measure these]
  Example: Primary outcome: [Y], Secondary: [Z]

✓ Publication: [Type and language]
  Example: Peer-reviewed English-language publications

✓ Time period: [Publication date range]
  Example: Published 2015-2025

✓ Setting: [Where study conducted]
  Example: Clinical settings, hospital-based, ambulatory care

EXCLUSION CRITERIA
✗ Wrong population: [Examples]
✗ Wrong intervention: [Examples]
✗ Wrong outcomes: [Examples]
✗ Wrong study design: [Examples]
✗ Review articles: [If seeking original research]
✗ Non-English publications: [If language constraint]
✗ Before [date]: [If time-limited review]
✗ Conference abstracts only: [No full papers]
```

## Search Documentation Template

```
SEARCH LOG ENTRY

Search #: [Number]
Database: [PubMed/arXiv/etc]
Search Date: [YYYY-MM-DD]
Time Range: [E.g., 2015-2025]

Search Query:
[Exact query as entered]

Results: [Number of papers returned]
Fields Searched: [Title/Abstract/Full text/etc]
Filters Applied: [Language, publication type, etc]

New Relevant Papers: [Number found]
Pass Rate: [Percentage of results relevant]

Refinements for Next Search:
[Notes for improving future searches]

New Concepts Identified:
[Any new keywords/concepts to explore]
```

## Citation Format Quick Reference

### APA (Author-Date)
```
Journal article:
Smith, J., & Jones, M. (2023). Title of article. Journal Name, 45(3), 123-145.
https://doi.org/10.xxxx/xxxxx

Book chapter:
Johnson, R. (2022). Chapter title. In M. Editor (Ed.), Book title (pp. 45-67).
Publisher. https://doi.org/10.xxxx/xxxxx

In-text citation:
(Smith & Jones, 2023) or Smith and Jones (2023) showed...

Multiple works:
(Smith & Jones, 2023; Johnson, 2022)
```

### Chicago (Notes-Bibliography)
```
Footnote (first reference):
1. Jennifer Smith and Maria Jones, "Title of Article," Journal Name 45,
   no. 3 (2023): 123-145, https://doi.org/10.xxxx/xxxxx.

Footnote (subsequent reference):
2. Smith and Jones, "Title of Article," 130.

Bibliography entry:
Smith, Jennifer, and Maria Jones. "Title of Article." Journal Name 45,
no. 3 (2023): 123-145. https://doi.org/10.xxxx/xxxxx.
```

### IEEE (Numbered)
```
Journal article:
[1] J. Smith and M. Jones, "Title of article," Journal Name, vol. 45,
    no. 3, pp. 123–145, 2023, doi: 10.xxxx/xxxxx.

In-text citation:
[1] or The authors in [1] showed...

References list (numbered in order of appearance):
[1] first cited paper
[2] second cited paper
etc.
```

### Nature/Science (Vancouver-style)
```
Journal article:
Smith, J., Jones, M. Title of article. Journal Name 45, 123–145 (2023).

Online publication:
Smith, J., Jones, M. Title of article. Journal Name https://doi.org/10.xxxx/xxxxx (2023).

In-text citations:
as superscript numbers¹²³

References in order of appearance
```

## Data Extraction Template

```
---
Citation: [Full formatted reference]
DOI: [Digital object identifier]
Link: [URL to paper]

BIBLIOGRAPHIC INFO
Authors: [Full list]
Year: [Publication year]
Journal/Venue: [Publication outlet]
Impact Factor: [If applicable]
Type: [Original research/Review/Methods/etc]

STUDY CHARACTERISTICS
Design: [RCT/Cohort/Case-control/Observational/etc]
Population: [N=X, characteristics]
Setting: [Where conducted]
Duration: [Study timeframe]
Intervention: [What was tested]
Comparison: [Comparison group/control]

KEY FINDINGS
Primary outcome: [Measure and result]
Effect size: [If quantitative]
Statistical significance: [p-value, CI]
Secondary findings: [Other important results]

QUALITY ASSESSMENT
GRADE rating: [A/B/C/D]
Risk of bias: [High/Medium/Low]
Key concerns: [Specific quality issues]
Strengths: [What study does well]
Limitations: [Acknowledged and others]

RELEVANCE & CODING
Primary theme: [Main research topic]
Secondary themes: [Related areas]
Methodology: [Key methodological approach]
Novelty: [Foundational/Incremental/Novel]
Relevance to review: [High/Medium/Low]

NOTES
[Any additional important information]
---
```

## Thematic Organization Quick Template

```
THEME: [Main theme name]
Papers: [Number of papers in theme]

Definition: [Clear definition of this theme]

Subtopics:
1. [Subtopic 1] - [X papers]
   Key finding: [Summary statement]
   Examples: [Exemplary papers]

2. [Subtopic 2] - [X papers]
   Key finding: [Summary statement]
   Examples: [Exemplary papers]

Key Consensus Finding:
[What most papers agree on]

Areas of Disagreement:
[Conflicting findings]

Research Evolution:
[How this topic has changed over time]

Gaps in this theme:
[What needs more research]
```

## Quality Assessment Quick Scores

### GRADE Assessment
```
A - High quality: Very unlikely biased estimate of true effect
B - Good quality: Unlikely biased estimate of true effect
C - Fair quality: May be biased but likely addresses question
D - Poor quality: Very likely biased; limited confidence
```

### Risk of Bias Quick Check (Quantitative)
```
✓ Selection bias: Random assignment or adequate matching
✓ Performance bias: Blinding of participants/providers
✓ Detection bias: Blinding of outcome assessors
✓ Attrition bias: <10-15% dropout, balanced loss to follow-up
✓ Reporting bias: All planned outcomes reported
✓ Conflict of interest: No undisclosed conflicts

Each criterion: YES/NO/UNCLEAR
```

### Qualitative Study Quick Assessment
```
Clear research aims? YES / NO / UNCLEAR
Appropriate methodology? YES / NO / UNCLEAR
Rigorous data collection? YES / NO / UNCLEAR
Clear analysis process? YES / NO / UNCLEAR
Reflexivity addressed? YES / NO / UNCLEAR
Data presented clearly? YES / NO / UNCLEAR
Limitations acknowledged? YES / NO / UNCLEAR

→ Rate overall: High / Medium / Low quality
```

## Search Refinement Decision Tree

```
Do you have?

Fewer than 50 papers after screening?
├─ YES → Broaden search
│        • Add synonyms: "term" OR "synonym"
│        • Reduce specificity: Remove restrictive terms
│        • Expand date range
│        • Include grey literature
│        • Try different databases
│        └─ Rerun search
└─ NO → Continue

More than 5,000 papers?
├─ YES → Narrow search
│        • Add specificity: Add more AND operators
│        • Combine similar terms with OR
│        • Add publication type filters
│        • Reduce date range
│        └─ Rerun search
└─ NO → Continue

Are results relevant?
├─ ~70-80% relevant → GOOD, proceed to full-text screening
├─ 30-70% relevant → MODERATE, may refine but proceed
├─ <30% relevant → POOR, refine search before screening
└─ >90% relevant → VERY NARROW, consider broadening
```

## Common Search Mistakes & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Too many results | Too broad | Add AND + specifics |
| Too few results | Too narrow | Add OR + synonyms |
| Wrong results | Poor operators | Check parentheses () |
| Missing papers | Keyword variants | Try synonyms, acronyms |
| Duplicates | Searching multiple DBs | Deduplicate in RefManager |
| Lost in searches | No documentation | Use search log template |

## Report Structure Checklist

### Required Sections
- [ ] Executive summary
- [ ] Introduction (problem, objectives, scope)
- [ ] Methods (search, inclusion/exclusion, quality assessment)
- [ ] Results (selection flowchart, characteristics, quality)
- [ ] Findings (organized thematically)
- [ ] Discussion (synthesis, gaps, implications)
- [ ] Conclusions
- [ ] References (formatted, complete, verified)

### For Systematic Reviews (PRISMA)
- [ ] PRISMA 2020 checklist completed
- [ ] PRISMA flow diagram included
- [ ] Risk of bias assessment table
- [ ] Evidence quality summary (GRADE)
- [ ] Search strategy fully documented
- [ ] Detailed inclusion/exclusion criteria

### For All Reviews
- [ ] All citations complete and accurate
- [ ] DOIs included where available
- [ ] Tables of study characteristics
- [ ] Clear distinction: fact vs. interpretation
- [ ] Conflicts of interest statement
- [ ] Funding source disclosure

## Tools & Links

### Search Tools
- PubMed: pubmed.ncbi.nlm.nih.gov
- arXiv: arxiv.org
- Google Scholar: scholar.google.com
- Web of Science: webofscience.com
- Scopus: scopus.com
- IEEE Xplore: ieeexplore.ieee.org
- ACM DL: dl.acm.org

### Reference Managers
- Zotero: zotero.org (free)
- Mendeley: mendeley.com (free tier)
- EndNote: endnote.com (paid)
- RefWorks: refworks.com (institutional)

### Quality Assessment Tools
- GRADE: gradeworkinggroup.org
- Cochrane Risk of Bias: training.cochrane.org
- CASP Checklists: casp-uk.net
- ROBINS-I: riskofbiasinhewvi.herokuapp.com

### Citation Tools
- CrossRef: crossref.org
- DOI.org: doi.org
- Unpaywall: unpaywall.org (OA finder)

## Key Metrics Quick Reference

### Research Impact
- **Citation count**: Number of times paper cited
- **h-index**: Author impact (h papers with ≥h citations)
- **Journal Impact Factor**: Average citations per article
- **Altmetric**: Broader impact (mentions, downloads)

### Study Quality (Effect Sizes)
- **Cohen's d**: 0.2=small, 0.5=medium, 0.8=large
- **r**: 0.1=small, 0.3=medium, 0.5=large
- **Odds Ratio**: 1.0=no effect, 1.5+=small effect
- **Relative Risk**: 1.0=no effect, 1.5+=moderate effect

## Convergence Indicators (When to Stop Searching)

Stop searching when:
- [ ] Each new search finds <10-15% truly new papers
- [ ] Same papers appearing across multiple searches
- [ ] New searches mostly cited papers already in review
- [ ] Limited new conceptual themes identified
- [ ] Theoretical saturation reached (concepts repeating)
- [ ] 2-3 consecutive searches yield <5% new relevant papers
- [ ] Budget/timeline constraints reached

Continue searching if:
- [ ] Finding >20% new relevant papers in recent searches
- [ ] New research areas continuously identified
- [ ] Important methodological gaps still emerging
- [ ] Time and resources permit

---

**For detailed information, see SKILL.md. For examples and workflows, see README.md.**
