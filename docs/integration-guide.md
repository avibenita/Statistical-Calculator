# Integration Guide

How to integrate calculators with the Statistico Analytics Office Add-in and other applications.

## Overview

The calculator suite is designed with two use cases:
1. **Standalone**: Direct access via web browser
2. **Integrated**: Embedded in other applications

## Integration Architecture

```
┌─────────────────────────────────────┐
│   Statistico Analytics Add-in       │
│   (Excel/Word Office Add-in)        │
├─────────────────────────────────────┤
│         Results Dialogs             │
│    ┌──────────────────────────┐    │
│    │   Power Tab              │    │
│    │   (embedded calculator)  │◄───┼─── Power Calculator Module
│    └──────────────────────────┘    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   Statistical Calculator Suite      │
├─────────────────────────────────────┤
│ • Power Calculators                 │
│ • Distribution Calculators          │
│ • Erlang Simulation                 │
│ • Quality Control                   │
└─────────────────────────────────────┘
```

## Power Calculator Integration

### Method 1: IFrame Embedding

```html
<iframe 
  src="power-calculators/SampleSizeCalculator.html"
  width="100%"
  height="600px"
  frameborder="0"
  id="powerCalculator">
</iframe>
```

### Method 2: Direct Module Import

```javascript
// In your application's JavaScript
const powerCalc = {
  calculateSampleSize: function(params) {
    // Import calculation logic
    const { alpha, power, effectSize, testType } = params;
    // ... calculation code
    return { sampleSize, totalN, actualPower };
  }
};

// Call from statistico-analytics
const result = powerCalc.calculateSampleSize({
  alpha: 0.05,
  power: 0.80,
  effectSize: 0.5,
  testType: 'two-sample-mean'
});
```

### Method 3: PostMessage API

```javascript
// In Statistico Analytics Add-in
const iframe = document.getElementById('powerCalculator');
iframe.contentWindow.postMessage({
  action: 'calculate',
  params: {
    mode: 'sample-size-power',
    alpha: 0.05,
    power: 0.80,
    effectSize: 0.5,
    testType: 'anova',
    numGroups: 3
  }
}, '*');

// Listen for results
window.addEventListener('message', (event) => {
  if (event.data.type === 'calculation-complete') {
    const { sampleSize, actualPower } = event.data.result;
    displayResults(sampleSize, actualPower);
  }
});

// In Calculator (add this to SampleSizeCalculator.html)
window.addEventListener('message', (event) => {
  if (event.data.action === 'calculate') {
    const result = performCalculation(event.data.params);
    window.parent.postMessage({
      type: 'calculation-complete',
      result: result
    }, '*');
  }
});
```

## Distribution Calculator Integration

### Use Case: Hypothesis Testing Support

```javascript
// Get p-value from t-distribution
function calculatePValue(tStatistic, df, tails = 2) {
  // Call t-distribution calculator module
  const tDist = new TDistribution(df);
  const pValue = tails === 2 
    ? 2 * (1 - tDist.cdf(Math.abs(tStatistic)))
    : 1 - tDist.cdf(tStatistic);
  return pValue;
}

// Example: In repeated measures ANOVA
const tStat = 2.45;
const degreesOfFreedom = 18;
const pValue = calculatePValue(tStat, degreesOfFreedom, 2);
```

## Shared Resource Management

### CSS Theming

```css
/* calculator-common.css */
:root {
  --primary-color: #5c6bc0;
  --accent-color: #ff9800;
  --success-color: #4caf50;
  --error-color: #f44336;
}

/* Override in parent application */
<style>
  #powerCalculator {
    --primary-color: #7e22ce; /* Match statistico-analytics purple */
  }
</style>
```

### Data Exchange Format

```javascript
// Standard result format for all calculators
const standardResult = {
  status: 'success' | 'error',
  calculator: 'power' | 'distribution' | 'erlang' | 'quality',
  timestamp: new Date().toISOString(),
  inputs: {
    // Input parameters
  },
  outputs: {
    // Calculation results
  },
  metadata: {
    version: '1.0.0',
    algorithm: 'description'
  }
};
```

## Configuration API

### Power Calculator Configuration

```javascript
// Configure calculator for specific needs
const config = {
  enabledTests: ['anova', 'regression', 'correlation'],
  defaultAlpha: 0.05,
  defaultPower: 0.80,
  showAdvancedOptions: true,
  theme: 'statistico-analytics',
  language: 'en'
};

// Apply configuration
powerCalculator.configure(config);
```

## Workflow Integration

### Example: Post-Analysis Power

```javascript
// After running ANOVA in statistico-analytics
const analysisResult = {
  testType: 'anova',
  numGroups: 3,
  sampleSize: 34, // n per group
  effectSize: 1.57, // Cohen's f
  alpha: 0.05
};

// Calculate achieved power
const achievedPower = powerCalc.calculatePowerGivenN(analysisResult);

// Display in results dialog
showPowerTab({
  power: achievedPower,
  interpretation: generatePowerInterpretation(achievedPower)
});
```

## Security Considerations

### Same-Origin Policy

When embedding in Office Add-ins:
```xml
<!-- manifest.xml -->
<AppDomains>
  <AppDomain>https://your-calculator-domain.com</AppDomain>
</AppDomains>
```

### Content Security Policy

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';">
```

## Performance Optimization

### Lazy Loading

```javascript
// Load calculator only when needed
async function loadPowerCalculator() {
  if (!window.powerCalculatorLoaded) {
    await import('./power-calculators/calculator-engine.js');
    window.powerCalculatorLoaded = true;
  }
}
```

### Caching Results

```javascript
const calculationCache = new Map();

function getCachedOrCalculate(params) {
  const cacheKey = JSON.stringify(params);
  if (calculationCache.has(cacheKey)) {
    return calculationCache.get(cacheKey);
  }
  const result = performCalculation(params);
  calculationCache.set(cacheKey, result);
  return result;
}
```

## Testing Integration

### Unit Tests

```javascript
// test-integration.js
describe('Power Calculator Integration', () => {
  it('should calculate ANOVA sample size correctly', () => {
    const result = powerCalc.calculateSampleSize({
      testType: 'anova',
      numGroups: 3,
      effectSize: 1.57,
      alpha: 0.05,
      power: 0.80
    });
    expect(result.sampleSize).toBe(34);
  });
});
```

## Version Compatibility

| Calculator Version | Statistico Analytics Version | Status |
|-------------------|------------------------------|--------|
| 1.0.x             | 1.0.x - 1.2.x               | ✅ Compatible |
| 1.1.x             | 1.2.x+                      | ✅ Recommended |

## Support

For integration support:
- Check the main README.md
- Review example implementations in `docs/examples/`
- Contact: [your-email]

## Changelog

### Version 1.1.0
- Added PostMessage API for cross-origin communication
- Improved power curve generation
- Added non-parametric test support

### Version 1.0.0
- Initial release
- Basic integration support
