# Distribution Calculator Standardization Guide

## Overview
This guide explains how to use the common CSS file (`calculator-common.css`) to ensure all distribution calculators have consistent styling, colors, and structure.

## Quick Setup

### 1. Link the Common CSS
Add this line in the `<head>` section of your calculator HTML, right after the Font Awesome link:

```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet"/>
<link href="calculator-common.css" rel="stylesheet"/>
```

### 2. Required HTML Structure
Your calculator must follow this structure:

```html
<body style="margin: 0; overflow: hidden;">
    <div style="width: 100vw; height: 100vh; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div id="mainContentWrapper" style="width: 90%; max-width: 1200px; height: auto;">
            <div class="container">
                <!-- Header -->
                <div class="header">
                    <h1><i class="fas fa-chart-line"></i> Calculator Name</h1>
                </div>
                
                <!-- Main Content Grid -->
                <div class="main-content">
                    <!-- Result Hero (Top Right) -->
                    <div class="result-hero">
                        <!-- Precision selector and main result -->
                    </div>
                    
                    <!-- Control Panel (Left Side) -->
                    <div class="control-panel">
                        <!-- Inputs and controls -->
                    </div>
                    
                    <!-- Visualization Panel (Bottom Right) -->
                    <div class="visualization-panel">
                        <!-- Charts and tabs -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
```

## What's Included in Common CSS

### ✅ Standardized Elements
- **Color scheme** (warm orange & cyan blue)
- **Layout grid** (3-area: controlPanel, resultHero, vizPanel)
- **Result-hero section** with glowing animations
- **Input fields** with consistent styling
- **Buttons** (primary, success, ghost)
- **Radio options** for calculation types
- **Tabs** with switching animations
- **Stats grids** and embedded results
- **Chart containers** with Highcharts dark theme
- **Responsive breakpoints** for mobile/tablet

### 🎨 Color Variables
All colors are centralized in CSS variables:
- `--accent-1`: rgb(255,165,120) (warm orange)
- `--accent-2`: rgb(120,200,255) (cyan blue)
- `--surface-0`: #0c1624 (background)
- `--surface-1`: #1a1f2e (panels)
- `--surface-2`: #242938 (chart boxes)

### ⚙️ Calculator-Specific Styles
Keep these in individual calculator files:
- Distribution-specific calculations (JavaScript)
- Unique input fields for that distribution
- Custom tooltips or help text
- About modal content
- Special chart configurations

## Default Settings

### Precision Selector
Default to **3 decimals**:
```html
<select class="mini-dropdown" id="precision">
    <option value="2">2</option>
    <option value="3" selected>3</option>
    <option value="4">4</option>
    <option value="5">5</option>
    <option value="6">6</option>
</select>
```

### Stats Grid Layout
For calculators with **5 statistics**, use the default 5-column grid (already in common CSS).

For calculators with **different numbers of stats**, add this in your calculator-specific styles:
```css
.embedded-stats-grid {
    grid-template-columns: repeat(3, 1fr); /* Or adjust as needed */
}
```

## Migration Checklist

When converting an existing calculator:

- [ ] Remove duplicate CSS from calculator file
- [ ] Add `<link>` to `calculator-common.css`
- [ ] Ensure HTML structure matches standard layout
- [ ] Move result display to result-hero section
- [ ] Update IDs: `mainResult`, `heroExpression`, `areaValue`, `explanationLine`
- [ ] Set precision default to 3
- [ ] Test responsive layouts on mobile
- [ ] Verify all animations work
- [ ] Test calculation functions still work

## Benefits

✨ **Consistency**: All calculators look and feel identical  
🚀 **Maintainability**: Update styles in one place  
📱 **Responsive**: Mobile-friendly out of the box  
🎨 **Modern**: Beautiful gradient effects and animations  
⚡ **Performance**: Cached CSS loads faster  

## Support

If you encounter issues or need to add new common styles, update `calculator-common.css` and document the changes here.

---
**Version**: 2.0  
**Last Updated**: December 2024  
**Applies to**: All Distribution Calculators

