#!/usr/bin/env python3
"""
Test Runner for EcoFarm Quest
Runs both Python backend tests and JavaScript frontend tests
"""

import subprocess
import sys
import os
from pathlib import Path

def run_python_tests():
    """Run Python backend tests"""
    print("🐍 Running Python Backend Tests...")
    print("=" * 50)
    
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v', 
            '--tb=short',
            '--cov=app',
            '--cov=models',
            '--cov=routes',
            '--cov-report=html',
            '--cov-report=term-missing'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Python tests: {e}")
        return False

def run_jest_tests():
    """Run JavaScript frontend tests"""
    print("\n🧪 Running JavaScript Frontend Tests...")
    print("=" * 50)
    
    try:
        # Check if node_modules exists, if not install dependencies
        if not os.path.exists('node_modules'):
            print("📦 Installing Node.js dependencies...")
            install_result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if install_result.returncode != 0:
                print(f"❌ Failed to install dependencies: {install_result.stderr}")
                return False
        
        # Run Jest tests
        result = subprocess.run([
            'npm', 'test'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Jest tests: {e}")
        return False

def run_mongodb_tests():
    """Run MongoDB-specific tests"""
    print("\n🍃 Running MongoDB Integration Tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/test_mongodb.py', 
            '-v',
            '--tb=short'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running MongoDB tests: {e}")
        return False

def main():
    """Main test runner"""
    print("🌱 EcoFarm Quest Test Suite")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    all_passed = True
    
    # Run Python backend tests
    if not run_python_tests():
        all_passed = False
    
    # Run MongoDB tests
    if not run_mongodb_tests():
        all_passed = False
    
    # Run JavaScript frontend tests
    if not run_jest_tests():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        print("🎉 Your EcoFarm Quest application is ready!")
    else:
        print("❌ Some tests failed!")
        print("🔧 Please check the output above for details.")
        sys.exit(1)

if __name__ == '__main__':
    main()