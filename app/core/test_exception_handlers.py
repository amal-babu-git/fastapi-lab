"""
Test script to verify exception handlers are working correctly.
"""
from fastapi.testclient import TestClient
from app.core.main import app

client = TestClient(app)


def test_exception_handlers():
    """Test that exception handlers are properly configured."""
    
    # Test root endpoint works
    response = client.get("/")
    assert response.status_code == 200
    print("✓ Root endpoint working")
    
    # Test health endpoint works
    response = client.get("/health")
    assert response.status_code == 200
    print("✓ Health endpoint working")
    
    # Test 404 handling
    response = client.get("/nonexistent")
    assert response.status_code == 404
    print("✓ 404 handling working")
    
    print("✓ All exception handler tests passed!")


if __name__ == "__main__":
    test_exception_handlers()