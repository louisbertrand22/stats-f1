import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test de l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "F1 Dashboard API" in data["message"]
    assert "endpoints" in data

def test_health_check():
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "redis" in data

@pytest.mark.asyncio
async def test_get_current_drivers():
    """Test de récupération des pilotes actuels"""
    response = client.get("/drivers/current")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "driverId" in data[0]
        assert "givenName" in data[0]
        assert "familyName" in data[0]

@pytest.mark.asyncio
async def test_get_driver_standings():
    """Test du classement des pilotes"""
    response = client.get("/standings/drivers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "position" in data[0]
        assert "points" in data[0]
        assert "Driver" in data[0]

@pytest.mark.asyncio
async def test_get_constructor_standings():
    """Test du classement des constructeurs"""
    response = client.get("/standings/constructors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "position" in data[0]
        assert "points" in data[0]
        assert "Constructor" in data[0]

@pytest.mark.asyncio
async def test_get_schedule():
    """Test du calendrier"""
    response = client.get("/schedule/current")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "raceName" in data[0]
        assert "date" in data[0]
        assert "Circuit" in data[0]

@pytest.mark.asyncio
async def test_get_last_race():
    """Test de la dernière course"""
    response = client.get("/race/last")
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "raceName" in data
        assert "Results" in data

@pytest.mark.asyncio
async def test_driver_stats():
    """Test des statistiques d'un pilote"""
    # Test avec un pilote connu
    response = client.get("/driver/hamilton/stats")
    assert response.status_code == 200
    data = response.json()
    assert "driver_id" in data
    assert "total_wins" in data
    assert "total_podiums" in data
    assert data["driver_id"] == "hamilton"

def test_invalid_endpoint():
    """Test d'un endpoint invalide"""
    response = client.get("/invalid/endpoint")
    assert response.status_code == 404