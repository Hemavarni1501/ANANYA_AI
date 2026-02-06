"""
Pytest Fixtures for ANANYA-AI Service
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from models.schemas import (
    InteractionData, 
    BiasDetectionRequest,
    AdaptationRequest,
    AdaptationType,
    BiasType
)


@pytest.fixture
def client():
    """FastAPI Test Client"""
    return TestClient(app)


@pytest.fixture
def sample_interaction():
    """Sample interaction data for testing"""
    return InteractionData(
        session_hash="test_session_123",
        content_id="content_abc",
        response_time_ms=5000,
        action_type="read",
        content_text="Sample learning content",
        is_repeated_error=False,
        clarification_count=0,
        time_on_content_seconds=30
    )


@pytest.fixture
def slow_interaction():
    """Interaction indicating struggle"""
    return InteractionData(
        session_hash="test_session_slow",
        content_id="content_abc",
        response_time_ms=25000,  # Very slow
        action_type="read",
        content_text="Complex content",
        is_repeated_error=True,
        clarification_count=0,
        time_on_content_seconds=120
    )


@pytest.fixture
def complex_text():
    """Text with high complexity"""
    return (
        "The implementations of sophisticated algorithmic paradigms necessitate "
        "comprehensive understanding of computational complexity theory and "
        "asymptotic analysis methodologies to facilitate optimal performance."
    )


@pytest.fixture
def simple_text():
    """Text with low complexity"""
    return "The cat sat on the mat. It was a happy cat."
