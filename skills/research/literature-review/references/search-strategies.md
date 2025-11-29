# Advanced Search Strategies for Literature Reviews

## Boolean Search Fundamentals

### Core Operators

#### AND (Set Intersection)
Retrieves papers containing ALL specified terms.

**Syntax**: Term1 AND Term2 AND Term3

**Use case**: Narrow results to papers addressing multiple concepts
```
"machine learning" AND "medical imaging"
→ Returns papers containing both concepts
→ Typical result: 30-50% of "machine learning" alone
```

**Best for**: Combining different aspects of your research question

#### OR (Set Union)
Retrieves papers containing ANY of the specified terms.

**Syntax**: Term1 OR Term2 OR Term3

**Use case**: Broaden results to include synonyms and related terms
```
"deep learning" OR "neural network" OR "machine learning"
→ Returns papers mentioning any of these terms
→ Typical result: 200-500% of "deep learning" alone
```

**Best for**: Including terminology variations and synonyms

#### NOT (Negation)
Excludes papers containing specified terms.

**Syntax**: Term1 NOT Term2

**Use case**: Remove irrelevant papers from results
```
"cancer" NOT "pediatric"
→ Returns cancer papers excluding those focusing on children
→ Typical result: 70-90% of "cancer" alone
```

**Best for**: Removing common confounders or irrelevant populations

#### Parentheses (Grouping)
Control search order and operator precedence.

**Syntax**: (Term1 OR Term2) AND Term3

**Use case**: Create complex searches with multiple operators
```
("deep learning" OR "neural network") AND ("medical imaging" OR "diagnosis")
→ Returns papers with (deep learning OR neural network) AND (medical imaging OR diagnosis)
→ Much more targeted than simple AND/OR
```

**Best for**: Organizing complex search concepts

### Operator Precedence

Most databases apply operator precedence (like math):
1. Parentheses ( ) - Highest
2. AND - Middle (in most systems)
3. OR - Lowest

Always use parentheses for clarity and control:
```
AVOID: A OR B AND C
(interprets as: A OR (B AND C), missing papers with (A AND C))

PREFERRED: (A OR B) AND C
(clearly: (A OR B) AND C)
```

## Field-Specific Searching

### Title Searching
**Scope**: Only search in article titles
**Advantage**: Very targeted, fewer false positives
**Disadvantage**: Misses papers discussing concept in body

```
PubMed:      TITLE:"deep learning"
Web of Science: TI="deep learning"
Scopus:      TITLE("deep learning")
IEEE Xplore: "Index Terms": deep learning
```

**Use when**: Looking for papers specifically focused on a concept

### Abstract Searching
**Scope**: Search article titles AND abstracts
**Advantage**: Captures papers discussing concept prominently
**Disadvantage**: More results, some false positives

```
PubMed:      "deep learning"[AB] or just "deep learning"
Web of Science: TS="deep learning" (topic search = title + abstract)
Scopus:      ABS("deep learning")
IEEE Xplore: Default search
```

**Use when**: Concept discussed at paper level

### Full-Text Searching
**Scope**: Search entire article including body
**Advantage**: Captures all mentions
**Disadvantage**: Massive results, many false positives

```
Database limitations: Most databases charge for full-text search
Alternative: Use PDF search tools after downloading papers
```

**Use when**: Searching for very specific terms or methodology details

### Author Searching
**Scope**: Find all papers by specific author(s)
**Advantage**: Track prolific researchers
**Disadvantage**: Need to know specific authors

```
PubMed:      "Smith J"[AU]
Web of Science: AU=Smith, J
Scopus:      AUTH(Smith)
Google Scholar: author:Smith
```

**Use when**: Doing citation tracking or author-based searches

### Journal Searching
**Scope**: Limit search to specific journals
**Advantage**: Access high-impact journals in field
**Disadvantage**: May miss papers in other journals

```
PubMed:      "Nature Medicine"[TA]
Web of Science: SO=Nature Medicine
Scopus:      SOURCE(Nature Medicine)
```

**Use when**: Targeting high-quality venue or specific discipline journal

### Publication Date Searching
**Scope**: Limit results to specific time period
**Advantage**: Focus on recent or historical papers
**Disadvantage**: May miss important early work

