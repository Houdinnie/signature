"""
Simple test script to verify the backend API is working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_agents_endpoint():
    """Test the agents endpoint"""
    print("Testing agents endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/agents/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Number of agents: {len(response.json())}")
        if response.json():
            print(f"First agent: {response.json()[0]}")
    else:
        print(f"Response: {response.text}")
    print()

if __name__ == "__main__":
    print("Testing Signature Backend API")
    print("=" * 40)
    
    try:
        test_root_endpoint()
        test_health_endpoint()
        test_agents_endpoint()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend.")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")