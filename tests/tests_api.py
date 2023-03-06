from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("http://127.0.0.1:8080/")
    assert response.status_code == 200
    assert response.json() == {"name": "CNMV scraping API",
                               "type": "scraper",
                               "description": "Scrape Sicavs from the CNMV",
                               "documentation": "/docs",
                               "database_status": "OK"}


def test_search():
    response = client.get("sicavs/search/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()
