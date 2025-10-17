#!/usr/bin/env python3
"""
Simple API test script for EcoFarm Quest Backend
This script tests the basic functionality of the API endpoints
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("🔍 Testing user registration...")
    try:
        user_data = {
            "name": "Test Farmer",
            "email": "test@example.com",
            "password": "TestPassword123",
            "phone": "+91 98765 43210",
            "location": "Test Village",
            "farm_size": "5 acres",
            "primary_crops": ["Rice", "Wheat"],
            "farming_experience": "10 years",
            "water_source": "borewell"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            print("✅ User registration passed")
            data = response.json()
            return data.get('data', {}).get('access_token')
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return None

def test_user_login():
    """Test user login"""
    print("🔍 Testing user login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login passed")
            data = response.json()
            return data.get('data', {}).get('access_token')
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None

def test_get_courses(token):
    """Test getting courses"""
    print("🔍 Testing get courses...")
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{BASE_URL}/courses/", headers=headers)
        if response.status_code == 200:
            print("✅ Get courses passed")
            data = response.json()
            courses = data.get('data', {}).get('courses', [])
            print(f"   Found {len(courses)} courses")
            return courses[0].get('id') if courses else None
        else:
            print(f"❌ Get courses failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Get courses error: {e}")
        return None

def test_get_community_stats():
    """Test getting community stats"""
    print("🔍 Testing community stats...")
    try:
        response = requests.get(f"{BASE_URL}/community/stats")
        if response.status_code == 200:
            print("✅ Community stats passed")
            return True
        else:
            print(f"❌ Community stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Community stats error: {e}")
        return False

def test_get_achievements():
    """Test getting achievements"""
    print("🔍 Testing get achievements...")
    try:
        response = requests.get(f"{BASE_URL}/achievements/")
        if response.status_code == 200:
            print("✅ Get achievements passed")
            data = response.json()
            achievements = data.get('data', {}).get('achievements', [])
            print(f"   Found {len(achievements)} achievements")
            return True
        else:
            print(f"❌ Get achievements failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get achievements error: {e}")
        return False

def main():
    """Run all tests"""
    print("🌱 EcoFarm Quest API Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Health check
    if test_health_check():
        tests_passed += 1
    
    print()
    
    # Test 2: User registration
    token = test_user_registration()
    if token:
        tests_passed += 1
    
    print()
    
    # Test 3: User login (if registration failed, try with existing user)
    if not token:
        token = test_user_login()
    if token:
        tests_passed += 1
    
    print()
    
    # Test 4: Get courses
    course_id = test_get_courses(token)
    if course_id:
        tests_passed += 1
    
    print()
    
    # Test 5: Community stats
    if test_get_community_stats():
        tests_passed += 1
    
    print()
    
    # Test 6: Get achievements
    if test_get_achievements():
        tests_passed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the API server.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


