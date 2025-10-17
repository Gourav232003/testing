# MongoDB Setup Guide for EcoFarm Quest

## 🚀 Quick Setup (Recommended)

### Option 1: Use MongoDB Atlas (Cloud - Free)
1. **Go to**: https://www.mongodb.com/atlas
2. **Sign up** for a free account
3. **Create a new cluster** (free tier)
4. **Get your connection string** from "Connect" → "Connect your application"
5. **Replace the connection string** in `.env` file

### Option 2: Use Local MongoDB (If you have it installed)
```bash
# Start MongoDB service
net start MongoDB

# Or if using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 🔧 Current Issue
The application is trying to connect to MongoDB but the connection string is invalid.

## ✅ Working Solution

### Step 1: Get a Real MongoDB Atlas Connection
1. Go to https://www.mongodb.com/atlas
2. Create a free account
3. Create a new cluster (M0 Sandbox - Free)
4. Create a database user with username/password
5. Whitelist your IP address (0.0.0.0/0 for all IPs)
6. Get the connection string

### Step 2: Update .env File
Replace the MONGODB_URI in your `.env` file with the real connection string:

```
MONGODB_URI=mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/ecofarm-quest?retryWrites=true&w=majority
```

### Step 3: Test the Connection
```bash
python run.py
```

## 🆘 Alternative: Use Mock Database for Testing
If you want to test without setting up MongoDB Atlas, I can modify the code to use mongomock for development.

## 📞 Need Help?
1. **MongoDB Atlas Setup**: https://docs.atlas.mongodb.com/getting-started/
2. **Free Tier**: https://www.mongodb.com/atlas/database/free
3. **Connection String Format**: https://docs.mongodb.com/manual/reference/connection-string/

## 🎯 Quick Fix
The easiest solution is to:
1. Sign up for MongoDB Atlas (free)
2. Create a cluster
3. Get the connection string
4. Update your `.env` file
5. Run the application

Your application will then work with a real cloud database! 🌱
