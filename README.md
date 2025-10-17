EcoFarm Quest – Flask Backend + Static Frontend
================================================

Overview
--------
This repository contains the EcoFarm Quest backend built with Python Flask and serves the existing static frontend from the `FRONTEND/` directory. The backend exposes REST APIs for authentication, users, courses, community, achievements, and uploads. The frontend (`index.html`, `app.js`, `style.css`) is served directly by Flask at the root path.

Project Structure
-----------------
```
FRONTEND/
  index.html
  app.js
  style.css
app.py
run.py
requirements.txt
requirements-test.txt
tests/
scripts/
models/
routes/
```

Prerequisites
-------------
- Python 3.10+
- MongoDB (local or Atlas)

Quick Start
-----------
1) Create and activate a virtual environment (recommended)
```
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Environment variables
Create a `.env` (you can copy from `env.example`) and set:
```
FLASK_ENV=development
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me
MONGODB_URI=mongodb://localhost:27017/ecofarmquest
FRONTEND_URL=http://localhost:5000

# Mail (optional for password reset/notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=noreply@ecofarmquest.com

# Cloudinary (only if uploads use Cloudinary)
CLOUDINARY_URL=cloudinary://<key>:<secret>@<cloud_name>
```

4) Run the server
```
python run.py
```
Open `http://localhost:5000/` – the frontend (`FRONTEND/index.html`) is served at `/`. Static assets (`/app.js`, `/style.css`) are automatically served from `FRONTEND/`.

API Base URL
------------
- Health: `GET /api/health`
- Auth: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`
- Users: `GET /api/users/profile`, `PUT /api/users/profile`, `GET /api/users/settings`, etc.
- Courses: `GET /api/courses/`, `POST /api/courses/{id}/enroll`, etc.
- Community: `GET /api/community/discussions`, `POST /api/community/discussions`, etc.
- Achievements: `GET /api/achievements/` (skipped in tests if model not present)
- Uploads: `POST /api/upload/avatar`, etc.

Serving the Frontend
--------------------
- `app.py` initializes Flask with `static_folder='FRONTEND'` and returns `index.html` at `/`.
- In `index.html`, reference assets as root-relative:
  - `/app.js`
  - `/style.css`

Testing
-------
Install test dependencies and run the runner:
```
pip install -r requirements-test.txt
python run_tests.py           # all tests
python test_basic.py          # basic smoke tests
python test_simple.py         # app import + health check
```
Notes:
- Some achievement tests are skipped automatically if `models/achievement.py` is not present.
- On Windows terminals, emojis may not render; messages remain functional.

Database Seeding (optional)
---------------------------
If `scripts/seed_database.py` exists, run:
```
python scripts/seed_database.py
```

Common Issues
-------------
- Missing modules (e.g., `bson`, `cloudinary`): install via `pip install pymongo cloudinary`.
- Flask-Limiter warning about in-memory storage is expected for local dev.
- CORS: `FRONTEND_URL` defaults to `http://localhost:3000`; adjust if serving the frontend via Flask at `http://localhost:5000`.

Deployment
----------
- Set production env vars and secrets.
- Use a WSGI server (e.g., `gunicorn`) and a reverse proxy.
- Configure a persistent rate-limit storage backend for Flask-Limiter.

License
-------
Proprietary – for EcoFarm Quest project use.

# 🌱 EcoFarm Quest Backend API

A comprehensive Python Flask backend API for the EcoFarm Quest sustainable farming learning platform.

## 🚀 Features

- **User Authentication & Management**: JWT-based authentication with user profiles and settings
- **Learning Management**: Course enrollment, progress tracking, and quiz system
- **Community Features**: Discussion forums, achievements, and leaderboards
- **File Upload**: Avatar and certificate uploads with Cloudinary integration
- **Real-time Notifications**: In-app notification system
- **RESTful API**: Well-structured REST endpoints with proper error handling
- **Security**: Rate limiting, CORS, input validation, and data sanitization

