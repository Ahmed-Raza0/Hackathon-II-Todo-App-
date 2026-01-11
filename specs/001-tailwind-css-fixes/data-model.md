# Data Model: UI Components for Tailwind and Global CSS Configuration

## UI Components Overview

### Tailwind Configuration
- **Purpose**: Defines custom theme, colors, spacing, and utility classes
- **Configuration**: Extends default Tailwind with custom color palette and spacing
- **Theme**: Custom indigo/blue primary colors, slate/gray secondary colors
- **Breakpoints**: Standard Tailwind responsive breakpoints

### Global CSS Structure
- **Purpose**: Base styles, resets, and custom CSS that extends Tailwind
- **CSS Variables**: Custom properties for consistent theming across the application
- **Base Styles**: Normalization and reset styles
- **Utility Classes**: Custom utility classes that supplement Tailwind

### CSS Variables (Custom Properties)
- **Color Palette**:
  - Primary colors: Indigo/blue family
  - Secondary colors: Slate/gray-blue family
  - Background: Light gray/off-white
  - Surface: Clean white/slightly warm neutral
  - Success: Muted green
  - Warning: Soft amber/yellow
  - Error: Muted red
  - Text: Near-black charcoal, neutral gray, light gray
  - Borders: Soft neutral gray

### Responsive Breakpoints
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

### Animation Principles
- Subtle transitions for state changes
- Purposeful animations that don't distract
- Reduced motion support for accessibility