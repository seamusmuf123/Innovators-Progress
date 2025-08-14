# 🚀 Progress Fitness App - Complete Setup Guide

## 📋 **Prerequisites**

1. **Python 3.8+** installed
2. **MySQL Server** running locally
3. **Git** for cloning the repository

## 🗄️ **Step 1: Set Up MySQL Database**

### **Option A: Install MySQL Locally**
1. Download MySQL from [mysql.com](https://dev.mysql.com/downloads/)
2. Install with default settings
3. Set root password as `password` (or update the config files)

### **Option B: Use Docker (Recommended)**
```bash
# Start MySQL container
docker run --name progress-mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=progress \
  -p 3306:3306 \
  -d mysql:8.0

# Wait for MySQL to start (check logs)
docker logs progress-mysql
```

## 🐍 **Step 2: Install Python Dependencies**

```bash
# Install backend dependencies
pip install -r api/requirements.txt

# Install frontend dependencies  
pip install -r app/requirements.txt

# Install database setup dependencies
pip install -r database-files/requirements.txt
```

## 🗃️ **Step 3: Set Up Database Schema & Sample Data**

```bash
# Navigate to database-files directory
cd database-files

# Run the database setup script
python setup_database.py
```

**Expected Output:**
```
🚀 Setting up Progress Fitness App Database...
✅ Database 'progress' created successfully
✅ All tables created successfully
✅ Sample data inserted successfully
✅ Database setup completed successfully!

📊 Database Summary:
   Users: 4
   Goals: 3
   Equipment: 4
```

## 🔧 **Step 4: Configure Database Connection**

The backend is configured to connect to:
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: `password`
- **Database**: `progress`

**To change these settings**, edit `api/backend_app.py`:
```python
DB_CONFIG = {
    'host': 'your_host',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'progress',
    'port': 3306
}
```

## 🚀 **Step 5: Start the Backend API**

```bash
# Navigate to api directory
cd api

# Start the Flask backend
python backend_app.py
```

**Expected Output:**
```
🚀 Progress Fitness App Backend Starting...
🌐 Server: http://localhost:4000
🔗 Health Check: http://localhost:4000/health
📊 Database: localhost:3306/progress
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:4000
```

## 🌐 **Step 6: Start the Frontend App**

```bash
# Open new terminal, navigate to app/src
cd app/src

# Start Streamlit frontend
streamlit run Progress_App.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## ✅ **Step 7: Verify Everything is Working**

### **Test Backend API:**
```bash
# Health check
curl http://localhost:4000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-08-14T...",
  "database": "connected"
}
```

### **Test Frontend:**
1. Open http://localhost:8501
2. Navigate through different user personas
3. Verify data is loading from database (not hardcoded)

## 🧪 **Test Data Available**

The setup script creates these sample users:

| User ID | Name | Email | Role | Gym Location |
|---------|------|-------|------|--------------|
| 1 | Maya Johnson | maya@email.com | Regular User | Downtown Gym |
| 2 | Alex LaFrance | alex@gym.com | Staff | Downtown Gym |
| 3 | Jordan Lee | jordan@email.com | Regular User | Westside Gym |
| 4 | Naomi Smith | naomi@admin.com | Admin | Central Gym |

## 🔍 **Troubleshooting**

### **Database Connection Issues:**
```bash
# Check MySQL status
mysql -u root -p -e "SELECT VERSION();"

# Verify database exists
mysql -u root -p -e "SHOW DATABASES;"

# Check tables
mysql -u root -p -e "USE progress; SHOW TABLES;"
```

### **Port Conflicts:**
- **Backend**: Change port in `api/backend_app.py` (line with `app.run(port=4000)`)
- **Frontend**: Change port in Streamlit command: `streamlit run Progress_App.py --server.port 8502`

### **Python Package Issues:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install specific versions if needed
pip install mysql-connector-python==8.1.0
```

## 📱 **Using the App**

1. **Home Page**: Overview of the app and user personas
2. **Maya Johnson (User ID: 1)**: Fitness tracking and goals
3. **Alex LaFrance (User ID: 2)**: Gym management and policies
4. **Jordan Lee (User ID: 3)**: Analytics and recommendations
5. **Naomi (User ID: 4)**: System monitoring and team chat

## 🎯 **Key Features Working**

- ✅ **Real Database**: All data comes from MySQL, not hardcoded
- ✅ **User Management**: Create, view, and manage fitness goals
- ✅ **Equipment Status**: Real-time equipment availability
- ✅ **Analytics**: Workout efficiency and progress tracking
- ✅ **Policies**: Gym policies and membership management
- ✅ **Team Collaboration**: System admin features and team chat

## 🚀 **Next Steps**

1. **Customize Data**: Modify `database-files/setup_database.py` to add more sample data
2. **Add Features**: Extend the API endpoints in `api/backend_app.py`
3. **Enhance UI**: Modify the Streamlit components in `app/src/Progress_App.py`
4. **Production**: Deploy to cloud services with proper security

---

**🎉 Congratulations! Your Progress Fitness App is now running with real database integration!**
