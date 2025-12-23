# Scientific Writing Example: Research Paper Sections

Complete examples of well-written scientific paper sections with before/after comparisons.

---

## Abstract Example

### BEFORE (Weak)

```
We studied machine learning for materials. We used neural networks. 
The results were good. This could be useful.
```

**Problems**: Vague, no quantitative results, missing context

### AFTER (Strong)

```
Predicting mechanical properties of crystalline materials typically requires expensive 
density functional theory (DFT) calculations. Here, we present a graph neural network 
(GNN) architecture that achieves DFT-level accuracy at a fraction of the cost. Our 
model, trained on 186,000 compounds from the Materials Project database, predicts 
elastic moduli with a mean absolute error (MAE) of 8.2 GPa, representing a 42% 
improvement over previous methods. When tested on 15,000 unseen structures, the model 
maintains accuracy while running 1000× faster than DFT. These results demonstrate that 
data-driven approaches can complement traditional physics-based methods for 
high-throughput materials screening.
```

**Strengths**:
- ✅ Clear context and problem
- ✅ Specific method
- ✅ Quantitative results with comparisons
- ✅ Key achievement highlighted
- ✅ Broader impact stated

---

## Introduction Example

### Paragraph 1: Context

**BEFORE**: "Materials science is important. Many people study materials."

**AFTER**: 
```
The discovery of materials with targeted properties remains a central challenge in 
materials science, with applications spanning renewable energy, electronics, and 
structural engineering [1,2]. Traditional approaches rely heavily on experimental 
trial-and-error or time-consuming computational screening using density functional 
theory (DFT) [3]. While DFT has proven remarkably successful, the computational 
cost—often requiring hours to days per compound—severely limits its application to 
high-throughput screening [4].
```

---

## Results Example

**BEFORE**: "Table 1 shows our results. Our method performed well."

**AFTER**:
```
Table 1 presents prediction performance for our model and baselines on the held-out 
test set of 18,644 compounds. Our approach achieves mean absolute errors (MAE) of 
8.2 GPa for bulk modulus, representing a 42% improvement compared to the previous 
state-of-the-art [5]. The coefficient of determination (R²) exceeds 0.94 for all 
properties, indicating that the model captures the majority of variance in the 
target properties.
```

---

## Writing Checklist

### Clarity
- [ ] Every sentence has clear subject and verb
- [ ] Technical terms defined on first use
- [ ] Figures/tables referenced in text

### Precision
- [ ] Quantitative results include units
- [ ] Comparisons specify what is compared
- [ ] Claims supported by data or citations

### Style
- [ ] Primarily active voice
- [ ] Past tense for actions taken
- [ ] Present tense for general truths
