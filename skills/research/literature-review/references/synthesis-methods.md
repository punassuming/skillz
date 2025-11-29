# Synthesis Methods and Evidence Integration

## Overview of Synthesis Approaches

Different literature reviews require different synthesis methods depending on research question, available evidence, and review objectives.

## 1. Narrative Synthesis

### Definition
Integrative summary of findings organized thematically or conceptually, using words and citations rather than statistical combination.

### When to Use
- Mixed study designs (RCTs, observational, qualitative)
- Small number of studies
- Heterogeneous populations or interventions
- Qualitative research predominant
- Evidence not amenable to meta-analysis

### Process

#### Step 1: Preliminary Synthesis
Group papers by primary themes or concepts.

```
Theme: Treatment Effectiveness for Condition X

Subtheme 1: Short-term outcomes (n=15 papers)
Subtheme 2: Long-term outcomes (n=8 papers)
Subtheme 3: Adverse effects (n=12 papers)
Subtheme 4: Cost-effectiveness (n=4 papers)
```

#### Step 2: Organize Findings

Create narrative summary organized by theme:

```
SHORT-TERM OUTCOMES

Fifteen studies examined short-term treatment effectiveness (weeks to 6 months).
The majority (13/15, 87%) reported statistically significant improvement
compared to control conditions (effect size range: Cohen's d = 0.4-1.2).

Two studies reported null results:
- Study A: Small sample (n=25), noted underpowering
- Study B: Used alternative outcome measure not showing improvement

Most studies (11/15) showed improvement of 30-50% relative to baseline.
Studies using [methodology X] (6 studies) showed larger effects (mean d=0.9)
compared to [methodology Y] (5 studies, mean d=0.6).

All studies enrolled predominantly [demographic A]; limited evidence in
[demographic B] populations.
```

#### Step 3: Explore Heterogeneity

Examine sources of variation in findings:

```
Sources of outcome variation identified:

1. Study Design
   - RCTs (n=8): Mean effect d=0.7, 95% showed improvement
   - Observational (n=7): Mean effect d=0.5, 85% showed improvement
   → RCTs show stronger effects

2. Patient Population
   - Adults: Consistent improvement (mean d=0.6)
   - Elderly: Mixed results (mean d=0.3)
   → Effectiveness may decrease with age

3. Treatment Duration
   - Short-term (2-4 weeks): d=0.4
   - Medium-term (1-3 months): d=0.6
   - Long-term (6+ months): d=0.7
   → Longer exposure shows stronger effects

4. Publication Year
   - Pre-2015: d=0.5 (older studies, n=4)
   - 2015-2020: d=0.6 (n=8)
   - 2020+: d=0.8 (n=3)
   → Possible improvement in methodology over time
```

#### Step 4: Synthesize Across Themes

Integrate findings to answer research question:

```
OVERALL SYNTHESIS

This review synthesized findings from 15 studies examining [intervention]
for [condition]. Key findings:

Evidence for Effectiveness:
- 87% of studies (13/15) reported significant improvement
- Effect sizes ranged from small to large (d=0.4-1.2)
- Consistent across most study designs and populations
- Effects increase with treatment duration

Evidence for Safety:
- Few serious adverse events reported
- Most adverse events mild and reversible
- [Specific concern] observed in 3 studies but not consistently

Evidence for Mechanisms:
- [Mechanism A] supported by [X studies]
- [Mechanism B] supported by [Y studies]
- Conflicting evidence regarding [Mechanism C]

Implications:
- Appears effective for [target population]
- Limited evidence for [different population]
- Magnitude of benefit similar to [comparable treatment]
- Practical implementation considerations noted in [X studies]
```

### Strengths
- Flexible, accommodates diverse study types
- Incorporates contextual factors and mechanisms
- Accessible to non-specialist readers
- Can include qualitative research

### Limitations
- Subjective organization decisions
- Potential for author bias in selection
- Difficult to assess overall strength of evidence
- Cannot statistically combine effects

## 2. Meta-Analysis

### Definition
Statistical combination of quantitative results from comparable studies to produce summary effect estimate.

### When to Use
- Multiple RCTs or similar designs
- Comparable interventions and populations
- Similar outcome measures
- ≥3 studies with sufficient data
- Homogeneous enough for combining

### Meta-Analysis Types

#### Fixed Effects Meta-Analysis
**Assumption**: Single true effect size, studies differ only due to sampling error

**Formula**:
```
Weighted average effect = Σ(effect × weight) / Σ(weights)
Weight = 1 / (variance of effect in study)
```

**Use when**: Studies very similar, minimal heterogeneity

**Example**:
```
Study A: effect = 0.6, n=100, weight=50%
Study B: effect = 0.5, n=100, weight=50%
Pooled effect = 0.55 (weighted average)
```

