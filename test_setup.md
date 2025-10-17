# EcoFarm Quest - MongoDB & Jest Testing Setup

## ✅ What I've Added

### 1. MongoDB Integration
- **Enhanced `app.py`** with MongoDB connection and health checks
- **Updated `requirements.txt`** with MongoDB testing dependencies
- **Created `tests/test_mongodb.py`** with comprehensive MongoDB tests
- **Added connection logging** and error handling

### 2. Jest Testing for Frontend
- **Created `package.json`** with Jest configuration
- **Added `FRONTEND/setupTests.js`** for test environment setup
- **Created `FRONTEND/__tests__/app.test.js`** for application tests
- **Created `FRONTEND/__tests__/api.test.js`** for API integration tests
- **Added `.babelrc`** for JavaScript transpilation

### 3. Test Runner
- **Created `run_tests.py`** to run both Python and JavaScript tests
- **Added coverage reporting** for both backend and frontend
- **Integrated MongoDB testing** with mock database

## 🚀 How to Use

### Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Run Tests
```bash
# Run all tests (Python + JavaScript)
python run_tests.py

# Run only Python tests
python -m pytest tests/ -v

# Run only JavaScript tests
npm test

# Run with coverage
npm run test:coverage
```

### MongoDB Testing
The MongoDB tests use `mongomock` for fast, isolated testing:
- Tests database operations
- Tests data consistency
- Tests performance queries
- Tests error handling

### Jest Testing
The Jest tests cover:
- Application initialization
- Authentication flows
- API integration
- Session management
- Error handling
- User interface updates

## 📁 New Files Created

### Backend
- `tests/test_mongodb.py` - MongoDB integration tests
- `run_tests.py` - Test runner script

### Frontend
- `package.json` - Node.js dependencies and scripts
- `FRONTEND/setupTests.js` - Jest test setup
- `FRONTEND/__tests__/app.test.js` - Application tests
- `FRONTEND/__tests__/api.test.js` - API tests
- `.babelrc` - Babel configuration

## 🔧 Configuration

### MongoDB
- Uses cloud MongoDB Atlas (no local installation needed)
- Connection string in `.env` file
- Health check endpoint: `/api/health`

### Jest
- Test environment: jsdom
- Coverage reporting enabled
- Mock fetch and localStorage
- Babel transpilation for ES6+

## 🎯 Test Coverage

### Backend Tests
- ✅ MongoDB connection
- ✅ User operations
- ✅ Learning progress
- ✅ Community data
- ✅ Achievements
- ✅ Data consistency
- ✅ Performance queries

### Frontend Tests
- ✅ Application initialization
- ✅ Login/Register flows
- ✅ API integration
- ✅ Session management
- ✅ Error handling
- ✅ UI updates

## 🚀 Next Steps

1. **Install dependencies**: `pip install -r requirements.txt && npm install`
2. **Run tests**: `python run_tests.py`
3. **Check coverage**: Open `htmlcov/index.html` for Python coverage
4. **View Jest coverage**: Check `FRONTEND/coverage/` directory

Your EcoFarm Quest application now has comprehensive testing for both backend and frontend! 🌱
