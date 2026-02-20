# Power Calculators

Statistical power and sample size calculators for experimental design and study planning.

## 📊 Calculators

### 1. Sample Size & Power Calculator
**File**: `SampleSizeCalculator.html`

**Features**:
- Three calculation modes:
  - **Sample Size** (given power & effect size)
  - **Power** (given sample size & effect size)
  - **Sample Size** (given margin of error)
- Supported tests:
  - One-Sample t-test
  - Two-Sample t-test (independent)
  - One-Sample Proportion
  - Two-Sample Proportions
  - Correlation Analysis
  - One-Way ANOVA
  - Linear Regression
- Interactive power curves
- Effect size visualizations
- Non-parametric alternatives (Wilcoxon, Mann-Whitney)

**Integration**: Can be embedded in the statistico-analytics add-in

### 2. Precision Sample Calculator
**File**: `PrecisionSampleCalculator.html`

**Features**:
- Margin of error (MOE) based calculations
- Confidence interval precision
- Standard error specifications

## 🎯 Use Cases

### Standalone Applications
- Study design and grant proposals
- Pre-registration of clinical trials
- A priori power analysis
- Educational demonstrations

### Integration with Statistico Analytics
The power calculators integrate with the Office Add-in to provide:
- Real-time power recommendations
- Post-hoc power analysis
- Sample size guidance within analysis workflows

## 📐 Statistical Methods

- Exact t-distribution calculations
- Non-central F-distribution for ANOVA
- Fisher's Z transformation for correlations
- Iterative algorithms for complex designs
- Normal approximations where appropriate

## 🔗 API Integration

These calculators can be called programmatically:

```javascript
// Example: Calculate sample size for two-sample t-test
const result = calculateTwoSampleMean(
  alpha = 0.05,
  power = 0.80,
  effectSize = 0.5,
  alternative = 'two-sided'
);
console.log(`Required n per group: ${result.sampleSize}`);
```

## 📚 References

- Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences
- Faul, F., et al. (2007). G*Power 3: A flexible statistical power analysis program
