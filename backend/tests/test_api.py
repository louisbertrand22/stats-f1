import pytest
import os
import sys

# Ajouter le répertoire parent au path pour importer main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Forcer l'utilisation des données mockées pour les tests
os.environ["USE_MOCK_DATA"] = "true"

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    """Test de l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "F1 Dashboard API" in data["message"]
    assert "endpoints" in data
    assert "mode" in data

def test_health_check():
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "redis" in data
    assert "mode" in data
    assert data["mode"] == "mock"

def test_get_current_drivers():
    """Test de récupération des pilotes actuels"""
    response = client.get("/drivers/current")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "driverId" in data[0]
    assert "givenName" in data[0]
    assert "familyName" in data[0]
    assert data[0]["driverId"] == "piastri"

def test_get_current_constructors():
    """Test de récupération des constructeurs actuels"""
    response = client.get("/constructors/current")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "constructorId" in data[0]
    assert "name" in data[0]

def test_get_driver_standings():
    """Test du classement des pilotes"""
    response = client.get("/standings/drivers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "position" in data[0]
    assert "points" in data[0]
    assert "Driver" in data[0]
    assert data[0]["position"] == "1"
    assert data[0]["Driver"]["familyName"] == "Piastri"

def test_get_constructor_standings():
    """Test du classement des constructeurs"""
    response = client.get("/standings/constructors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "position" in data[0]
    assert "points" in data[0]
    assert "Constructor" in data[0]
    assert data[0]["Constructor"]["name"] == "McLaren"

def test_get_schedule():
    """Test du calendrier"""
    response = client.get("/schedule/current")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 24  # Full 2025 season schedule
    assert "raceName" in data[0]
    assert "date" in data[0]
    assert "Circuit" in data[0]
    assert data[0]["raceName"] == "Australian Grand Prix"
    # Verify last race
    assert data[-1]["raceName"] == "Abu Dhabi Grand Prix"
    assert data[-1]["round"] == "24"

def test_get_last_race():
    """Test de la dernière course"""
    response = client.get("/race/last")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert "raceName" in data
    assert "Results" in data
    assert len(data["Results"]) > 0
    # Verify it's the last race of the season
    assert data["raceName"] == "Abu Dhabi Grand Prix"
    assert data["round"] == "24"

def test_driver_stats_verstappen():
    """Test des statistiques de Verstappen"""
    response = client.get("/driver/verstappen/stats")
    assert response.status_code == 200
    data = response.json()
    assert "driver_id" in data
    assert "total_wins" in data
    assert "total_podiums" in data
    assert data["driver_id"] == "verstappen"
    assert data["total_wins"] > 0

def test_driver_stats_hamilton():
    """Test des statistiques d'Hamilton"""
    response = client.get("/driver/hamilton/stats")
    assert response.status_code == 200
    data = response.json()
    assert "driver_id" in data
    assert "total_wins" in data
    assert "total_podiums" in data
    assert data["driver_id"] == "hamilton"
    assert data["total_wins"] > 0

def test_driver_stats_unknown():
    """Test des statistiques d'un pilote inconnu"""
    response = client.get("/driver/unknown_driver/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["driver_id"] == "unknown_driver"
    assert data["total_wins"] == 0
    assert data["total_podiums"] == 0

def test_invalid_endpoint():
    """Test d'un endpoint invalide"""
    response = client.get("/invalid/endpoint")
    assert response.status_code == 404

def test_drivers_data_structure():
    """Test de la structure des données des pilotes"""
    response = client.get("/drivers/current")
    data = response.json()
    
    for driver in data:
        assert "driverId" in driver
        assert "givenName" in driver
        assert "familyName" in driver
        assert "dateOfBirth" in driver
        assert "nationality" in driver

def test_standings_data_integrity():
    """Test de l'intégrité des données du classement"""
    response = client.get("/standings/drivers")
    data = response.json()
    
    # Vérifier que les positions sont dans l'ordre
    for i, standing in enumerate(data):
        assert standing["position"] == str(i + 1)
        assert int(standing["points"]) >= 0
        assert int(standing["wins"]) >= 0