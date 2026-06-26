# API Documentation

## Base URL

Production: `https://russia-tv.online/api`

## Endpoints

### GET /schedule

Returns TV schedule for a given date.

**Query Parameters:**
- `date` (string, required): One of `today`, `yesterday`, `tomorrow`, or `YYYY-MM-DD`
- `channel_id` (string, optional): Filter by specific channel

**Response:**
- Status: 200 OK
- Body: JSON with `channels` array

### GET /schedule/current

Returns currently airing programs.

**Response:**
- Status: 200 OK
- Body: JSON with current broadcasts

### GET /channels

Returns list of all channels.

**Query Parameters:**
- `category` (string, optional): Filter by category slug

**Response:**
- Status: 200 OK
- Body: JSON with `channels` array

### GET /channels/{id}

Returns detailed information for a specific channel.

**Response:**
- Status: 200 OK or 404 Not Found

### GET /search

Search channels or programs.

**Query Parameters:**
- `q` (string, required): Search query
- `limit` (integer, optional): Max results (default 20)

**Response:**
- Status: 200 OK
- Body: JSON with `results` array

## Error Handling

The framework uses custom domain exceptions defined in `core/exceptions.py`:

- `APIError` — Base for all API failures (HTTP status, network errors, invalid JSON)
- `ScheduleAPIError` — Schedule-specific failures
- `ChannelAPIError` — Channel-specific failures
- `SearchAPIError` — Search-specific failures

All API calls in `BaseAPI` automatically:
1. Validate HTTP status codes (`raise_for_status`)
2. Catch `httpx.HTTPStatusError` and `httpx.RequestError`
3. Log exceptions via `logging.exception`
4. Re-raise as typed `APIError` with original cause attached

## Note on Site Architecture

`russia-tv.online` is a Nuxt.js SPA with SSR. It does **not** expose a public REST API — the documented endpoints above represent the intended contract that the frontend uses internally. Direct HTTP calls to these endpoints may return HTML (SSR response) rather than JSON, which is why integration tests marked with `xfail` are expected to fail when calling the API directly.

For production testing, prefer:
- **E2E tests** via Playwright for full user journey validation
- **Site availability tests** (`tests/integration/test_site_availability.py`) for HTTP 200 contract checks
