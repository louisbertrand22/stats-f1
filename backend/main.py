from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Tuple
import asyncio
import logging
import pickle
from pathlib import Path

# Import mock data en alias pour éviter tout écrasement
from mock_data import (
    get_constructor_standings as mock_get_constructor_standings,
    get_driver_standings as mock_get_driver_standings,
    get_schedule_current as mock_get_schedule_current,
    get_last_race as mock_get_last_race,
    get_constructors_current as mock_get_constructors_current,
    get_drivers_current as mock_get_drivers_current,
    get_race_result as mock_get_race_result,
)

app = FastAPI(title="F1 Dashboard API", version="1.0.0")

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# ── Cache configuration ───────────────────────────────────────────────────────
CACHE_DIR = os.getenv("CACHE_DIR", "/tmp/f1_cache")
CACHE_PERSIST = os.getenv("CACHE_PERSIST", "true").strip().lower() in {"1", "true", "yes", "on"}

# ── Ergast API ────────────────────────────────────────────────────────────────
ERGAST_BASE_URL = "https://ergast.com/api/f1"
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "20"))

# ── Custom Cache Implementation ───────────────────────────────────────────────
class CustomCache:
    """Custom cache with TTL support and optional file-based persistence.
    
    Features:
    - In-memory caching with automatic TTL expiration
    - Optional file-based persistence for cache durability across restarts
    - Thread-safe operations using asyncio locks
    - Statistics tracking (hits, misses, hit rate)
    """
    
    def __init__(self, cache_dir: str = CACHE_DIR, persist: bool = CACHE_PERSIST):
        self._cache: Dict[str, Tuple[any, datetime]] = {}
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
        self._persist = persist
        self._cache_dir = Path(cache_dir)
        
        # Create cache directory if persistence is enabled
        if self._persist:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            self._load_cache()
            logger.info(f"Custom cache initialized with persistence at {self._cache_dir}")
        else:
            logger.info("Custom cache initialized (in-memory only)")
    
    def _get_cache_file_path(self) -> Path:
        """Get the path to the cache persistence file."""
        return self._cache_dir / "cache_data.pkl"
    
    def _load_cache(self):
        """Load cache from disk if persistence is enabled."""
        if not self._persist:
            return
        
        cache_file = self._get_cache_file_path()
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self._cache = data.get('cache', {})
                    # Clean expired entries on load
                    now = datetime.now()
                    expired_keys = [k for k, (_, expiry) in self._cache.items() if now >= expiry]
                    for key in expired_keys:
                        del self._cache[key]
                    logger.info(f"Loaded {len(self._cache)} cache entries from disk (removed {len(expired_keys)} expired)")
            except Exception as e:
                logger.warning(f"Failed to load cache from disk: {e}")
                self._cache = {}
    
    def _save_cache(self):
        """Save cache to disk if persistence is enabled."""
        if not self._persist:
            return
        
        try:
            cache_file = self._get_cache_file_path()
            with open(cache_file, 'wb') as f:
                pickle.dump({'cache': self._cache}, f)
        except Exception as e:
            logger.warning(f"Failed to save cache to disk: {e}")
    
    async def get(self, key: str) -> Optional[any]:
        """Get value from cache if not expired."""
        async with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if datetime.now() < expiry:
                    self._hits += 1
                    return value
                else:
                    # Expired, remove it
                    del self._cache[key]
                    self._save_cache()
            self._misses += 1
            return None
    
    async def set(self, key: str, value: any, ttl: int):
        """Set value in cache with TTL in seconds."""
        async with self._lock:
            expiry = datetime.now() + timedelta(seconds=ttl)
            self._cache[key] = (value, expiry)
            self._save_cache()
    
    async def clear(self):
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._save_cache()
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return {
            "entries": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "persistence": "enabled" if self._persist else "disabled"
        }

# Initialize the custom cache
custom_cache = CustomCache()

async def get_cached_data(key: str, fetch_function, ttl: int = 3600):
    """Récupère les données depuis le cache custom, sinon via fetch_function(), puis met en cache."""
    # Try custom cache
    cached = await custom_cache.get(key)
    if cached is not None:
        return cached

    # Fetch fresh data
    data = await fetch_function()
    
    # Store in cache
    if data is not None:
        await custom_cache.set(key, data, ttl)

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
            "/race/{season}/{round}",
            "/drivers/stats",
            "/driver/{driver_id}/stats",
            "/cache/stats",
        ],
    }

