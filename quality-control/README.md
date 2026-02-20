# Quality Control

Process capability and quality metrics calculators for manufacturing and Six Sigma.

## 📊 Calculators

### 1. Cpk Calculator
**File**: `CpkCalculator.html`

**Features**:
- Process capability indices:
  - **Cp** (Potential capability)
  - **Cpk** (Actual capability)
  - **Pp** (Performance potential)
  - **Ppk** (Performance actual)
- Control chart integration
- Defect rate estimation (PPM)
- Sigma level calculation

### Process Capability Metrics

#### Cp (Process Capability)
```
Cp = (USL - LSL) / (6σ)
```
- Measures potential capability
- Assumes process is centered
- Values: Cp ≥ 1.33 considered capable

#### Cpk (Process Capability Index)
```
Cpk = min[(USL - μ) / (3σ), (μ - LSL) / (3σ)]
```
- Measures actual capability
- Accounts for process centering
- Most commonly used index

#### Pp & Ppk (Performance Indices)
- Long-term process performance
- Based on overall variation
- Includes all sources of variation

## 🎯 Applications

### Manufacturing
- Production process monitoring
- Quality assurance
- Specification verification
- Continuous improvement

### Six Sigma
- DMAIC phase analysis
- Process capability studies
- Control plan development
- Defect reduction

### Industries
- Automotive (IATF 16949)
- Aerospace (AS9100)
- Medical devices (ISO 13485)
- General manufacturing (ISO 9001)

## 📈 Capability Interpretation

| Cpk Value | Capability Level | Sigma Level | DPMO |
|-----------|------------------|-------------|------|
| < 1.00    | Inadequate       | < 3σ        | > 66,807 |
| 1.00-1.33 | Marginal         | 3σ          | 66,807 |
| 1.33-1.67 | Adequate         | 4σ          | 6,210 |
| 1.67-2.00 | Good             | 5σ          | 233 |
| ≥ 2.00    | Excellent        | 6σ          | 3.4 |

## 🔧 Input Requirements

- **Process data**: Sample measurements
- **Specification limits**: USL (Upper), LSL (Lower)
- **Sample size**: Minimum 30 observations recommended
- **Distribution**: Assumes normal distribution

## 📊 Visualizations

- Process distribution curve
- Specification limits overlay
- Capability histogram
- Control charts (optional)

## 📚 Standards

Compliant with:
- AIAG SPC Manual
- ISO 22514 (Statistical Process Control)
- ASQC/AIAG guidelines
- Six Sigma methodology

## 🎓 Best Practices

1. **Verify normality**: Use Anderson-Darling or Shapiro-Wilk test
2. **Stable process**: Ensure process is in statistical control
3. **Adequate sample size**: Minimum 30 data points
4. **Correct sigma**: Use within-subgroup or overall variation
5. **Regular monitoring**: Update capability studies periodically

## 🔗 Integration

Can be used:
- Standalone for capability analysis
- Integrated with SPC software
- Embedded in quality management systems
- Part of statistical analysis workflows

## 📖 References

- Montgomery, D.C. (2012). "Statistical Quality Control"
- AIAG (2005). "Statistical Process Control (SPC) Reference Manual"
- Pyzdek, T. (2003). "The Six Sigma Handbook"