#### Random Effects Meta-Analysis
**Assumption**: Different true effect sizes in different studies

**Adds**: Additional variance component for between-study differences

**Use when**: Heterogeneity present, populations vary, interventions vary

**More conservative**: Wider confidence intervals than fixed effects

**Example**:
```
Study A: effect = 0.6, 95% CI: 0.4-0.8
Study B: effect = 0.4, 95% CI: 0.2-0.6
Heterogeneity: I² = 60% (substantial)
→ Use random effects
Pooled effect = 0.50, 95% CI: 0.25-0.75
(wider CI reflecting uncertainty about true effect)
```

### Steps in Meta-Analysis

#### Step 1: Determine Comparability
```
Decision: Can we combine these studies?

Study Similarity Assessment:
✓ Similar outcomes? (all use same measure)
✓ Similar populations? (age, disease severity, etc.)
✓ Similar interventions? (dose, duration, delivery)
✓ Similar designs? (all RCTs, all observational, etc.)

If YES to most: Proceed with meta-analysis
If NO to several: Consider subgroup analysis or narrative synthesis
```

#### Step 2: Extract Effect Data

For each study, extract:
- Effect size with confidence interval
- Sample size for each group
- Mean, SD, and N for each outcome
- Correlation coefficients (for continuous outcomes)
- Event counts (for binary outcomes)

```
Study Data Extraction:

Treatment group: n=100, events=70
Control group: n=100, events=50

Risk difference = (70-50)/100 = 0.20
Risk ratio = 70/50 = 1.40
Odds ratio = (70×50)/(30×50) = 2.33

Select appropriate effect measure for analysis
```

#### Step 3: Calculate Effects

Convert all studies to same metric:

```
Continuous outcomes:
→ Standardized Mean Difference (Cohen's d)
→ Mean Difference

Binary outcomes:
→ Odds Ratio
→ Risk Ratio
→ Risk Difference

Survival data:
→ Hazard Ratio
```

#### Step 4: Pool Effects

Combine using fixed or random effects model:

```R
# Example forest plot interpretation:

Study A   ◆────────○────────┐  0.60 [0.40-0.80]
Study B      ◆──────○──────┐  0.50 [0.35-0.65]
Study C        ◆───────○──┐  0.70 [0.50-0.90]

Overall       ◆─────○─────┐  0.60 [0.48-0.72]

Diamond = overall pooled effect
Width = confidence interval
```

#### Step 5: Assess Heterogeneity

**I² statistic**: Percentage of variation due to heterogeneity (not sampling error)

```
I² = 0%: No heterogeneity
I² = 25%: Low heterogeneity
I² = 50%: Moderate heterogeneity
I² = 75%: High heterogeneity
I² = 100%: Very high heterogeneity

→ I² > 50% suggests problems with pooling
→ Investigate sources of heterogeneity
```

#### Step 6: Investigate Sources

If heterogeneity exists, examine:

```
Subgroup analysis:
- By population (age, gender, disease severity)
- By intervention (dose, duration, delivery)
- By study quality (RCTs vs observational)
- By outcome measurement

Meta-regression:
- Examine effect of continuous variables
- Example: Does effect increase with treatment dose?
- Example: Do effects differ by year of publication?
```

#### Step 7: Assess Publication Bias

Check for bias using:
- Funnel plots
- Egger's test
- Trim and fill method
- Duval and Tweedie's test

```
Symmetric funnel plot = no bias
Asymmetric funnel plot = publication bias likely
```

#### Step 8: Report Results

**Essential reporting elements**:
1. Forest plot showing individual and pooled effects
2. Summary of heterogeneity (I² and p-value)
3. Subgroup analyses if performed
4. Publication bias assessment
5. Sensitivity analyses
6. Interpretation with clinical context

### Meta-Analysis Reporting (PRISMA)

```
SAMPLE META-ANALYSIS RESULTS SECTION

Pooled Analysis:

Eleven studies provided data for meta-analysis (n=2,847 participants).
Meta-analysis using random effects model yielded a pooled relative risk
of 1.35 (95% CI: 1.15-1.59, p<0.001) favoring [intervention] over
control (Figure 2).

Heterogeneity:
Heterogeneity was moderate (I² = 48%, p=0.02). Meta-regression analysis
revealed that heterogeneity decreased with more recent publication year
(coefficient: 0.05 per year, p=0.03).

Subgroup Analyses:
Effects varied by study design:
- RCTs (n=6): RR = 1.48 (95% CI: 1.25-1.75)
- Observational (n=5): RR = 1.15 (95% CI: 0.92-1.43)

Effects appeared consistent across age groups (p for interaction = 0.32).

Publication Bias:
The funnel plot showed modest asymmetry (p=0.08 by Egger's test),
suggesting possible publication bias toward positive results.

Sensitivity Analysis:
Results remained robust when restricting to studies with low risk of bias
(n=7, RR=1.39, 95% CI: 1.18-1.65), suggesting publication bias unlikely
to substantially affect conclusions.
```

