"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

Real-Time 3D Audit Event Map Server
FastAPI + WebSocket broadcaster with offline GeoIP and live weather

Origin ID: HMV-SOV-20251003-ALL
"""

import os
import time
import json
import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Set, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import geoip2.database
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

# Configuration
AUDIT_DB_URL = os.getenv("AUDIT_DB_URL", "postgresql://audituser:auditpass@localhost:5432/auditdb")
MAXMIND_DB_PATH = os.getenv("MAXMIND_DB_PATH", "/data/GeoLite2-City.mmdb")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))
WEATHER_CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL", "300"))
WS_PORT = int(os.getenv("WS_PORT", "8765"))
HTTP_PORT = int(os.getenv("HTTP_PORT", "8080"))

# Initialize
app = FastAPI(title="Real-Time Audit Map")
app.mount("/static", StaticFiles(directory="static"), name="static")

# State
connected_clients: Set[WebSocket] = set()
seen_events: Set[str] = set()  # Event deduplication
weather_cache: Dict[str, tuple] = {}  # (data, timestamp)
geoip_reader = None
last_processed_id = 0

# Initialize GeoIP reader
try:
    geoip_reader = geoip2.database.Reader(MAXMIND_DB_PATH)
    print(f"✅ GeoIP database loaded: {MAXMIND_DB_PATH}")
except Exception as e:
    print(f"⚠️ GeoIP database not found: {e}")
    print("   Download from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data")


def get_db_connection():
    """Create PostgreSQL connection"""
    return psycopg2.connect(AUDIT_DB_URL, cursor_factory=RealDictCursor)


def geolocate_ip(ip: str) -> Optional[Dict]:
    """Offline IP geolocation using MaxMind DB"""
    if not geoip_reader:
        return None
    
    try:
        response = geoip_reader.city(ip)
        return {
            "lat": response.location.latitude,
            "lon": response.location.longitude,
            "city": response.city.name or "Unknown",
            "country": response.country.name or "Unknown",
            "country_code": response.country.iso_code or "XX"
        }
    except Exception as e:
        print(f"⚠️ GeoIP lookup failed for {ip}: {e}")
        return None


async def fetch_weather(lat: float, lon: float) -> Optional[Dict]:
    """Fetch weather data from OpenWeatherMap API with caching"""
    if not OPENWEATHER_KEY:
        return None
    
    # Cache key: lat,lon rounded to 1 decimal
    cache_key = f"{round(lat, 1)},{round(lon, 1)}"
    
    # Check cache
    if cache_key in weather_cache:
        data, timestamp = weather_cache[cache_key]
        if time.time() - timestamp < WEATHER_CACHE_TTL:
            return data
    
    # Fetch from API
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_KEY,
            "units": "metric"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            weather_data = {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            
            # Update cache
            weather_cache[cache_key] = (weather_data, time.time())
            return weather_data
    except Exception as e:
        print(f"⚠️ Weather API failed for {lat},{lon}: {e}")
        return None


def event_hash(event_data: Dict) -> str:
    """Generate unique hash for event deduplication"""
    key_parts = [
        event_data.get("id", ""),
        event_data.get("ip", ""),
        event_data.get("timestamp", ""),
        event_data.get("event_type", "")
    ]
    return hashlib.md5("|".join(map(str, key_parts)).encode()).hexdigest()


async def poll_audit_db():
    """Poll audit database for new events"""
    global last_processed_id
    
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Query new events since last processed ID
            query = """
                SELECT id, timestamp, event_type, event_data, actor
                FROM audit_log
                WHERE id > %s
                  AND event_data->>'ip' IS NOT NULL
                ORDER BY id ASC
                LIMIT 100
            """
            cursor.execute(query, (last_processed_id,))
            rows = cursor.fetchall()
            
            for row in rows:
                # Extract IP address
                event_data = row["event_data"]
                ip = event_data.get("ip")
                
                if not ip:
                    continue
                
                # Deduplicate
                ev_hash = event_hash(row)
                if ev_hash in seen_events:
                    continue
                seen_events.add(ev_hash)
                
                # Keep seen_events set bounded
                if len(seen_events) > 10000:
                    seen_events.clear()
                
                # Geolocate
                geo = geolocate_ip(ip)
                if not geo:
                    continue
                
                # Fetch weather
                weather = await fetch_weather(geo["lat"], geo["lon"])
                
                # Build event packet
                event_packet = {
                    "id": row["id"],
                    "timestamp": row["timestamp"].isoformat() if row["timestamp"] else None,
                    "event_type": row["event_type"],
                    "actor": row["actor"],
                    "ip": ip,
                    "lat": geo["lat"],
                    "lon": geo["lon"],
                    "city": geo["city"],
                    "country": geo["country"],
                    "country_code": geo["country_code"],
                    "weather": weather
                }
                
                # Broadcast to all connected clients
                await broadcast(event_packet)
                
                # Update last processed ID
                last_processed_id = row["id"]
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Poll error: {e}")
        
        await asyncio.sleep(POLL_INTERVAL)


async def broadcast(event: Dict):
    """Broadcast event to all connected WebSocket clients"""
    if not connected_clients:
        return
    
    message = json.dumps(event)
    disconnected = set()
    
    for client in connected_clients:
        try:
            await client.send_text(message)
        except Exception:
            disconnected.add(client)
    
    # Remove disconnected clients
    connected_clients.difference_update(disconnected)


@app.on_event("startup")
async def startup_event():
    """Start background polling task"""
    asyncio.create_task(poll_audit_db())
    print(f"✅ Server started on port {HTTP_PORT}")
    print(f"✅ WebSocket listening on port {WS_PORT}")
    print(f"✅ Polling audit DB every {POLL_INTERVAL}s")


@app.get("/")
async def root():
    """Serve map HTML"""
    return FileResponse("static/map.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming"""
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(connected_clients)}")


@app.get("/api/config")
async def get_config():
    """Client configuration endpoint"""
    return {
        "mapbox_token": os.getenv("MAPBOX_TOKEN", ""),
        "ws_port": WS_PORT
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "connected_clients": len(connected_clients),
        "last_processed_id": last_processed_id,
        "geoip_loaded": geoip_reader is not None,
        "weather_enabled": bool(OPENWEATHER_KEY)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT)
