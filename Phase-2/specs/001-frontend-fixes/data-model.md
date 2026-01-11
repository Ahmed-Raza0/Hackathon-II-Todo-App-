# Data Model: Frontend Components for Todo Application

## UI Components Overview

### TaskCard Component
- **Purpose**: Displays individual tasks with ability to mark as complete/incomplete
- **Fields**:
  - title (string): Task title text
  - completed (boolean): Completion status
  - createdAt (timestamp): Date/time created
- **States**:
  - Editing state
  - Confirmation state for deletion
  - Loading states for toggle/delete operations
- **Relationships**: Belongs to a user context

### Button Component
- **Purpose**: Reusable button element with consistent styling
- **Variants**:
  - Primary: For main actions
  - Secondary: For alternative actions
  - Danger: For destructive actions
  - Ghost: For subtle actions
- **Properties**:
  - variant (string): Type of button
  - size (string): Size of button (sm, md, lg)
  - disabled (boolean): Whether button is clickable
  - loading (boolean): Whether button is in loading state

### Input Component
- **Purpose**: Reusable input element with consistent styling and validation
- **Properties**:
  - label (string): Label text
  - error (string): Error message
  - helperText (string): Additional helper text
  - id (string): Unique identifier
- **Validation**: Built-in error display and helper text support

### Navbar Component
- **Purpose**: Navigation bar displayed on authenticated pages
- **Elements**:
  - App title/logo
  - Logout button
- **State**: Shows only for authenticated users

## Styling Architecture

### CSS Custom Properties (Variables)
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