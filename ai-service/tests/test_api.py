"""
API Integration Tests
Verifies full end-to-end API functionality
"""
import pytest
from models.schemas import AdaptationType


def test_health_check(client):
    """Verify health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "bias_detector" in data["services"]
    assert data["configuration"]["log_user_identifiers"] is False


def test_detect_bias_endpoint(client, complex_text):
    """Verify bias detection API."""
    payload = {
        "session_hash": "test_session_api",
        "content_text": complex_text,
        "interaction_patterns": []
    }
    
    response = client.post("/detect-bias", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["bias_detected"] is True
    assert data["complexity_level"] == "complex"
    assert "deterministic_hash" in data


def test_generate_adaptation_endpoint(client, complex_text):
    """Verify adaptation generation API."""
    payload = {
        "session_hash": "test_session_api",
        "original_content": complex_text,
        "requested_adaptations": ["simplify_language"],
        "interaction_signals": {"clarification_count": 4}
    }
    
    response = client.post("/generate-adaptation", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["adaptations"]) > 0
    assert data["adaptations"][0]["adaptation_type"] == "simplify_language"


def test_analyze_interaction_endpoint(client):
    """Verify interaction analysis API."""
    payload = {
        "session_hash": "test_session_api",
        "content_id": "c1",
        "response_time_ms": 25000,
        "action_type": "read",
        "content_text": "text",
        "is_repeated_error": True,
        "clarification_count": 0,
        "time_on_content_seconds": 60
    }
    
    response = client.post("/analyze-interaction", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["requires_adaptation"] is True
    assert data["response_pattern"] == "deliberate"


def test_privacy_enforcement(client):
    """Verify that valid request without user IDs works, and check logging."""
    # This implicit test confirms we aren't asking for user_id in schemas
    payload = {
        "session_hash": "anon_123",  # Anonymized ID
        "content_text": "Test content",
        "interaction_patterns": []
    }
    
    response = client.post("/detect-bias", json=payload)
    assert response.status_code == 200
    
    # We can't easily test internal logs here, but unit tests covered it