## 3. Framework Synthesis (Thematic Synthesis)

### Definition
Use conceptual framework to organize and integrate findings.

### When to Use
- Mixed methods evidence
- Complex interventions with multiple components
- Theory-driven reviews
- Exploring mechanisms and contextual factors

### Process

#### Step 1: Define Analytical Framework

Create conceptual model of how concepts relate:

```
Example: Barriers to Treatment Adherence

INDIVIDUAL FACTORS
├─ Knowledge/understanding of treatment
├─ Perceived efficacy
├─ Motivation/readiness
└─ Self-efficacy

TREATMENT FACTORS
├─ Side effects/tolerability
├─ Frequency/complexity of dosing
├─ Cost
└─ Accessibility

SOCIAL/CONTEXT FACTORS
├─ Family/social support
├─ Healthcare provider relationship
├─ Cultural beliefs/practices
└─ Environmental constraints

OUTCOMES
└─ Medication adherence
    ├─ Near-term: Persistence
    └─ Long-term: Medication possession ratio
```

#### Step 2: Code Findings to Framework

Map findings to framework categories:

```
Study A findings → Knowledge/understanding factor
Study B findings → Side effects factor
Study C findings → Provider relationship factor
Study D findings → Cost factor

Results:
Individual factors: 8 studies
Treatment factors: 12 studies
Social factors: 5 studies
```

#### Step 3: Synthesize Within Categories

Integrate findings for each framework element:

```
KNOWLEDGE/UNDERSTANDING FACTOR

Five studies examined patient understanding of [treatment].

Smith et al. (2020): 45% of patients could not identify
  indication for medication; associated with non-adherence

Jones et al. (2021): Educational intervention improved understanding
  by 60% and adherence by 35%

Brown et al. (2019): Limited understanding correlated with
  discontinuation (r=0.45, p<0.001)

Synthesis: Limited treatment knowledge appears associated with poor
adherence; targeted education shows promise for improvement.
```

#### Step 4: Integrate Across Categories

Show how framework elements interact:

```
SYNTHESIS

Treatment adherence influenced by multiple interconnected factors:

1. KNOWLEDGE-EFFICACY PATHWAY
   Poor understanding → Low perceived efficacy → Non-adherence
   (Evidence: 5 studies support this pathway)

2. SIDE EFFECTS-SUPPORT PATHWAY
   Significant side effects → Less social support → Non-adherence
   (Evidence: 3 studies show side effects reduce support-seeking)

3. COMPLEX TREATMENT-MOTIVATION PATHWAY
   Complex regimens → Reduced motivation → Poor adherence
   (Evidence: Multiple studies support this)

INTEGRATED MODEL:
Adherence results from complex interaction of:
- Individual capacity (knowledge, motivation, self-efficacy)
- Treatment characteristics (acceptability, complexity, effectiveness)
- Social resources (support, relationships, environmental structure)

Interventions addressing single factor show modest effects (10-20%
improvement); combined interventions addressing multiple factors
show larger effects (30-50% improvement).
```

## 4. Critical Interpretive Synthesis (CIS)

### Definition
Deep interpretive synthesis that goes beyond reporting studies to develop new understanding.

### When to Use
- Complex, context-dependent phenomena
- Diverse methodologies and perspectives
- Goal is theory-building
- Need to reconcile apparently contradictory findings

### Process

#### Step 1: Identify Key Interpretations

What do different studies interpret from evidence?

```
Question: Why do some patients benefit from [intervention] while
others don't?

Study A interpretation: Individual differences in baseline severity
determine response

Study B interpretation: Motivation and engagement differences explain
variation

Study C interpretation: Timing and context of intervention matter

Study D interpretation: Multiple mechanisms operate simultaneously
```

#### Step 2: Examine Underlying Assumptions

What assumptions shape different interpretations?

```
Study A assumes: Linear dose-response relationship
Study B assumes: Psychological factors paramount
Study C assumes: Contextual factors modifiable
Study D assumes: Multiple pathways possible

Examining assumptions reveals why interpretations differ
even when results similar
```

#### Step 3: Develop Integrative Interpretation

Create new synthesis that incorporates different perspectives:

```
INTEGRATIVE INTERPRETATION

Rather than a single explanation for variable treatment response,
evidence suggests multiple interacting mechanisms:

1. BIOLOGICAL MECHANISM
   - Treatment may work better in patients with [biomarker X]
   - 3 studies show biomarker association with response
   - Mechanism: [biological pathway]

2. PSYCHOLOGICAL MECHANISM
   - Treatment response enhanced by therapeutic alliance
   - 5 studies show alliance-outcome correlation
   - Mechanism: Enhanced engagement, adherence, expectancy

3. CONTEXTUAL MECHANISM
   - Real-world settings show different outcomes than RCTs
   - Environmental supports/barriers modify treatment effect
   - Mechanism: Sustainability, implementation fidelity

4. TEMPORAL MECHANISM
   - Treatment response may be time-dependent
   - Early response predicts long-term outcomes
   - Mechanism: Different neural processes at different timepoints

PROPOSED MODEL:
Treatment response depends on optimization across multiple levels:
- Right biological target (baseline severity, biomarker status)
- Right psychological/behavioral approach (motivation, engagement)
- Right contextual supports (environmental structure, family support)
- Right timing (when intervention administered)

This multidimensional model explains why unimodal interventions
show variable effectiveness; suggests future research and
practice should optimize across all dimensions.
```

## 5. Realist Synthesis

### Definition
Systematic review method examining "how," "why," and "for whom" interventions work.

### When to Use
- Complex interventions with context-dependent outcomes
- Mechanisms poorly understood
- Need to understand implementation factors
- Heterogeneous populations and settings

### Key Concepts

**Program theory**: Hypotheses about how intervention works

**Causal mechanisms**: Underlying processes that produce outcomes

**Context**: Conditions that enable or inhibit mechanisms

**Outcomes**: Changes produced by mechanisms in specific contexts

### Process

#### Step 1: Develop Initial Program Theory

```
PROGRAM THEORY FOR [INTERVENTION]

Assumed mechanism:
If patients understand [mechanism] AND feel motivated to change
THEN they will engage in [behavior]
AND this will lead to [outcome]

Context required:
- Access to information
- Supportive environment
- Adequate resources
- Healthcare provider support

Outcomes:
- Short-term: Behavioral engagement
- Medium-term: Habit formation
- Long-term: Sustained behavior change
```

#### Step 2: Search for Evidence on Mechanism

Look for evidence addressing "how does this work?"

```
Questions to address:
- What conditions enable mechanism to work?
- What conditions prevent mechanism from working?
- For whom does mechanism work best?
- How does context modify mechanism?
- Are there unintended consequences?
```

#### Step 3: Analyze Evidence for Mechanism

Extract mechanism-focused findings:

```
MECHANISM: Understanding + Motivation → Behavioral Engagement

Supporting evidence:
- Study A: Participants with high understanding (n=50) showed
  higher engagement (85%) vs. low understanding (45%)

- Study B: Motivation level predicted engagement
  (r=0.62, p<0.001)

- Study C: Combined understanding + motivation showed
  synergistic effect (interaction p=0.02)

Contextual modifiers:
- Study D: Education-only interventions (understanding without
  motivation support) showed minimal effect (10% engagement)

- Study E: Motivation interventions without information
  not sustained long-term

- Study F: Combined approach with ongoing support most effective

Unexpected findings:
- Study G: Some highly educated participants showed low engagement
  due to perceived lack of relevance

- Study H: Motivation without resources insufficient
```

#### Step 4: Refine Program Theory

Update understanding based on evidence:

```
REFINED PROGRAM THEORY

Understanding AND Motivation AND Resources → Engagement → Outcomes

Mechanisms:
1. Information pathway: Understanding enables informed decisions
2. Motivational pathway: Motivation sustains effort
3. Resource pathway: Accessible resources remove barriers

Critical contexts:
- Access to information (education level, literacy, language)
- Supportive relationships (provider support, family support)
- Material resources (cost, time, accessibility)
- Environmental fit (cultural appropriateness, practical feasibility)

For whom:
- Works best: Motivated individuals with adequate resources
- Moderate: Those lacking one component (can be supported)
- Limited: Those lacking multiple components (need systematic support)

Outcomes:
- Engagement: Needed for any benefit
- Behavior change: Depends on adequate engagement
- Sustained change: Requires ongoing support
```

## Synthesis Quality Checklist

- [ ] Clear research question for synthesis
- [ ] Systematic, documented search strategy
- [ ] Appropriate study selection criteria applied
- [ ] Study quality assessed and integrated into synthesis
- [ ] All relevant data extracted and organized
- [ ] Synthesis method appropriate for evidence type
- [ ] Heterogeneity examined and explained
- [ ] Contradictions addressed transparently
- [ ] Findings contextualized with existing knowledge
- [ ] Limitations of synthesis acknowledged
- [ ] Clear distinction between findings and interpretation
- [ ] Strength of evidence indicated
- [ ] Conclusions supported by evidence presented

---

**For specific techniques, see SKILL.md. For quick templates, see QUICK_REFERENCE.md.**
