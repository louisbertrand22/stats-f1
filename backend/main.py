from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import redis
import json
from datetime import datetime
import os

# Import des données mockées
from mock_data import (
    MOCK_DRIVERS,
    MOCK_CONSTRUCTORS,
    MOCK_DRIVER_STANDINGS,
    MOCK_CONSTRUCTOR_STANDINGS,
    MOCK_SCHEDULE,
    MOCK_LAST_RACE
)

app = FastAPI(title="F1 Dashboard API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mode de fonctionnement (mock ou real)
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"

# Configuration Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()
except:
    redis_client = None
    print("⚠️  Redis non disponible - cache désactivé")

# URL de base de l'API Ergast F1
ERGAST_BASE_URL = "https://ergast.com/api/f1"

async def get_cached_data(key: str, fetch_function, ttl: int = 3600):
    """Récupère les données depuis le cache ou l'API"""
    if redis_client:
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
    
    data = await fetch_function()
    
    if redis_client and data:
        redis_client.setex(key, ttl, json.dumps(data))
    
    return data

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
            "/driver/{driver_id}/stats"
        ]
    }

@app.get("/health")
async def health_check():
    """Endpoint pour vérifier la santé de l'API"""
    return {
        "status": "healthy",
        "redis": "connected" if redis_client else "disconnected",
        "mode": "mock" if USE_MOCK_DATA else "live",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/drivers/current")
async def get_current_drivers():
    """Récupère la liste des pilotes de la saison en cours"""
    if USE_MOCK_DATA:
        return MOCK_DRIVERS
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current/drivers.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            return response.json()["MRData"]["DriverTable"]["Drivers"]
    
    return await get_cached_data("drivers:current", fetch, ttl=86400)

@app.get("/constructors/current")
async def get_current_constructors():
    """Récupère la liste des écuries de la saison en cours"""
    if USE_MOCK_DATA:
        return MOCK_CONSTRUCTORS
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current/constructors.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            return response.json()["MRData"]["ConstructorTable"]["Constructors"]
    
    return await get_cached_data("constructors:current", fetch, ttl=86400)

@app.get("/standings/drivers")
async def get_driver_standings():
    """Récupère le classement actuel des pilotes"""
    if USE_MOCK_DATA:
        return MOCK_DRIVER_STANDINGS
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current/driverStandings.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            standings = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
            return standings[0]["DriverStandings"] if standings else []
    
    return await get_cached_data("standings:drivers", fetch, ttl=3600)

@app.get("/standings/constructors")
async def get_constructor_standings():
    """Récupère le classement actuel des écuries"""
    if USE_MOCK_DATA:
        return MOCK_CONSTRUCTOR_STANDINGS
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current/constructorStandings.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            standings = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
            return standings[0]["ConstructorStandings"] if standings else []
    
    return await get_cached_data("standings:constructors", fetch, ttl=3600)

@app.get("/schedule/current")
async def get_current_schedule():
    """Récupère le calendrier de la saison en cours"""
    if USE_MOCK_DATA:
        return MOCK_SCHEDULE
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            return response.json()["MRData"]["RaceTable"]["Races"]
    
    return await get_cached_data("schedule:current", fetch, ttl=86400)

@app.get("/race/last")
async def get_last_race_results():
    """Récupère les résultats de la dernière course"""
    if USE_MOCK_DATA:
        return MOCK_LAST_RACE
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ERGAST_BASE_URL}/current/last/results.json")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            races = response.json()["MRData"]["RaceTable"]["Races"]
            return races[0] if races else None
    
    return await get_cached_data("race:last", fetch, ttl=1800)

@app.get("/driver/{driver_id}/stats")
async def get_driver_stats(driver_id: str):
    """Récupère les statistiques d'un pilote"""
    if USE_MOCK_DATA:
        # Données mockées pour quelques pilotes
        mock_stats = {
            "verstappen": {"driver_id": "verstappen", "total_wins": 53, "total_podiums": 98, "total_races": 175},
            "hamilton": {"driver_id": "hamilton", "total_wins": 103, "total_podiums": 197, "total_races": 335},
            "leclerc": {"driver_id": "leclerc", "total_wins": 5, "total_podiums": 30, "total_races": 120},
            "sainz": {"driver_id": "sainz", "total_wins": 3, "total_podiums": 20, "total_races": 185},
        }
        return mock_stats.get(driver_id, {"driver_id": driver_id, "total_wins": 0, "total_podiums": 0, "total_races": 0})
    
    async def fetch():
        async with httpx.AsyncClient() as client:
            # Récupère toutes les victoires du pilote
            wins_response = await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results/1.json?limit=1000")
            # Récupère tous les podiums
            podiums_response = await client.get(f"{ERGAST_BASE_URL}/drivers/{driver_id}/results.json?limit=1000")
            
            if wins_response.status_code != 200 or podiums_response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erreur API F1")
            
            wins_data = wins_response.json()["MRData"]["RaceTable"]
            all_races = podiums_response.json()["MRData"]["RaceTable"]["Races"]
            
            podiums = sum(1 for race in all_races for result in race["Results"] if int(result["position"]) <= 3)
            
            return {
                "driver_id": driver_id,
                "total_wins": int(wins_data["total"]),
                "total_podiums": podiums,
                "total_races": len(all_races)
            }
    
    return await get_cached_data(f"driver:{driver_id}:stats", fetch, ttl=86400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)