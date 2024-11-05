import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_message_missing_fields():
    response = client.post("/api/generate-message", json={})
    assert response.status_code == 422  # Validation error

def test_generate_message_invalid_url():
    response = client.post("/api/generate-message", json={
        "username": "test@example.com",
        "password": "password123",
        "target_profile_url": "not-a-valid-url"
    })
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_generate_message_success(mocker):
    # Mock the scraper and message generator
    mock_profile_data = {
        "posts": [
            {"content": "Test post 1", "timestamp": "1d"},
            {"content": "Test post 2", "timestamp": "2d"}
        ],
        "profile_info": {"name": "Test User"}
    }
    
    mocker.patch(
        "app.linkedin_scraper.get_profile_data",
        return_value=mock_profile_data
    )
    
    mocker.patch(
        "app.message_generator.create_message",
        return_value="Generated test message"
    )

    response = client.post("/api/generate-message", json={
        "username": "test@example.com",
        "password": "password123",
        "target_profile_url": "https://linkedin.com/in/testuser"
    })
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "posts" in response.json() 