## 🛠️ Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: MongoDB with PyMongo
- **Authentication**: Flask-JWT-Extended
- **File Upload**: Cloudinary
- **Email**: Flask-Mail
- **Security**: Flask-CORS, Flask-Limiter
- **Validation**: Custom validation functions

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Cloudinary account (for file uploads)
- Gmail account (for email functionality)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd ecofarm-quest-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# Required variables:
# - MONGODB_URI
# - SECRET_KEY
# - JWT_SECRET_KEY
# - CLOUDINARY_* (for file uploads)
# - MAIL_* (for email functionality)
```

### 3. Database Setup

```bash
# Make sure MongoDB is running
# Start MongoDB service

# Seed the database with initial data
python scripts/seed_database.py
```

### 4. Run the Application

```bash
# Development mode
python app.py

# Or using Flask CLI
flask run --host=0.0.0.0 --port=5000
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | User login |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | User logout |
| GET | `/auth/me` | Get current user info |
| POST | `/auth/forgot-password` | Request password reset |
| POST | `/auth/reset-password` | Reset password |

### User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/profile` | Get user profile |
| PUT | `/users/profile` | Update user profile |
| GET | `/users/settings` | Get user settings |
| PUT | `/users/settings` | Update user settings |
| GET | `/users/progress` | Get learning progress |
| PUT | `/users/avatar` | Update user avatar |
| GET | `/users/export-data` | Export user data |
| DELETE | `/users/delete-account` | Delete user account |

### Course Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/courses/` | Get all courses |
| GET | `/courses/<id>` | Get course by ID |
| POST | `/courses/<id>/enroll` | Enroll in course |
| GET | `/courses/<id>/progress` | Get course progress |
| POST | `/courses/<id>/lessons/<lesson_id>/complete` | Complete lesson |
| POST | `/courses/<id>/quiz/<quiz_id>/submit` | Submit quiz |
| GET | `/courses/my-courses` | Get user's courses |
| GET | `/courses/search` | Search courses |

### Community Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/community/discussions` | Get discussions |
| POST | `/community/discussions` | Create discussion |
| GET | `/community/discussions/<id>` | Get discussion details |
| POST | `/community/discussions/<id>/reply` | Reply to discussion |
| POST | `/community/discussions/<id>/like` | Like discussion |
| GET | `/community/leaderboard` | Get leaderboard |
| POST | `/community/leaderboard/update` | Update leaderboard |
| GET | `/community/stats` | Get community stats |

### Achievement Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/achievements/` | Get all achievements |
| GET | `/achievements/categories` | Get achievement categories |
| GET | `/achievements/my-achievements` | Get user achievements |
| POST | `/achievements/check` | Check new achievements |
| GET | `/achievements/leaderboard` | Get achievement leaderboard |

### File Upload Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/avatar` | Upload user avatar |
| POST | `/upload/certificate` | Upload certificate |
| POST | `/upload/course-material` | Upload course material |
| DELETE | `/upload/delete` | Delete uploaded file |
| GET | `/upload/config` | Get upload configuration |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT secret key | Required |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/ecofarm-quest` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Required for uploads |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Required for uploads |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Required for uploads |
| `MAIL_SERVER` | Email server | `smtp.gmail.com` |
| `MAIL_PORT` | Email port | `587` |
| `MAIL_USERNAME` | Email username | Required for emails |
| `MAIL_PASSWORD` | Email password | Required for emails |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |
| `PORT` | Server port | `5000` |

## 🗄️ Database Schema

### Collections

- **users**: User profiles and authentication data
- **courses**: Course information and metadata
- **lessons**: Individual lesson content
- **quizzes**: Quiz questions and answers
- **user_progress**: Overall user learning progress
- **course_progress**: User progress in specific courses
- **lesson_progress**: User progress in specific lessons
- **discussions**: Community discussion posts
- **discussion_replies**: Replies to discussions
- **achievements**: Available achievements
- **leaderboard**: User rankings and points
- **notifications**: User notifications

## 🧪 Testing

```bash
# Run tests (when implemented)
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

## 🚀 Deployment

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📝 API Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Response data
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "error": "Detailed error information"
}
```

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- Rate limiting to prevent abuse
- CORS configuration for cross-origin requests
- Input validation and sanitization
- Password hashing with bcrypt
- File upload validation and size limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Complete API implementation
- User authentication and management
- Course and learning management
- Community features
- File upload functionality
- Achievement system
- Notification system

---

🌱 **EcoFarm Quest** - Empowering farmers through sustainable learning!
# MangoDevelopersWebpage
# testing