```
PubMed:      2015:2025[CRDT]
Web of Science: PY=2015-2025
Scopus:      PUBYEAR > 2015
IEEE Xplore: Content publication year: 2015-2025
```

**Use when**: Setting temporal boundaries for review

## Query Construction Strategies

### Strategy 1: Concept-Based Search

Break research question into core concepts, search for each separately, then combine.

**Example**: "What is the effectiveness of deep learning for cancer diagnosis?"

1. **Concept 1 - Methodology**: deep learning
   - Synonyms: "neural network", "artificial intelligence", "machine learning"
   - Related: "convolutional neural network", "deep neural network"

2. **Concept 2 - Domain**: cancer diagnosis
   - Synonyms: "oncology", "malignancy", "tumour"
   - Related: "early detection", "screening", "classification"

3. **Combine systematically**:
   ```
   ("deep learning" OR "neural network*" OR "convolutional neural network")
   AND
   ("cancer" OR "oncology" OR "malignancy")
   AND
   ("diagnosis" OR "detection" OR "classification")
   ```

### Strategy 2: Building Blocks Approach

Start simple, add complexity iteratively.

```
Search 1: "deep learning"
→ 50,000+ results (too broad)

Search 2: "deep learning" AND "medical"
→ 10,000 results (still broad)

Search 3: "deep learning" AND "cancer diagnosis"
→ 1,500 results (reasonable)

Search 4: ("deep learning" OR "convolutional neural network") AND
          ("cancer" OR "oncology") AND
          ("diagnosis" OR "detection") AND
          (2015:2025)
→ 340 results (manageable)

Search 5: ("deep learning" OR "CNN") AND
          ("breast cancer" OR "lung cancer") AND
          ("sensitivity" OR "specificity" OR "accuracy") AND
          NOT ("review" OR "editorial") AND
          2015:2025
→ 85 results (highly targeted)
```

### Strategy 3: Keyword Expansion

Use initial search results to identify new keywords and concepts.

```
Initial search: "machine learning" + "medical imaging"
Result: 2,400 papers

Scanning top papers, identify additional concepts:
- Methodology variants: "deep learning", "random forest", "support vector machine"
- Application areas: "radiology", "pathology", "oncology"
- Metrics: "AUC", "sensitivity", "specificity"
- Challenges: "overfitting", "interpretability", "generalization"

Expanded searches:
- "random forest" AND "medical imaging"
- "interpretability" AND "machine learning" AND "medical"
- "transfer learning" AND "diagnostic imaging"
```

### Strategy 4: Citation-Based Keywords

Use papers you know to find similar papers.

```
1. Identify key paper in your field
2. Review its keywords and terminology
3. Note main concepts, methods, applications
4. Search for papers citing or cited by this paper
5. Extract keywords from these papers
6. Formulate new searches using identified keywords

Example:
Key paper: "ImageNet-trained convolutional networks for cancer diagnosis"
- Keywords identified: ImageNet, transfer learning, convolutional networks, cancer
- New searches:
  * "transfer learning" + "cancer diagnosis"
  * "ImageNet" + "medical imaging"
  * "pretrained network" + "oncology"
```

## Query Optimization Techniques

### Truncation and Wildcards

**Truncation (*)**: Match multiple word variations
```
"behavio*" matches: behavior, behaviour, behavioral, behavioural
"learn*" matches: learning, learned, learner, learns
```

**Wildcards (?)**: Replace single character
```
"wom?n" matches: woman, women
"colo?r" matches: color, colour
```

**Note**: Not all databases support truncation/wildcards; check documentation

### Phrase Searching

**Exact phrase**: Use quotation marks for multi-word phrases
```
"machine learning" (exact phrase)
vs.
machine learning (either term, anywhere)

"deep neural network" (exact phrase)
vs.
deep neural network (all three words, but not necessarily together)
```

**Best practices**:
- Use for specific terminology: "convolutional neural network"
- Avoid for common concepts: "deep" and "learning" separately might be better
- Use sparingly to avoid missing variations

### Proximity Searching

Some databases support proximity operators (words within N positions).

```
NEAR/5: Words within 5 positions
neural NEAR/5 network
→ "neural" and "network" within 5 words of each other

WITHIN/10: Words within 10 words
"machine learning" WITHIN/10 "medical imaging"
→ Both phrases within 10 words of each other
```

