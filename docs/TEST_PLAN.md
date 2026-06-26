# Test Plan: russia-tv.online

## Scope

Testing covers the online TV guide at https://russia-tv.online/ including:
- Home page with channel grid
- Category filtering
- Date-based schedule navigation
- Search functionality
- Channel detail pages
- Responsive design

## Test Levels

### Unit Tests
- Date formatting utilities
- Data model validation
- Input validators

### Integration Tests
- `/api/schedule` — schedule by date
- `/api/channels` — channel lists and details
- `/api/search` — search queries
- JSON schema validation

### E2E Tests
- Home page load and channel display
- Category filter interaction
- Date navigation (today/yesterday/tomorrow)
- Search input and results
- Cross-browser compatibility
- Responsive breakpoints

## Browsers
- Chromium (primary)
- Firefox
- WebKit (optional)

## Environments
- Production: https://russia-tv.online/
- Staging: (configured in `config/environments.py`)
- Dev: (configured in `config/environments.py`)
