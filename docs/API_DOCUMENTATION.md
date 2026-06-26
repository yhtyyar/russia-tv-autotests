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
