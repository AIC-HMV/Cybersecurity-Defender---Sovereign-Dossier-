# Real-Time 3D Audit Event Map

**Author:** Hung Minh Vo (Austin) | AIC-HMV  
**Origin ID:** HMV-SOV-20251003-ALL  
**Purpose:** Living HD 3D visualization of audit events with geolocation and live weather overlay

## Overview

High-performance, self-hosted real-time visualization system that streams audit events to an interactive 3D globe with weather overlays, animated markers, and defensive monitoring capabilities.

## Features

### Backend (FastAPI + WebSocket)
- **Audit Event Streaming** - Polls PostgreSQL audit DB or accepts inbound events
- **Offline IP Geolocation** - MaxMind GeoLite2 local database (no external lookups)
- **Live Weather Integration** - OpenWeatherMap API with configurable caching (300s TTL)
- **WebSocket Broadcasting** - Push events to all connected clients in real-time
- **Performance Optimized** - Event deduplication, weather caching, compact JSON frames

### Frontend (Mapbox GL / MapLibre)
- **3D Globe Rendering** - High-quality terrain and building visualization
- **Animated Markers** - Smooth animations for event locations with fade-out
- **Temperature Heat Layer** - Color-coded temperature overlay
- **Side Panel Dashboard** - Live event feed with scrolling history
- **Auto-Reconnect** - Resilient WebSocket with exponential backoff
- **Responsive Design** - Works on desktop and mobile

