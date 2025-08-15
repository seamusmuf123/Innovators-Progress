import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from modules.nav import SideBarLinks

API_BASE_URL = "http://localhost:4000/api"

def show_home_page():
    """Home page showing app overview and features"""
    st.markdown('<h1 class="main-header">💪 Progress</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Data-Driven Personal Fitness App</h2>', unsafe_allow_html=True)
    
    # App overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 **Our Mission**
        Progress empowers individuals to stay consistent, motivated, and goal-oriented in their fitness journey. 
        Track workouts, monitor progress, and achieve your fitness goals with data-driven insights.
        
        ### 🚀 **Key Features**
        - **Dynamic Progress Visualizer** - See your growth over time
        - **Personalized Goal Setting** - Set and track specific fitness objectives
        - **Routine Library** - Adaptive workout plans based on your results
        - **Consistency Tracking** - Stay accountable with visual progress
        """)
    
    with col2:
        st.markdown("""
        ### 👥 **User Personas**
        
        **👩‍💼 Maya Johnson (Regular User)**
        - Fitness tracking and goal management
        - Routine planning and progress visualization
        
        **👨‍💼 Alex LaFrance (Desk Attendant)**
        - Gym policy management and user monitoring
        - Equipment status and safety oversight
        
        **👨‍💻 Jordan Lee (Analyst)**
        - Workout efficiency analytics
        - Smart recommendations and time management
        
        **👩‍💻 Naomi (System Admin)**
        - System monitoring and maintenance
        - Team collaboration and alerts
        """)
    
    # Quick stats from API
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/gym-usage")
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Users", stats.get('total_users', 'N/A'))
            with col2:
                st.metric("Active Memberships", stats.get('active_memberships', 'N/A'))
            with col3:
                st.metric("Total Workouts", stats.get('total_workouts', 'N/A'))
            with col4:
                st.metric("Avg Duration", f"{stats.get('avg_workout_duration', 'N/A')} min")
        else:
            st.info("API connection: Mock mode active")
    except:
        st.info("API connection: Mock mode active")

def show_maya_page():
    """Maya Johnson - Regular User Interface (Wireframes 1 & 2)"""
    st.markdown('<h1 class="main-header">👩‍💼 Maya Johnson</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Regular User - Fitness Tracking & Goals</h3>', unsafe_allow_html=True)
    
    # User ID input
    user_id = st.number_input("Enter your User ID:", min_value=1, value=1, step=1)
    
    # Two main sections as per wireframes
    tab1, tab2 = st.tabs(["🔐 Login & Workout Logging", "📋 Routine Builder & Tracker"])
    
    with tab1:
        st.markdown("### 🔐 Login to Workout")
        
        # Mock login form
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email:", value="maya@email.com")
            password = st.text_input("Password:", type="password", value="password123")
        
        with col2:
            st.markdown("#### Quick Stats")
            if st.button("Login & Load Data"):
                st.success("✅ Login successful!")
                
                # Load user data
                try:
                    response = requests.get(f"{API_BASE_URL}/goals?user_id={user_id}")
                    if response.status_code == 200:
                        goals_data = response.json()
                        st.metric("Active Goals", goals_data.get('count', 0))
                        st.metric("User ID", user_id)
                except:
                    st.info("Mock data loaded")
    
    with tab2:
        st.markdown("### 📋 Routine Builder & Tracker")
        
        # Goals section
        st.subheader("🎯 Your Fitness Goals")
        try:
            response = requests.get(f"{API_BASE_URL}/goals?user_id={user_id}")
            if response.status_code == 200:
                goals_data = response.json()
                
                if goals_data.get('goals'):
                    for goal in goals_data['goals']:
                        with st.expander(f"🎯 {goal.get('goal_name', 'Goal')}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Task:** {goal.get('task', 'N/A')}")
                                st.write(f"**Status:** {goal.get('status', 'N/A')}")
                            with col2:
                                st.write(f"**Days Remaining:** {goal.get('days_remaining', 'N/A')}")
                                st.progress(0.7)  # Mock progress
                else:
                    st.info("No goals found. Create your first goal!")
        except:
            st.info("Mock data: 2 active goals")
        
        # Create new goal
        st.subheader("➕ Create New Goal")
        with st.form("new_goal"):
            goal_name = st.text_input("Goal Name:")
            task = st.text_area("Task Description:")
            target_date = st.date_input("Target Date:")
            
            if st.form_submit_button("Create Goal"):
                if goal_name and task:
                    st.success("Goal created successfully!")
                else:
                    st.error("Please fill in all fields")
        
        # Available equipment
        st.subheader("🏋️ Available Equipment")
        try:
            response = requests.get(f"{API_BASE_URL}/equipment/available?user_id={user_id}")
            if response.status_code == 200:
                equipment_data = response.json()
                
                if equipment_data.get('equipment'):
                    for equipment in equipment_data['equipment']:
                        st.write(f"✅ {equipment.get('equipment_name')} - {equipment.get('location')}")
                else:
                    st.info("No equipment data available")
        except:
            st.info("Mock data: Treadmill #1, Bench Press #1 available")
        
        # Progress tracker
        st.subheader("📈 Progress Tracker")
        col1, col2 = st.columns(2)
        
        with col1:
            # Mock progress chart
            progress_data = pd.DataFrame({
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'Progress': [20, 35, 50, 65]
            })
            fig = px.line(progress_data, x='Week', y='Progress', title='Weekly Progress')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Mock consistency tracker
            consistency_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Workouts': [1, 1, 0, 1, 1, 0, 1]
            })
            fig = px.bar(consistency_data, x='Day', y='Workouts', title='Weekly Consistency')
            st.plotly_chart(fig, use_container_width=True)

def show_alex_page():
    """Alex LaFrance - Desk Attendant Interface (Wireframes 5 & 6)"""
    st.markdown('<h1 class="main-header">👨‍💼 Alex LaFrance</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Desk Attendant - Gym Management & Safety</h3>', unsafe_allow_html=True)
    
    # Two main sections as per wireframes
    tab1, tab2 = st.tabs(["📊 Workout Analysis Summary", "🧘 Daily Mindfulness"])
    
    with tab1:
        st.markdown("### 📊 Workout Analysis Summary")
        st.markdown("Concise analysis of user workouts with visual charts and numbers")
        
        # Gym policies
        st.subheader("📋 Gym Policies")
        try:
            response = requests.get(f"{API_BASE_URL}/policies")
            if response.status_code == 200:
                policies_data = response.json()
                
                if policies_data.get('policies'):
                    for policy in policies_data['policies']:
                        with st.expander(f"📋 {policy.get('title')}"):
                            st.write(f"**Category:** {policy.get('category')}")
                            st.write(f"**Description:** {policy.get('description')}")
                else:
                    st.info("No policies found")
        except:
            st.info("Mock data: Safety and Security policies available")
        
        # User membership status
        st.subheader("👥 User Membership Status")
        try:
            response = requests.get(f"{API_BASE_URL}/users/membership-status")
            if response.status_code == 200:
                users_data = response.json()
                
                if users_data.get('users'):
                    df = pd.DataFrame(users_data['users'])
                    st.dataframe(df[['name', 'email', 'gym_location', 'current_status']], use_container_width=True)
                else:
                    st.info("No user data available")
        except:
            st.info("Mock data: 4 active users")
        
        # Equipment status
        st.subheader("🏋️ Equipment Status")
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/equipment-utilization")
            if response.status_code == 200:
                util_data = response.json()
                
                if util_data.get('utilization'):
                    for location in util_data['utilization']:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Location", location.get('location'))
                        with col2:
                            st.metric("Available", location.get('available_equipment'))
                        with col3:
                            st.metric("Availability %", f"{location.get('availability_percentage')}%")
                else:
                    st.info("No equipment data available")
        except:
            st.info("Mock data: Cardio Area 50%, Weight Room 100%")
        
        # Mock workout summary chart
        st.subheader("📈 Weekly Workout Summary")
        summary_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Users': [45, 52, 38, 61, 58, 42, 35],
            'Equipment_Usage': [80, 85, 70, 90, 88, 75, 65]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=summary_data['Day'], y=summary_data['Users'], name='Daily Users', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=summary_data['Day'], y=summary_data['Equipment_Usage'], name='Equipment Usage %', mode='lines+markers'))
        fig.update_layout(title='Weekly Gym Activity', xaxis_title='Day', yaxis_title='Count/Percentage')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🧘 Daily Mindfulness")
        st.markdown("Daily and weekly mindfulness quotes for our users")
        
        # Mindfulness quotes
        quotes = [
            "The only bad workout is the one that didn't happen.",
            "Strength doesn't come from what you can do. It comes from overcoming the things you thought you couldn't.",
            "Your body can stand almost anything. It's your mind you have to convince.",
            "The difference between try and triumph is just a little umph!",
            "Make yourself proud.",
            "Every rep counts. Every set matters. Every workout builds you.",
            "Consistency is the key to success."
        ]
        
        st.markdown("#### 🌟 Today's Quote")
        import random
        today_quote = random.choice(quotes)
        st.markdown(f'<div class="persona-card"><h4>"{today_quote}"</h4></div>', unsafe_allow_html=True)
        
        # Weekly mindfulness tracker
        st.markdown("#### 📅 Weekly Mindfulness Tracker")
        mindfulness_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Mood': [8, 7, 9, 6, 8, 9, 7],
            'Energy': [7, 6, 8, 5, 7, 8, 6]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(mindfulness_data, x='Day', y='Mood', title='Weekly Mood (1-10)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(mindfulness_data, x='Day', y='Energy', title='Weekly Energy Level (1-10)')
            st.plotly_chart(fig, use_container_width=True)

def show_jordan_page():
    """Jordan Lee - Analyst Interface (Wireframes 3 & 4)"""
    st.markdown('<h1 class="main-header">👨‍💻 Jordan Lee</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Analyst - Workout Efficiency & Smart Recommendations</h3>', unsafe_allow_html=True)
    
    # User ID input for Jordan
    user_id = st.number_input("Enter your User ID:", min_value=1, value=3, step=1)
    
    # Two main sections as per wireframes
    tab1, tab2 = st.tabs(["📊 Workout Analysis", "🤖 Smart Workout Recommendations"])
    
    with tab1:
        st.markdown("### 📊 Workout Analysis")
        st.markdown("Analysis of workout efficiency and time-based summaries")
        
        # Workout efficiency analytics
        st.subheader("⚡ Workout Efficiency Analytics")
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/workout-efficiency?user_id={user_id}")
            if response.status_code == 200:
                reports_data = response.json()
                
                if reports_data.get('reports'):
                    for report in reports_data['reports']:
                        with st.expander(f"📋 {report.get('title')}"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Efficiency", f"{report.get('work_efficiency')}%")
                            with col2:
                                st.metric("Duration", f"{report.get('workout_duration')} min")
                            with col3:
                                st.metric("Calories", report.get('calories_burned'))
                else:
                    st.info("No workout reports available")
        except:
            st.info("Mock data: Week 1 & Week 2 summaries available")
        
        # Time-based summaries
        st.subheader("⏰ Time-Based Summaries")
        time_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Total_Time': [4.5, 5.25, 6.0, 5.5],
            'Efficiency': [85.5, 92.0, 88.0, 90.5]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(time_data, x='Week', y='Total_Time', title='Weekly Workout Time (Hours)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(time_data, x='Week', y='Efficiency', title='Weekly Efficiency Trend (%)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Goal-based alerts
        st.subheader("🔔 Goal-Based Alerts")
        alerts = [
            "🎯 You're 80% to your strength goal!",
            "⏰ 2 days until your weekly cardio target",
            "💪 Great job hitting 5 workouts this week!",
            "📈 Your endurance has improved 15% this month"
        ]
        
        for alert in alerts:
            st.info(alert)
    
    with tab2:
        st.markdown("### 🤖 Smart Workout Recommendations")
        st.markdown("AI-powered workout suggestions based on your data")
        
        # Smart recommendations
        st.subheader("🧠 AI Recommendations")
        
        # Mock recommendation engine
        recommendations = [
            {
                "type": "Strength Training",
                "reason": "Based on your goal to build lean muscle",
                "workouts": ["Bench Press", "Squats", "Deadlifts", "Pull-ups"],
                "duration": "45-60 minutes",
                "frequency": "3x per week"
            },
            {
                "type": "Cardio",
                "reason": "To improve your endurance and burn calories",
                "workouts": ["HIIT Training", "Running", "Cycling", "Rowing"],
                "duration": "20-30 minutes",
                "frequency": "2x per week"
            },
            {
                "type": "Recovery",
                "reason": "Your body needs rest to build muscle",
                "workouts": ["Stretching", "Yoga", "Foam Rolling", "Light Walking"],
                "duration": "15-20 minutes",
                "frequency": "Daily"
            }
        ]
        
        for i, rec in enumerate(recommendations):
            with st.expander(f"💡 {rec['type']} - {rec['reason']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Workouts:**")
                    for workout in rec['workouts']:
                        st.write(f"• {workout}")
                with col2:
                    st.write(f"**Duration:** {rec['duration']}")
                    st.write(f"**Frequency:** {rec['frequency']}")
                
                if st.button(f"Apply {rec['type']} Plan", key=f"apply_{i}"):
                    st.success(f"✅ {rec['type']} plan applied to your routine!")
        
        # Device syncing status
        st.subheader("📱 Device Syncing Status")
        devices = [
            {"name": "Apple Watch", "status": "✅ Connected", "last_sync": "2 min ago"},
            {"name": "iPhone", "status": "✅ Connected", "last_sync": "1 min ago"},
            {"name": "Fitbit", "status": "❌ Disconnected", "last_sync": "2 hours ago"}
        ]
        
        for device in devices:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.write(f"**{device['name']}**")
            with col2:
                st.write(device['status'])
            with col3:
                st.write(f"Last sync: {device['last_sync']}")

def show_naomi_page():
    """Naomi - System Administrator Interface (Wireframes 7 & 8)"""
    st.markdown('<h1 class="main-header">👩‍💻 Naomi</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">System Administrator - System Monitoring & Team Collaboration</h3>', unsafe_allow_html=True)
    
    # Two main sections as per wireframes
    tab1, tab2 = st.tabs(["🖥️ System Activity", "💬 Team Chat"])
    
    with tab1:
        st.markdown("### 🖥️ System Activity")
        st.markdown("Monitor system health, logs, and alerts")
        
        # System overview
        st.subheader("📊 System Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Status", "🟢 Online", delta="+2.5%")
        with col2:
            st.metric("Active Users", "156", delta="+12")
        with col3:
            st.metric("CPU Usage", "23%", delta="-5%")
        with col4:
            st.metric("Memory", "67%", delta="+3%")
        
        # System alerts
        st.subheader("🚨 System Alerts")
        alerts = [
            {"level": "🟡 Warning", "message": "Disk space at 75%", "time": "5 min ago"},
            {"level": "🟢 Info", "message": "Backup completed successfully", "time": "1 hour ago"},
            {"level": "🟢 Info", "message": "Security scan completed", "time": "2 hours ago"},
            {"level": "🔴 Critical", "message": "Database connection timeout", "time": "10 min ago"}
        ]
        
        for alert in alerts:
            st.markdown(f"**{alert['level']}** - {alert['message']} ({alert['time']})")
        
        # System logs
        st.subheader("📝 Recent System Logs")
        logs = [
            "2025-08-14 19:30:15 - User login: maya@email.com",
            "2025-08-14 19:28:42 - API request: /api/goals?user_id=1",
            "2025-08-14 19:25:18 - Database backup initiated",
            "2025-08-14 19:22:33 - Equipment status updated",
            "2025-08-14 19:20:07 - New user registration: alex@gym.com"
        ]
        
        for log in logs:
            st.code(log, language="text")
        
        # Equipment utilization chart
        st.subheader("📈 Equipment Utilization")
        util_data = pd.DataFrame({
            'Location': ['Cardio Area', 'Weight Room', 'Pool', 'Yoga Studio'],
            'Utilization': [75, 85, 45, 60],
            'Maintenance': [2, 1, 0, 1]
        })
        
        fig = px.bar(util_data, x='Location', y='Utilization', title='Equipment Utilization by Area (%)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Inactive memberships
        st.subheader("❌ Inactive Memberships")
        try:
            response = requests.get(f"{API_BASE_URL}/users/membership-status")
            if response.status_code == 200:
                users_data = response.json()
                
                if users_data.get('users'):
                    df = pd.DataFrame(users_data['users'])
                    inactive_users = df[df['current_status'] == 'Inactive']
                    
                    if not inactive_users.empty:
                        st.dataframe(inactive_users[['name', 'email', 'gym_location']], use_container_width=True)
                    else:
                        st.success("✅ All memberships are active!")
                else:
                    st.info("No user data available")
        except:
            st.info("Mock data: All memberships active")
    
    with tab2:
        st.markdown("### 💬 Team Chat")
        st.markdown("Collaborate with the analysis team using team chat")
        
        # Team members
        st.subheader("👥 Team Members")
        team_members = [
            {"name": "Naomi Smith", "role": "System Admin", "status": "🟢 Online"},
            {"name": "Jordan Lee", "role": "Data Analyst", "status": "🟢 Online"},
            {"name": "Alex LaFrance", "role": "Desk Attendant", "status": "🟡 Away"},
            {"name": "Maya Johnson", "role": "User Support", "status": "🔴 Offline"}
        ]
        
        for member in team_members:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{member['name']}**")
            with col2:
                st.write(member['role'])
            with col3:
                st.write(member['status'])
        
        # Chat interface
        st.subheader("💬 Team Chat")
        
        # Mock chat messages
        chat_messages = [
            {"user": "Naomi", "message": "System maintenance scheduled for tonight at 2 AM", "time": "19:25"},
            {"user": "Jordan", "message": "Got it. Will ensure all users are notified", "time": "19:26"},
            {"user": "Alex", "message": "Equipment check completed. All systems operational", "time": "19:28"},
            {"user": "Naomi", "message": "Great work team! Database backup completed successfully", "time": "19:30"}
        ]
        
        # Display chat
        chat_container = st.container()
        with chat_container:
            for msg in chat_messages:
                if msg['user'] == 'Naomi':
                    st.markdown(f'<div style="text-align: right; margin: 10px 0;"><strong>{msg["user"]}</strong> ({msg["time"]})<br><div style="background-color: #e3f2fd; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">{msg["message"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="text-align: left; margin: 10px 0;"><strong>{msg["user"]}</strong> ({msg["time"]})<br><div style="background-color: #f5f5f5; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">{msg["message"]}</div></div>', unsafe_allow_html=True)
        
        # Send message
        st.subheader("✍️ Send Message")
        with st.form("chat_form"):
            message = st.text_area("Your message:")
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.form_submit_button("Send"):
                    if message:
                        st.success("Message sent!")
                    else:
                        st.error("Please enter a message")

def main():
    st.set_page_config(
        page_title="Progress - Data-Driven Fitness App",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .persona-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🏠 Progress App")
    page = st.sidebar.selectbox(
        "Choose your role:",
        [
            "🏠 Home",
            "👩‍💼 Maya Johnson (User)",
            "👨‍💼 Alex LaFrance (Desk Attendant)", 
            "👨‍💻 Jordan Lee (Analyst)",
            "👩‍💻 Naomi (System Admin)"
        ]
    )
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "👩‍💼 Maya Johnson (User)":
        show_maya_page()
    elif page == "👨‍💼 Alex LaFrance (Desk Attendant)":
        show_alex_page()
    elif page == "👨‍💻 Jordan Lee (Analyst)":
        show_jordan_page()
    elif page == "👩‍💻 Naomi (System Admin)":
        show_naomi_page()

if __name__ == "__main__":
    main()
