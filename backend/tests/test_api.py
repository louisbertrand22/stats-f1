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
    assert "cache" in data
    assert "mode" in data
    assert data["mode"] == "mock"
    assert data["cache"]["status"] == "active"

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
    assert data["total_wins"] == 68  # Exact win count as of end of 2024 season
    assert data["total_podiums"] == 122
    assert data["total_races"] == 228

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

def test_get_all_driver_stats():
    """Test de récupération des statistiques de tous les pilotes"""
    response = client.get("/drivers/stats")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Vérifier la structure des données
    for driver_stat in data:
        assert "driver_id" in driver_stat
        assert "name" in driver_stat
        assert "total_wins" in driver_stat
        assert "total_podiums" in driver_stat
        assert "total_races" in driver_stat
        assert "total_poles" in driver_stat
    # Vérifier que Hamilton a les bonnes stats
    hamilton = next((d for d in data if d["driver_id"] == "hamilton"), None)
    assert hamilton is not None
    assert hamilton["total_wins"] == 105
    assert hamilton["total_poles"] == 104
    # Vérifier que Verstappen a les bonnes stats (67 victoires)
    verstappen = next((d for d in data if d["driver_id"] == "verstappen"), None)
    assert verstappen is not None
    assert verstappen["total_wins"] == 68
    assert verstappen["total_podiums"] == 122
    assert verstappen["total_races"] == 228
    assert verstappen["total_poles"] == 47

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

def test_get_race_result():
    """Test de récupération d'un résultat de course spécifique"""
    response = client.get("/race/2025/1")
    assert response.status_code == 200
    data = response.json()
    assert "raceName" in data
    assert "Results" in data
    assert len(data["Results"]) >= 3
    assert data["season"] == "2025"
    assert data["round"] == "1"
    assert data["raceName"] == "Australian Grand Prix"
    # Vérifier le podium
    assert data["Results"][0]["position"] == "1"
    assert data["Results"][1]["position"] == "2"
    assert data["Results"][2]["position"] == "3"

def test_get_race_result_not_found():
    """Test d'un résultat de course inexistant"""
    response = client.get("/race/2025/99")
    assert response.status_code == 404

def test_cache_stats():
    """Test du endpoint de statistiques du cache"""
    response = client.get("/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "cache" in data
    assert "status" in data
    assert data["status"] == "active"
    assert "entries" in data["cache"]
    assert "hits" in data["cache"]
    assert "misses" in data["cache"]
    assert "hit_rate" in data["cache"]
    assert "persistence" in data["cache"]

def test_cache_functionality():
    """Test que le cache fonctionne correctement - Note: avec USE_MOCK_DATA=true, le cache est contourné"""
    # Même avec mock data, le cache stats endpoint devrait fonctionner
    response1 = client.get("/drivers/current")
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Deuxième requête - les données devraient être identiques
    response2 = client.get("/drivers/current")
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Les données devraient être identiques (cohérence)
    assert data1 == data2
    assert len(data1) > 0
    
    # Vérifier que le cache stats endpoint fonctionne
    stats_response = client.get("/cache/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    
    # Vérifier la structure des stats (même si cache n'est pas utilisé en mode mock)
    assert "cache" in stats
    assert "status" in stats
    assert isinstance(stats["cache"]["entries"], int)
    assert isinstance(stats["cache"]["hits"], int)
    assert isinstance(stats["cache"]["misses"], int)

def test_health_check_multiple_calls():
    """Test que plusieurs appels à /health ne génèrent pas de logs excessifs"""
    # Appeler /health plusieurs fois - cela ne devrait pas causer d'erreur
    # et ne devrait pas générer de logs excessifs (testé manuellement)
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "cache" in data
        assert data["cache"]["status"] == "active"