**Availability**: Limited in most academic databases

### MeSH Terms (PubMed)

Medical Subject Headings - standardized vocabulary for medical literature.

```
MeSH major topic: [MeSH:noexp]
Exact MeSH only: "Neoplasms"[MeSH Terms]
Exploded MeSH: "Neoplasms"[MeSH] (includes subtopics)

Example:
("Deep Learning"[MeSH] OR "Artificial Intelligence"[MeSH])
AND
("Diagnostic Imaging"[MeSH] OR "Radiology"[MeSH])
→ Highly standardized, relevant results
```

## Search Strategy By Research Domain

### Biomedical/Clinical Research

**Question**: "What is the effectiveness of [treatment] for [condition]?"

**Key elements**:
- Condition terms (ICD codes if possible)
- Treatment/intervention terms
- Outcome measures
- Study design filters (RCT, observational, etc.)
- Population characteristics

**Example search**:
```
("depression" OR "major depressive disorder" OR "MDD")
AND
("cognitive behavioral therapy" OR "CBT" OR "psychotherapy")
AND
("efficacy" OR "effectiveness" OR "remission rate" OR "symptom reduction")
AND
("randomized controlled trial" OR "RCT" OR "clinical trial")
NOT ("review" OR "meta-analysis" OR "editorial")
AND
2015:2025
```

### Computer Science/Engineering

**Question**: "How effective is [method/algorithm] for [task/problem]?"

**Key elements**:
- Algorithm/method name
- Task/problem domain
- Benchmark/dataset names
- Performance metrics
- Comparison baselines

**Example search**:
```
("transformer model*" OR "attention mechanism*" OR "self-attention")
AND
("natural language processing" OR "NLP" OR "machine translation")
AND
("BLEU score" OR "accuracy" OR "F1 score" OR "perplexity")
NOT ("review" OR "survey")
AND
2018:2025
```

### Materials Science/Chemistry

**Question**: "What properties/methods are used to [characterize/synthesize] [material]?"

**Key elements**:
- Material name/composition
- Property of interest
- Synthesis/characterization method
- Performance metrics
- Application

**Example search**:
```
("perovskite" OR "halide perovskite")
AND
("band gap" OR "electronic properties" OR "optoelectronic properties")
AND
("density functional theory" OR "DFT" OR "first principles")
AND
("solar cell" OR "photovoltaic" OR "light-emitting diode")
NOT ("review" OR "book chapter")
```

### Social Sciences/Psychology

**Question**: "What factors influence [outcome] in [population]?"

**Key elements**:
- Outcome variable
- Predictor/factor variables
- Population characteristics
- Study design (qualitative/quantitative)
- Context/setting

**Example search**:
```
("social media" OR "social network*")
AND
("adolescent*" OR "teenager*" OR "young adult*")
AND
("mental health" OR "depression" OR "anxiety" OR "self-esteem")
AND
("qualitative" OR "interview" OR "focus group" OR "quantitative" OR "survey")
NOT ("animal" OR "cellular")
```

## Iterative Search Refinement

### When Search Returns Too Many Results (>5,000)

**Diagnosis**: Query too broad

**Solutions** (in order of preference):
1. **Add more AND terms**: Combine with additional concepts
   ```
   Before: "machine learning"
   After: "machine learning" AND "medical imaging" AND "diagnosis"
   ```

2. **Be more specific with OR terms**: Use exact terms instead of synonyms
   ```
   Before: "neural network*" OR "deep learning" OR "AI"
   After: "convolutional neural network" OR "deep learning"
   ```

3. **Add exclusion terms**: Remove common non-relevant topics
   ```
   NOT ("game*" OR "robot*" OR "autonomous vehicle*")
   ```

4. **Narrow publication type**: Focus on peer-reviewed research
   ```
   NOT ("news" OR "editorial" OR "opinion")
   ```

5. **Limit date range**: Focus on recent literature
   ```
   2020:2025
   ```

6. **Add quality filters**: Limit to high-impact venues
   ```
   AND (Nature OR Science OR PLOS OR Nature Medicine)
   ```