@app.get("/health")
async def health_check():
    cache_stats = custom_cache.get_stats()
    
    return {
        "status": "healthy",
        "cache": {
            "status": "active",
            "entries": cache_stats["entries"],
            "persistence": cache_stats["persistence"]
        },
        "mode": "mock" if USE_MOCK_DATA else "live",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics for monitoring."""
    return {
        "cache": custom_cache.get_stats(),
        "status": "active"
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

@app.get("/race/{season}/{round}")
async def api_get_race_result(season: str, round: str):
    """Get race results for a specific season and round."""
    if USE_MOCK_DATA:
        result = mock_get_race_result(season, round)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Résultats non disponibles pour la course {season}/{round}")
        return result

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                r = await client.get(f"{ERGAST_BASE_URL}/{season}/{round}/results.json")
                r.raise_for_status()
                races = r.json()["MRData"]["RaceTable"]["Races"]
                if not races:
                    return None
                return races[0]
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (race result): {e}")
    
    result = await get_cached_data(f"race:{season}:{round}", fetch, ttl=86400)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Résultats non disponibles pour la course {season}/{round}")
    return result

@app.get("/drivers/stats")
async def api_get_all_driver_stats():
    """Get statistics for all current drivers"""
    if USE_MOCK_DATA:
        # Career statistics from statsf1.com (accurate as of end 2024 season)
        all_stats = [
            {"driver_id": "verstappen", "name": "Max Verstappen", "total_wins": 67, "total_podiums": 121, "total_races": 227, "total_poles": 46},
            {"driver_id": "hamilton",   "name": "Lewis Hamilton",   "total_wins": 105, "total_podiums": 202, "total_races": 374, "total_poles": 104},
            {"driver_id": "leclerc",    "name": "Charles Leclerc",    "total_wins": 8, "total_podiums": 48, "total_races": 165, "total_poles": 27},
            {"driver_id": "norris",     "name": "Lando Norris",     "total_wins": 9, "total_podiums": 40, "total_races": 146, "total_poles": 13},
            {"driver_id": "piastri",    "name": "Oscar Piastri",    "total_wins": 9, "total_podiums": 24, "total_races": 64, "total_poles": 5},
            {"driver_id": "russell",    "name": "George Russell",    "total_wins": 5, "total_podiums": 23, "total_races": 146, "total_poles": 7},
            {"driver_id": "alonso",     "name": "Fernando Alonso",     "total_wins": 32, "total_podiums": 106, "total_races": 419, "total_poles": 22},
            {"driver_id": "sainz_jr",   "name": "Carlos Sainz Jr.",   "total_wins": 4, "total_podiums": 28, "total_races": 223, "total_poles": 6},
            {"driver_id": "tsunoda",    "name": "Yuki Tsunoda",    "total_wins": 0, "total_podiums": 0, "total_races": 88, "total_poles": 0},
            {"driver_id": "albon",      "name": "Alex Albon",      "total_wins": 0, "total_podiums": 2, "total_races": 122, "total_poles": 0},
            {"driver_id": "gasly",      "name": "Pierre Gasly",      "total_wins": 1, "total_podiums": 5, "total_races": 171, "total_poles": 0},
            {"driver_id": "ocon",       "name": "Esteban Ocon",       "total_wins": 1, "total_podiums": 4, "total_races": 173, "total_poles": 0},
            {"driver_id": "stroll",     "name": "Lance Stroll",     "total_wins": 0, "total_podiums": 3, "total_races": 183, "total_poles": 1},
            {"driver_id": "hulkenberg", "name": "Nico Hülkenberg", "total_wins": 0, "total_podiums": 1, "total_races": 244, "total_poles": 1},
            {"driver_id": "antonelli",  "name": "Kimi Antonelli",  "total_wins": 0, "total_podiums": 1, "total_races": 18, "total_poles": 0},
            {"driver_id": "bearman",    "name": "Oliver Bearman",    "total_wins": 0, "total_podiums": 0, "total_races": 5, "total_poles": 0},
            {"driver_id": "lawson",     "name": "Liam Lawson",     "total_wins": 0, "total_podiums": 0, "total_races": 11, "total_poles": 0},
            {"driver_id": "colapinto",  "name": "Franco Colapinto",  "total_wins": 0, "total_podiums": 0, "total_races": 9, "total_poles": 0},
            {"driver_id": "hadjar",     "name": "Isack Hadjar",     "total_wins": 0, "total_podiums": 1, "total_races": 17, "total_poles": 0},
            {"driver_id": "bortoleto",  "name": "Gabriel Bortoleto",  "total_wins": 0, "total_podiums": 0, "total_races": 0, "total_poles": 0},
        ]
        return all_stats

    async def fetch():
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": "f1-dashboard/1.0"}) as client:
                # Get current drivers list
                drivers_r = await client.get(f"{ERGAST_BASE_URL}/current/drivers.json")
                drivers_r.raise_for_status()
                drivers = drivers_r.json()["MRData"]["DriverTable"]["Drivers"]
                
                all_stats = []
                for driver in drivers:
                    driver_id = driver["driverId"]
                    given_name = driver.get("givenName", "")
                    family_name = driver.get("familyName", "")
                    name = f"{given_name} {family_name}".strip()
                    
                    # Fetch stats for each driver
                    wins_r = await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results/1.json?limit=1000")
                    all_r =  await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results.json?limit=1000")
                    poles_r = await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/qualifying/1.json?limit=1000")
                    
                    wins_r.raise_for_status()
                    all_r.raise_for_status()
                    poles_r.raise_for_status()
                    
                    wins_data = wins_r.json()["MRData"]["RaceTable"]
                    all_races = all_r.json()["MRData"]["RaceTable"]["Races"]
                    poles_data = poles_r.json()["MRData"]["RaceTable"]
                    
                    podiums = sum(1 for race in all_races for res in race["Results"] if int(res["position"]) <= 3)
                    
                    all_stats.append({
                        "driver_id": driver_id,
                        "name": name,
                        "total_wins": int(wins_data["total"]),
                        "total_podiums": podiums,
                        "total_races": len(all_races),
                        "total_poles": int(poles_data["total"])
                    })
                
                return all_stats
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Erreur API F1 (all driver stats): {e}")
    
    return await get_cached_data("drivers:all:stats", fetch, ttl=86400)

@app.get("/driver/{driver_id}/stats")
async def api_get_driver_stats(driver_id: str):
    if USE_MOCK_DATA:
        # Career statistics from statsf1.com (accurate as of end 2024 season)
        mock_stats = {
            "verstappen": {"driver_id": "verstappen", "total_wins": 67, "total_podiums": 121, "total_races": 227},
            "hamilton":   {"driver_id": "hamilton",   "total_wins": 105, "total_podiums": 202, "total_races": 374},
            "leclerc":    {"driver_id": "leclerc",    "total_wins": 8, "total_podiums": 48, "total_races": 165},
            "norris":     {"driver_id": "norris",     "total_wins": 9, "total_podiums": 40, "total_races": 146},
            "piastri":    {"driver_id": "piastri",    "total_wins": 9, "total_podiums": 24, "total_races": 64},
            "russell":    {"driver_id": "russell",    "total_wins": 5, "total_podiums": 23, "total_races": 146},
            "alonso":     {"driver_id": "alonso",     "total_wins": 32, "total_podiums": 106, "total_races": 419},
            "sainz_jr":   {"driver_id": "sainz_jr",   "total_wins": 4, "total_podiums": 28, "total_races": 223},
            "tsunoda":    {"driver_id": "tsunoda",    "total_wins": 0, "total_podiums": 0, "total_races": 88},
            "albon":      {"driver_id": "albon",      "total_wins": 0, "total_podiums": 2, "total_races": 122},
            "gasly":      {"driver_id": "gasly",      "total_wins": 1, "total_podiums": 5, "total_races": 171},
            "ocon":       {"driver_id": "ocon",       "total_wins": 1, "total_podiums": 4, "total_races": 173},
            "stroll":     {"driver_id": "stroll",     "total_wins": 0, "total_podiums": 3, "total_races": 183},
            "hulkenberg": {"driver_id": "hulkenberg", "total_wins": 0, "total_podiums": 1, "total_races": 244},
            "antonelli":  {"driver_id": "antonelli",  "total_wins": 0, "total_podiums": 1, "total_races": 18},
            "bearman":    {"driver_id": "bearman",    "total_wins": 0, "total_podiums": 0, "total_races": 5},
            "lawson":     {"driver_id": "lawson",     "total_wins": 0, "total_podiums": 0, "total_races": 11},
            "colapinto":  {"driver_id": "colapinto",  "total_wins": 0, "total_podiums": 0, "total_races": 9},
            "hadjar":     {"driver_id": "hadjar",     "total_wins": 0, "total_podiums": 1, "total_races": 17},
            "bortoleto":  {"driver_id": "bortoleto",  "total_wins": 0, "total_podiums": 0, "total_races": 0},
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
