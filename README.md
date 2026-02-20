# Statistical Calculators Suite

A comprehensive collection of statistical calculators for power analysis, probability distributions, quality control, and simulation.

## 📁 Repository Structure

```
├── power-calculators/          # Power & Sample Size Analysis
│   ├── SampleSizeCalculator.html
│   ├── PrecisionSampleCalculator.html
│   └── README.md
│
├── statistical-distributions/  # Probability Distribution Calculators
│   ├── Normal.html
│   ├── TDistribution.html
│   ├── ChiSquare.html
│   └── README.md
│
├── erlang-simulation/         # Erlang Queuing & Simulation
│   ├── Erlang_SimpleAndSimulation.html
│   └── README.md
│
├── quality-control/           # Quality Control & Process Capability
│   ├── CpkCalculator.html
│   └── README.md
│
├── assets/                    # Shared Resources
│   ├── calculator-common.css
│   └── TEMPLATE_Calculator.html
│
├── docs/                      # Documentation
│   └── integration-guide.md
│
└── index.html                 # Main Hub/Landing Page
```

## 🎯 Calculator Categories

### 1. Power Calculators
**Purpose**: Sample size and statistical power analysis

**Standalone Use**: Researchers planning studies
**Integration**: Serves the `statistico-analytics` module with power calculations

**Files**:
- `SampleSizeCalculator.html` - Main power/sample size calculator
- `PrecisionSampleCalculator.html` - Precision-based sample size (MOE)

### 2. Statistical Distributions
**Purpose**: Probability distribution calculations and visualizations

**Standalone Use**: Educational tools and probability calculations
**Integration**: Can be embedded in statistical analysis workflows

**Files**: 13 distribution calculators (Normal, t, F, Chi-square, etc.)

### 3. Erlang & Simulation
**Purpose**: Queuing theory and traffic modeling

**Standalone Use**: Telecommunications and operations research
**Integration**: Independent module

**Files**:
- `Erlang_SimpleAndSimulation.html` - Erlang B/C with simulation

### 4. Quality Control
**Purpose**: Process capability and quality metrics

**Standalone Use**: Manufacturing and Six Sigma applications
**Integration**: Independent module

**Files**:
- `CpkCalculator.html` - Process capability indices

## 🔗 Integration with Statistico Analytics

The power calculators are designed to integrate with the [statistico-analytics](https://github.com/avibenita/statistico-analytics) Office Add-in:

- Embedded in the "Power" tab of results dialogs
- Provides sample size recommendations
- Calculates achieved power for completed analyses

## 🚀 Quick Start

1. **Standalone Use**: Open `index.html` as the main hub
2. **Integration**: Import specific calculator modules into your application
3. **Development**: Use `TEMPLATE_Calculator.html` as starting point for new calculators

## 📦 Technology Stack

- Pure HTML5/CSS3/JavaScript (no dependencies)
- Responsive design
- Modern statistical algorithms
- Interactive visualizations

## 📝 License

[Your License Here]

## 👥 Author

Avi Benita