### When Search Returns Too Few Results (<50)

**Diagnosis**: Query too narrow

**Solutions** (in order of preference):
1. **Add synonyms with OR**: Include related terminology
   ```
   Before: "convolutional neural network"
   After: ("convolutional neural network" OR "CNN" OR "deep learning")
   ```

2. **Remove restrictive terms**: Reduce specificity
   ```
   Before: "cancer diagnosis" AND "deep learning" AND "FDA approved"
   After: "cancer diagnosis" AND "deep learning"
   ```

3. **Remove field restrictions**: Search full text instead of title
   ```
   Before: TITLE:"deep learning"
   After: "deep learning" (full text)
   ```

4. **Expand date range**: Include older literature
   ```
   Before: 2020:2025
   After: 2015:2025
   ```

5. **Remove study design filters**: Include all relevant designs
   ```
   Before: "randomized controlled trial"
   After: (include observational, case reports, etc.)
   ```

6. **Include grey literature**: Theses, conference papers, preprints
   ```
   Add: arXiv, conference papers, dissertations
   ```

## Common Search Mistakes and Fixes

| Issue | Cause | Example | Fix |
|-------|-------|---------|-----|
| Results too broad | Missing AND operators | "cancer treatment" | "cancer" AND "treatment" |
| Results too narrow | Too many AND operators | A AND B AND C AND D AND E | Reduce to key concepts, add OR synonyms |
| Wrong domain | Unclear field selection | CS search in Medline | Use appropriate database for domain |
| Terminology gaps | Using different vocabulary than field | "car" in transportation | Use "automobile", "vehicle" |
| Acronym issues | Acronym means different things | "RNA" (RNA biology vs. Registered Nurse Anesthetists) | Add disambiguating terms |
| Phrase problems | Phrase split across fields | "deep" in title, "learning" in abstract | Use full-text or separate fields |
| Date range | Excluding foundational work | 2020:2025 only | Include earlier key papers |
| Language bias | English-only searches | English search only | Check if other languages important |

## Validation Techniques

### Cross-Database Verification

Validate important papers appear in multiple databases:

```
Search key terms in:
- PubMed (biomedical focus)
- Web of Science (multidisciplinary)
- Scopus (broader coverage)
- Google Scholar (broadest)

If important paper appears in ≥2 databases → Confidence in retrieval
If important paper only in Google Scholar → May be missed in speciality databases
```

### Citation Tracking Validation

Check that key papers are cited consistently:

```
Paper A: Heavily cited (>500 citations)
Search multiple databases:
- How many databases return Paper A?
- How many citing papers found in each database?
- Do differences indicate bias in database coverage?
```

### Baseline Comparison

Use known important papers as validation:

```
1. Identify landmark papers you know should be included
2. Execute search strategy
3. Check if landmark papers appear in results
4. If landmark papers missing:
   → Adjust search strategy
   → Check inclusion/exclusion criteria
   → Verify database coverage
```

## Advanced Strategies

### Search Filter Building

Pre-build common filter combinations:

```
Clinical Study Design Filter (PubMed):
("randomized controlled trial"[PT] OR "controlled clinical trial"[PT]
OR "pragmatic clinical trial"[PT] OR "randomized"[TW])
AND ("human"[MeSH Terms])
AND ("adult"[MeSH Terms])
NOT ("review"[PT])

Reuse across searches:
[Disease] AND [Intervention] AND [Outcomes] AND [Clinical Study Design Filter]
```

### Strategy Testing

Systematically test search effectiveness:

```
Test 1: ("cancer" AND "diagnosis") in PubMed
Result: 450,000+ papers
Pass rate: 5% (2,250 potentially relevant)
Assessment: Too broad, refine

Test 2: ("lung cancer" AND "diagnosis" AND "deep learning")
Result: 1,200 papers
Pass rate: 45% (540 potentially relevant)
Assessment: Better, but still broad

Test 3: ("small cell lung cancer" OR "SCLC") AND "early detection"
        AND ("machine learning" OR "deep learning")
Result: 89 papers
Pass rate: 70% (62 potentially relevant)
Assessment: Manageable, well-targeted
```

---

**For quick search templates, see QUICK_REFERENCE.md. For overall methodology, see SKILL.md.**
