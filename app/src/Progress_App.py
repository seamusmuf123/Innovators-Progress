import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Progress - Fitness App",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = "http://localhost:4000/api"

def main():
    st.title("💪 Progress - Data-Driven Fitness App")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
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

def show_home_page():
    """Home page with app overview and team information"""
    st.header("Welcome to Progress! 🎯")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Progress** is a comprehensive, data-driven personal fitness application designed to help users stay consistent, 
        motivated, and goal-oriented in their fitness journey.
        
        ### Key Features:
        - 🎯 **Dynamic Progress Visualizer** - Track your fitness journey with detailed analytics
        - 📱 **Personalized Goal Setting** - Set and monitor fitness goals with smart tracking
        - 🏋️ **Routine Library** - Access workout plans that adapt to your progress
        - 📊 **Comprehensive Analytics** - Data-driven insights for better performance
        - 🔄 **Device Syncing** - Track progress across multiple devices
        - 🏢 **Gym Management** - Complete gym operations and safety monitoring
        
        ### User Personas:
        1. **👩‍💼 Maya Johnson** - Regular user seeking fitness tracking and goal management
        2. **👨‍💼 Alex LaFrance** - Desk attendant managing gym operations and safety
        3. **👨‍💻 Jordan Lee** - Analyst requiring data insights and recommendations
        4. **👩‍💻 Naomi** - System administrator maintaining app performance
        """)
    
    with col2:
        st.markdown("""
        ### Team Innovators
        - **Samuel Ayedun** (Point Person)
        - **Amir Sesay**
        - **Seamus Mufarinya**
        - **Kevin Akaho**
        - **Oluchukwu Egbuna**
        
        **Course:** CS 3200 - Summer 2 2025
        """)
        
        # Quick stats
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/gym-usage")
            if response.status_code == 200:
                stats = response.json()
                st.metric("Total Users", stats.get('total_users', 0))
                st.metric("Active Memberships", stats.get('active_memberships', 0))
                st.metric("Total Workouts", stats.get('total_workouts', 0))
        except:
            st.info("API connection required for live stats")
    
    st.markdown("---")
    st.markdown("### Getting Started")
    st.markdown("""
    Select your role from the sidebar to access personalized features and functionality.
    Each persona has specific tools and insights tailored to their needs.
    """)

def show_maya_page():
    """Maya Johnson's page - Regular user fitness tracking"""
    st.header("👩‍💼 Maya Johnson - Fitness Tracking Dashboard")
    st.markdown("**Goal:** Lose 10 pounds and gain lean muscle")
    
    # User ID input
    user_id = st.number_input("Enter your User ID:", min_value=1, value=1, key="maya_user_id")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Current Goals")
        try:
            response = requests.get(f"{API_BASE_URL}/goals?user_id={user_id}")
            if response.status_code == 200:
                goals = response.json()
                if goals['goals']:
                    for goal in goals['goals']:
                        with st.expander(f"🎯 {goal['goal_name']}"):
                            st.write(f"**Task:** {goal['task']}")
                            st.write(f"**Tracking:** {goal['tracking']}")
                            st.write(f"**Status:** {goal['status']}")
                            st.write(f"**Target Date:** {goal['target_date']}")
                            st.write(f"**Days Remaining:** {goal['days_remaining']}")
                else:
                    st.info("No goals found. Create your first fitness goal!")
            else:
                st.error("Failed to load goals")
        except:
            st.error("API connection failed")
        
        # Create new goal
        st.subheader("➕ Create New Goal")
        with st.form("new_goal_form"):
            goal_name = st.text_input("Goal Name")
            task = st.text_input("Task Description")
            tracking = st.text_input("Tracking Method")
            target_date = st.date_input("Target Date")
            
            if st.form_submit_button("Create Goal"):
                if goal_name and task:
                    try:
                        data = {
                            "user_ID": user_id,
                            "goal_name": goal_name,
                            "task": task,
                            "tracking": tracking,
                            "target_date": target_date.strftime("%Y-%m-%d")
                        }
                        response = requests.post(f"{API_BASE_URL}/goals", json=data)
                        if response.status_code == 201:
                            st.success("Goal created successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to create goal")
                    except:
                        st.error("API connection failed")
    
    with col2:
        st.subheader("🏋️ Available Equipment")
        try:
            response = requests.get(f"{API_BASE_URL}/equipment/available?user_id={user_id}")
            if response.status_code == 200:
                equipment = response.json()
                if equipment['equipment']:
                    df = pd.DataFrame(equipment['equipment'])
                    st.dataframe(df[['equipment_name', 'location', 'condition']], use_container_width=True)
                else:
                    st.info("No equipment information available")
            else:
                st.error("Failed to load equipment")
        except:
            st.error("API connection failed")
        
        st.subheader("📊 Progress Tracker")
        try:
            response = requests.get(f"{API_BASE_URL}/progress/tracker?user_id={user_id}")
            if response.status_code == 200:
                progress = response.json()
                if progress['goals']:
                    # Create progress chart
                    goal_names = [g['goal_name'] for g in progress['goals']]
                    days_remaining = [g['days_remaining'] for g in progress['goals']]
                    
                    fig = px.bar(
                        x=goal_names,
                        y=days_remaining,
                        title="Days Remaining for Goals",
                        labels={'x': 'Goals', 'y': 'Days Remaining'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No progress data available")
            else:
                st.error("Failed to load progress")
        except:
            st.error("API connection failed")

def show_alex_page():
    """Alex LaFrance's page - Desk attendant gym management"""
    st.header("👨‍💼 Alex LaFrance - Gym Management Dashboard")
    st.markdown("**Role:** Front desk attendant ensuring gym safety and access control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Gym Policies")
        try:
            response = requests.get(f"{API_BASE_URL}/policies")
            if response.status_code == 200:
                policies = response.json()
                if policies['policies']:
                    for policy in policies['policies']:
                        with st.expander(f"📋 {policy['title']}"):
                            st.write(f"**Category:** {policy['category']}")
                            st.write(f"**Description:** {policy['description']}")
                            st.write(f"**Created:** {policy['created_at']}")
                else:
                    st.info("No policies found")
            else:
                st.error("Failed to load policies")
        except:
            st.error("API connection failed")
        
        st.subheader("👥 User Membership Status")
        try:
            response = requests.get(f"{API_BASE_URL}/users/membership-status")
            if response.status_code == 200:
                users = response.json()
                if users['users']:
                    df = pd.DataFrame(users['users'])
                    st.dataframe(df[['name', 'email', 'gym_location', 'current_status']], use_container_width=True)
                else:
                    st.info("No users found")
            else:
                st.error("Failed to load users")
        except:
            st.error("API connection failed")
    
    with col2:
        st.subheader("🎥 Security Monitoring")
        try:
            days = st.slider("Days back to check:", 1, 30, 7)
            response = requests.get(f"{API_BASE_URL}/security/video-footage?days={days}")
            if response.status_code == 200:
                footage = response.json()
                if footage['footage']:
                    df = pd.DataFrame(footage['footage'])
                    st.dataframe(df[['camera_ID', 'location', 'timestamp', 'duration_seconds']], use_container_width=True)
                else:
                    st.info(f"No video footage found in the last {days} days")
            else:
                st.error("Failed to load video footage")
        except:
            st.error("API connection failed")
        
        st.subheader("🏋️ Equipment Status")
        try:
            response = requests.get(f"{API_BASE_URL}/equipment/status")
            if response.status_code == 200:
                equipment = response.json()
                if equipment['equipment']:
                    df = pd.DataFrame(equipment['equipment'])
                    
                    # Equipment status chart
                    status_counts = df['condition'].value_counts()
                    fig = px.pie(
                        values=status_counts.values,
                        names=status_counts.index,
                        title="Equipment Status Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(df[['equipment_name', 'location', 'condition', 'status_description']], use_container_width=True)
                else:
                    st.info("No equipment found")
            else:
                st.error("Failed to load equipment")
        except:
            st.error("API connection failed")

def show_jordan_page():
    """Jordan Lee's page - Analyst data insights"""
    st.header("👨‍💻 Jordan Lee - Analytics Dashboard")
    st.markdown("**Role:** Data analyst seeking workout efficiency insights")
    
    # User ID input
    user_id = st.number_input("Enter your User ID:", min_value=1, value=3, key="jordan_user_id")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Workout Efficiency Analytics")
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/workout-efficiency?user_id={user_id}")
            if response.status_code == 200:
                reports = response.json()
                if reports['reports']:
                    df = pd.DataFrame(reports['reports'])
                    
                    # Efficiency trend chart
                    fig = px.line(
                        df,
                        x='report_date',
                        y='work_efficiency',
                        title="Workout Efficiency Over Time",
                        labels={'work_efficiency': 'Efficiency %', 'report_date': 'Date'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(df[['title', 'work_efficiency', 'workout_duration', 'calories_burned']], use_container_width=True)
                else:
                    st.info("No workout reports found")
            else:
                st.error("Failed to load workout efficiency data")
        except:
            st.error("API connection failed")
        
        st.subheader("⏰ Time-Based Summaries")
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/time-summaries?user_id={user_id}")
            if response.status_code == 200:
                summaries = response.json()
                if summaries['summaries']:
                    df = pd.DataFrame(summaries['summaries'])
                    
                    # Duration chart
                    fig = px.bar(
                        df,
                        x='report_date',
                        y='workout_duration',
                        title="Workout Duration by Date",
                        labels={'workout_duration': 'Duration (minutes)', 'report_date': 'Date'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(df[['title', 'formatted_duration', 'calories_burned', 'time_based_summary']], use_container_width=True)
                else:
                    st.info("No time summaries found")
            else:
                st.error("Failed to load time summaries")
        except:
            st.error("API connection failed")
    
    with col2:
        st.subheader("📱 Device Syncing")
        try:
            response = requests.get(f"{API_BASE_URL}/devices/sync?user_id={user_id}")
            if response.status_code == 200:
                devices = response.json()
                if devices['devices']:
                    df = pd.DataFrame(devices['devices'])
                    st.dataframe(df[['device_type', 'device_name', 'transfer', 'last_sync', 'is_active']], use_container_width=True)
                else:
                    st.info("No devices found")
            else:
                st.error("Failed to load device information")
        except:
            st.error("API connection failed")
        
        st.subheader("🎯 Goal Alerts")
        try:
            response = requests.get(f"{API_BASE_URL}/goals?user_id={user_id}")
            if response.status_code == 200:
                goals = response.json()
                if goals['goals']:
                    for goal in goals['goals']:
                        days_remaining = goal.get('days_remaining', 0)
                        if days_remaining <= 7:
                            st.error(f"🚨 URGENT: {goal['goal_name']} due in {days_remaining} days!")
                        elif days_remaining <= 30:
                            st.warning(f"⚠️ {goal['goal_name']} due in {days_remaining} days")
                        else:
                            st.success(f"✅ {goal['goal_name']} - {days_remaining} days remaining")
                else:
                    st.info("No goals found")
            else:
                st.error("Failed to load goals")
        except:
            st.error("API connection failed")

def show_naomi_page():
    """Naomi's page - System administrator"""
    st.header("👩‍💻 Naomi - System Administration Dashboard")
    st.markdown("**Role:** System administrator maintaining app performance and user experience")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 System Alerts")
        try:
            response = requests.get(f"{API_BASE_URL}/system/status")
            if response.status_code == 200:
                systems = response.json()
                if systems['systems']:
                    for system in systems['systems']:
                        if system['status'] != 'online':
                            st.error(f"🔴 {system['system_name']}: {system['alert_status']}")
                        elif system['alerts']:
                            st.warning(f"⚠️ {system['system_name']}: {system['alerts']}")
                        else:
                            st.success(f"✅ {system['system_name']}: {system['alert_status']}")
                else:
                    st.success("✅ All systems operational")
            else:
                st.error("Failed to load system status")
        except:
            st.error("API connection failed")
        
        st.subheader("📋 System Logs")
        try:
            response = requests.get(f"{API_BASE_URL}/system/logs")
            if response.status_code == 200:
                logs = response.json()
                if logs['logs']:
                    for log in logs['logs'][:5]:  # Show last 5 logs
                        with st.expander(f"📋 {log['system_name']} - {log['last_updated']}"):
                            st.write(f"**Status:** {log['status']}")
                            st.write(f"**Logs:** {log['logs']}")
                            st.write(f"**Admin:** {log['admin_name']}")
                else:
                    st.info("No system logs found")
            else:
                st.error("Failed to load system logs")
        except:
            st.error("API connection failed")
    
    with col2:
        st.subheader("👥 Inactive Memberships")
        try:
            response = requests.get(f"{API_BASE_URL}/users/inactive-memberships")
            if response.status_code == 200:
                users = response.json()
                if users['users']:
                    df = pd.DataFrame(users['users'])
                    st.dataframe(df[['name', 'email', 'membership_status', 'end_date']], use_container_width=True)
                else:
                    st.success("✅ All memberships are active")
            else:
                st.error("Failed to load inactive memberships")
        except:
            st.error("API connection failed")
        
        st.subheader("📊 System Overview")
        try:
            # Get overall stats
            response = requests.get(f"{API_BASE_URL}/analytics/gym-usage")
            if response.status_code == 200:
                stats = response.json()
                
                # Create metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Users", stats.get('total_users', 0))
                with col2:
                    st.metric("Active Memberships", stats.get('active_memberships', 0))
                with col3:
                    st.metric("Total Workouts", stats.get('total_workouts', 0))
                
                # Equipment utilization
                response = requests.get(f"{API_BASE_URL}/analytics/equipment-utilization")
                if response.status_code == 200:
                    utilization = response.json()
                    if utilization['utilization']:
                        df = pd.DataFrame(utilization['utilization'])
                        fig = px.bar(
                            df,
                            x='location',
                            y='availability_percentage',
                            title="Equipment Availability by Location",
                            labels={'availability_percentage': 'Availability %', 'location': 'Location'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Failed to load system overview")
        except:
            st.error("API connection failed")

if __name__ == "__main__":
    main()
