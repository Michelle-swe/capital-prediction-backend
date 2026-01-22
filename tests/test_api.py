import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthCheck:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

class TestPrediction:
    def test_predict_valid_year(self):
        """Test prediction with valid year"""
        response = client.post("/api/predict/income", json={"year": 2024})
        assert response.status_code == 200
        data = response.json()
        assert "predicted_income" in data
        assert isinstance(data["predicted_income"], float)

    def test_predict_boundary_years(self):
        """Test prediction with boundary years"""
        # Minimum year
        response = client.post("/api/predict/income", json={"year": 1900})
        assert response.status_code == 200
        
        # Maximum year
        response = client.post("/api/predict/income", json={"year": 2100})
        assert response.status_code == 200

    def test_predict_invalid_year_below_range(self):
        """Test prediction with year below minimum"""
        response = client.post("/api/predict/income", json={"year": 1800})
        assert response.status_code == 422  # Validation error

    def test_predict_invalid_year_above_range(self):
        """Test prediction with year above maximum"""
        response = client.post("/api/predict/income", json={"year": 2200})
        assert response.status_code == 422  # Validation error

    def test_predict_invalid_input_type(self):
        """Test prediction with invalid input type"""
        response = client.post("/api/predict/income", json={"year": "2024"})
        assert response.status_code == 422  # Validation error

class TestModelVersion:
    def test_get_model_version(self):
        """Test model version endpoint"""
        response = client.get("/api/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "r2_score" in data
        assert "trained_date" in data

class TestIntegration:
    def test_api_flow(self):
        """Test complete API flow"""
        # Check health
        health = client.get("/api/health")
        assert health.status_code == 200
        
        # Get model version
        version = client.get("/api/version")
        assert version.status_code == 200
        
        # Make prediction
        prediction = client.post("/api/predict/income", json={"year": 2024})
        assert prediction.status_code == 200
        assert prediction.json()["predicted_income"] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
