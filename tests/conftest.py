"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI app.
    The client can be used to make requests to the app without running a server.
    """
    return TestClient(app)


@pytest.fixture
def test_data():
    """
    Fixture that provides consistent test data (emails, activity names) 
    for use across multiple test functions.
    """
    return {
        "existing_email": "michael@mergington.edu",
        "new_email": "newstudent@mergington.edu",
        "existing_activity": "Chess Club",
        "nonexistent_activity": "Nonexistent Club",
    }
