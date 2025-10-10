from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import redis
import json
from datetime import datetime
import os

# Import mock data en alias pour éviter tout écrasement
from mock_data import (
    get_constructor_standings as mock_get_constructor_standings,
    get_driver_standings as mock_get_driver_standings,
    get_schedule_current as mock_get_schedule_current,
    get_last_race as mock_get_last_race,
    get_constructors_current as mock_get_constructors_current,
    get_drivers_current as mock_get_drivers_current,
)

app = FastAPI(title="F1 Dashboard API", version="1.0.0")

# ── CORS ───────────────────────────────────────────────────────────────────────
# En prod, préfère définir FRONTEND_ORIGIN pour éviter le "*"
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mode mock/live ────────────────────────────────────────────────────────────
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").strip().lower() in {"1", "true", "yes", "on"}

# ── Redis cache ───────────────────────────────────────────────────────────────
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()
except Exception:
    redis_client = None
    print("⚠️  Redis non disponible - cache désactivé")

# ── Ergast API ────────────────────────────────────────────────────────────────
ERGAST_BASE_URL = "https://ergast.com/api/f1"
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "20"))

async def get_cached_data(key: str, fetch_function, ttl: int = 3600):
    """Récupère les données depuis Redis sinon via fetch_function(), puis met en cache."""
    if redis_client:
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

    data = await fetch_function()

    if redis_client and data is not None:
        redis_client.setex(key, ttl, json.dumps(data))

    return data

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "message": "🏎️ F1 Dashboard API",
        "version": "1.0.0",
        "mode": "MOCK DATA" if USE_MOCK_DATA else "LIVE DATA",
        "endpoints": [
            "/drivers/current",
            "/constructors/current",
            "/standings/drivers",
            "/standings/constructors",
            "/schedule/current",
            "/race/last",
            "/driver/{driver_id}/stats",
        ],
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "redis": "connected" if redis_client else "disconnected",
        "mode": "mock" if USE_MOCK_DATA else "live",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/drivers/current")
async def api_get_current_drivers():
    if USE_MOCK_DATA:
        return mock_get_drivers_current()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current/drivers.json")
                r.raise_for_status()
                return r.json()["MRData"]["DriverTable"]["Drivers"]
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (drivers): {e}")
    return await get_cached_data("drivers:current", fetch, ttl=86400)

@app.get("/constructors/current")
async def api_get_current_constructors():
    if USE_MOCK_DATA:
        return mock_get_constructors_current()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current/constructors.json")
                r.raise_for_status()
                return r.json()["MRData"]["ConstructorTable"]["Constructors"]
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (constructors): {e}")
    return await get_cached_data("constructors:current", fetch, ttl=86400)

@app.get("/standings/drivers")
async def api_get_driver_standings():
    if USE_MOCK_DATA:
        return mock_get_driver_standings()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current/driverStandings.json")
                r.raise_for_status()
                lists = r.json()["MRData"]["StandingsTable"]["StandingsLists"]
                return lists[0]["DriverStandings"] if lists else []
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (driverStandings): {e}")
    return await get_cached_data("standings:drivers", fetch, ttl=3600)

@app.get("/standings/constructors")
async def api_get_constructor_standings():
    if USE_MOCK_DATA:
        return mock_get_constructor_standings()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current/constructorStandings.json")
                r.raise_for_status()
                lists = r.json()["MRData"]["StandingsTable"]["StandingsLists"]
                return lists[0]["ConstructorStandings"] if lists else []
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (constructorStandings): {e}")
    return await get_cached_data("standings:constructors", fetch, ttl=3600)

@app.get("/schedule/current")
async def api_get_current_schedule():
    if USE_MOCK_DATA:
        return mock_get_schedule_current()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current.json")
                r.raise_for_status()
                return r.json()["MRData"]["RaceTable"]["Races"]
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (schedule): {e}")
    return await get_cached_data("schedule:current", fetch, ttl=86400)

@app.get("/race/last")
async def api_get_last_race_results():
    if USE_MOCK_DATA:
        return mock_get_last_race()

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/current/last/results.json")
                r.raise_for_status()
                races = r.json()["MRData"]["RaceTable"]["Races"]
                return races[0] if races else None
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (last race): {e}")
    return await get_cached_data("race:last", fetch, ttl=1800)

@app.get("/driver/{driver_id}/stats")
async def api_get_driver_stats(driver_id: str):
    if USE_MOCK_DATA:
        # Exemple enrichi (tu peux brancher sur ton mock_data si tu veux)
        mock_stats = {
            "verstappen": {"driver_id": "verstappen", "total_wins": 53, "total_podiums": 98, "total_races": 175},
            "hamilton":   {"driver_id": "hamilton",   "total_wins": 103, "total_podiums": 197, "total_races": 335},
            "leclerc":    {"driver_id": "leclerc",    "total_wins": 5, "total_podiums": 30, "total_races": 120},
        }
        return mock_stats.get(driver_id, {"driver_id": driver_id, "total_wins": 0, "total_podiums": 0, "total_races": 0})

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                wins_r = await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results/1.json?limit=1000")
                all_r =  await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results.json?limit=1000")
                wins_r.raise_for_status(); all_r.raise_for_status()
                wins_data = wins_r.json()["MRData"]["RaceTable"]
                all_races = all_r.json()["MRData"]["RaceTable"]["Races"]
                podiums = sum(1 for race in all_races for res in race["Results"] if int(res["position"]) <= 3)
                return {"driver_id": driver_id, "total_wins": int(wins_data["total"]), "total_podiums": podiums, "total_races": len(all_races)}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (driver stats): {e}")
    return await get_cached_data(f"driver:{driver_id}:stats", fetch, ttl=86400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