### Security & Compliance
- **Defensive Only** - All operations lawful, non-violent, authorized monitoring
- **Self-Hosted** - No external dependencies except optional weather API
- **Privacy Preserving** - Local GeoIP lookups, no third-party tracking
- **Audit Trail** - All events logged with timestamps and sources

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PostgreSQL Audit DB                      │
│  (frozen_audit.py writes signed events with IP addresses)   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server (server.py)                │
│  - Polls audit DB every 5s for new events                   │
│  - MaxMind GeoLite2 City DB → lat/lon lookup (offline)     │
│  - OpenWeatherMap API → temperature (cached 5 min)          │
│  - WebSocket broadcaster → pushes events to clients          │
└────────────────┬────────────────────────────────────────────┘
                 │ WebSocket (ws://localhost:8765)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Web Client (static/map.html)                    │
│  - Mapbox GL JS or MapLibre GL for 3D rendering             │
│  - Animated markers with pulsing effect                     │
│  - Temperature heatmap overlay                               │
│  - Live event feed sidebar                                   │
│  - Auto-reconnect on disconnect                              │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

1. **Python 3.9+**
2. **PostgreSQL 14+** with audit database
3. **MaxMind GeoLite2 City Database**
   - Download from https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
   - Extract to `/data/GeoLite2-City.mmdb` (or configure path in `.env`)
4. **OpenWeatherMap API Key** (optional, for weather overlay)
   - Sign up at https://openweathermap.org/api
5. **Mapbox Token** (optional, for Mapbox GL)
   - Get free token at https://www.mapbox.com/
   - Or use MapLibre GL (no token required)

### Setup

1. **Clone and navigate to directory:**
```bash
cd real-time-audit-map
```

2. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database URL, MaxMind path, API keys
```

4. **Run server:**
```bash
python3 server.py
```

5. **Open browser:**
```
http://localhost:8080/map.html
```

## Configuration

### Environment Variables (.env)

```bash
# Database connection
AUDIT_DB_URL=postgresql://audituser:auditpass@localhost:5432/auditdb

# MaxMind GeoIP database (download GeoLite2-City.mmdb)
MAXMIND_DB_PATH=/data/GeoLite2-City.mmdb

# OpenWeatherMap API key (leave blank to disable weather)
OPENWEATHER_KEY=your_openweather_api_key

# Mapbox token (leave blank to use MapLibre)
MAPBOX_TOKEN=your_mapbox_token

# Server configuration
POLL_INTERVAL=5          # Poll database every N seconds
WEATHER_CACHE_TTL=300    # Cache weather data for N seconds
WS_PORT=8765            # WebSocket port
HTTP_PORT=8080          # HTTP server port
```

## Usage

### Starting the Server

```bash
# Development mode with auto-reload
uvicorn server:app --reload --host 0.0.0.0 --port 8080

# Production mode
python3 server.py
```

### Accessing the Map

Navigate to `http://localhost:8080/map.html` in a modern browser (Chrome, Firefox, Safari, Edge).

### Features in Action

1. **Real-Time Events** - New audit events appear as animated markers on the globe
2. **Click Markers** - Click any marker to see event details
3. **Temperature Overlay** - Toggle temperature heatmap in controls
4. **Event Feed** - Scrollable sidebar shows last 100 events
5. **3D Navigation** - Drag to rotate, scroll to zoom, shift+drag to tilt

## Performance Optimization

### Backend Optimizations

1. **Event Deduplication** - Hash-based dedup prevents duplicate markers
2. **Weather Caching** - 5-minute TTL reduces API calls
3. **Connection Pooling** - PostgreSQL connection pool for efficiency
4. **Async Operations** - Non-blocking I/O with asyncio

### Frontend Optimizations

1. **Marker Clustering** - Group nearby markers at low zoom levels
2. **Marker Culling** - Remove old markers after 5 minutes (configurable)
3. **Lazy Loading** - Load map tiles on demand
4. **WebGL Rendering** - Hardware-accelerated 3D graphics
5. **Binary Frames** - Consider MessagePack for high-frequency updates (see code comments)

### Scaling for High Volume

For >1000 events/minute:

1. **Vector Tiles** - Pre-render event density as vector tiles
2. **Binary Protocol** - Switch WebSocket to MessagePack
3. **Edge Caching** - CDN for static assets
4. **Load Balancing** - Multiple server instances behind nginx
5. **Redis Pub/Sub** - Decouple event ingestion from broadcasting

## Deployment

### SystemD Service

Create `/etc/systemd/system/audit-map-server.service`:

```ini
[Unit]
Description=Real-Time Audit Map Server
After=network.target postgresql.service

[Service]
Type=simple
User=cea-audit
WorkingDirectory=/opt/core7/real-time-audit-map
EnvironmentFile=/opt/core7/real-time-audit-map/.env
ExecStart=/usr/bin/python3 server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable audit-map-server
sudo systemctl start audit-map-server
```

### Nginx Reverse Proxy

```nginx
upstream audit_map_ws {
    server localhost:8765;
}

upstream audit_map_http {
    server localhost:8080;
}

server {
    listen 443 ssl;
    server_name auditmap.ceasentinel.com;

    ssl_certificate /etc/letsencrypt/live/auditmap.ceasentinel.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/auditmap.ceasentinel.com/privkey.pem;

    location /ws {
        proxy_pass http://audit_map_ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    location / {
        proxy_pass http://audit_map_http;
    }
}
```

## Security Considerations

### Access Control

1. **Authentication** - Add API key or OAuth to WebSocket endpoint
2. **Rate Limiting** - Limit connections per IP
3. **IP Whitelisting** - Restrict to authorized networks
4. **HTTPS Only** - Enforce TLS in production

### Data Privacy

1. **Anonymization** - Hash or truncate sensitive IP addresses before display
2. **Access Logs** - Log all client connections with timestamps
3. **Event Filtering** - Only stream authorized event types to clients
4. **Encryption** - Use WSS (WebSocket Secure) in production

### Compliance

1. **GDPR** - Document data processing, retention policies
2. **Audit Trail** - Log all map access in audit database
3. **Data Minimization** - Only collect necessary geolocation data
4. **Right to Access** - Provide mechanism to query stored events

## Troubleshooting

### WebSocket Connection Fails

```bash
# Check server is running
sudo systemctl status audit-map-server

# Check WebSocket port is open
sudo netstat -tlnp | grep 8765

# Check firewall rules
sudo ufw status
```

### No Events Appearing

```bash
# Check database connectivity
psql $AUDIT_DB_URL -c "SELECT COUNT(*) FROM audit_log;"

# Check server logs
journalctl -u audit-map-server -f

# Verify events have IP addresses
psql $AUDIT_DB_URL -c "SELECT event_data->>'ip' FROM audit_log LIMIT 10;"
```

### GeoIP Lookup Errors

```bash
# Verify MaxMind database exists
ls -lh /data/GeoLite2-City.mmdb

# Test GeoIP lookup
python3 -c "import geoip2.database; reader = geoip2.database.Reader('/data/GeoLite2-City.mmdb'); print(reader.city('8.8.8.8'))"
```

### Weather API Rate Limiting

```bash
# Check API key is valid
curl "https://api.openweathermap.org/data/2.5/weather?lat=33.6&lon=-117.7&appid=$OPENWEATHER_KEY"

# Increase cache TTL in .env
WEATHER_CACHE_TTL=600  # 10 minutes
```

## License

AIC-HMV Sovereign License v3  
Origin ID: HMV-SOV-20251003-ALL  
Author: Hung Minh Vo (Austin)

All code is provided for defensive, lawful, non-violent purposes only. Unauthorized use, modification, or distribution triggers sovereign trace and enforcement protocols.

## Support

For issues, questions, or contributions:
- Email: aichmvprimeowner@gmail.com
- Repository: https://github.com/AIC-HMV/Cybersecurity-Defender---Sovereign-Dossier-

---

**System is sovereign. Collapse-resistant. Unstoppable.**
