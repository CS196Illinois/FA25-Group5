"""
Test script for Schedule Generator API

Run this after starting the server to test the endpoints
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_api_test():
    """Test the API test endpoint"""
    print("\n" + "="*60)
    print("Testing API Test Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/v1/test")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_generate_schedule():
    """Test schedule generation endpoint"""
    print("\n" + "="*60)
    print("Testing Schedule Generation Endpoint")
    print("="*60)
    
    payload = {
        "user_profile": {
            "target_gpa": 3.5,
            "max_workload_hours": 15,
            "current_gpa": 3.3,
            "preferred_professors": ["Smith"],
            "avoid_professors": []
        },
        "hard_constraints": {
            "completed_courses": ["CS101"],
            "required_courses": [],
            "time_blocks": [],
            "excluded_courses": []
        },
        "soft_preferences": {
            "preferred_times": ["morning"],
            "preferred_days": ["MWF"],
            "rating_threshold": 3.5
        },
        "num_schedules": 3
    }
    
    print("\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(
        f"{BASE_URL}/api/v1/generate-schedule",
        json=payload
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def test_recommendations():
    """Test recommendations endpoint"""
    print("\n" + "="*60)
    print("Testing Recommendations Endpoint")
    print("="*60)
    
    payload = {
        "user_profile": {
            "target_gpa": 3.5,
            "max_workload_hours": 15,
            "current_gpa": 3.3,
            "preferred_professors": [],
            "avoid_professors": []
        },
        "hard_constraints": {
            "completed_courses": [],
            "required_courses": [],
            "time_blocks": [],
            "excluded_courses": []
        },
        "soft_preferences": {
            "rating_threshold": 4.0
        },
        "top_n": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/recommend",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def test_search_courses():
    """Test course search endpoint"""
    print("\n" + "="*60)
    print("Testing Course Search Endpoint")
    print("="*60)
    
    query = "CS"
    response = requests.get(f"{BASE_URL}/api/v1/courses/search?q={query}")
    
    print(f"Search Query: {query}")
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def test_course_details():
    """Test course details endpoint"""
    print("\n" + "="*60)
    print("Testing Course Details Endpoint")
    print("="*60)
    
    course_id = "CS225"
    response = requests.get(f"{BASE_URL}/api/v1/courses/{course_id}")
    
    print(f"Course ID: {course_id}")
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code in [200, 404]


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("SCHEDULE GENERATOR API TESTS")
    print("="*60)
    print("Make sure the server is running on http://localhost:5000")
    print("="*60)
    
    tests = [
        ("Health Check", test_health),
        ("API Test", test_api_test),
        ("Generate Schedule", test_generate_schedule),
        ("Get Recommendations", test_recommendations),
        ("Search Courses", test_search_courses),
        ("Course Details", test_course_details)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "✓ PASSED" if success else "✗ FAILED"))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
            print("Make sure the server is running: python app.py")
            return
        except Exception as e:
            results.append((test_name, f"✗ ERROR: {str(e)}"))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results:
        print(f"{test_name:.<40} {result}")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
