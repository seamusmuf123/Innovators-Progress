import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

API_BASE_URL = "http://localhost:4000/api"

# Simplified user page: show editable routine and goals tables without persona-specific Maya UI
SideBarLinks()

st.title("User - Routine & Goals")

# Routine planning (30 example rows if not present)
if 'routine_plan' not in st.session_state:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workouts = [
        "Bench Press", "Running", "Pull-ups", "Squats", "Deadlift", "Cycling", "Yoga",
        "Push-ups", "Plank", "Rowing", "Jump Rope", "Lunges", "Burpees", "Box Jumps",
        "Dumbbell Curl", "Tricep Dip", "Lat Pulldown", "Shoulder Press", "Mountain Climbers",
        "Leg Press", "Chest Fly", "Russian Twist", "Step-ups", "Hamstring Curl", "Calf Raise",
        "Crunches", "Back Extension", "Farmer's Walk", "Sled Push", "Battle Ropes", "Wall Sit"
    ]
    st.session_state['routine_plan'] = pd.DataFrame([
        {"Day": days[i % 7], "Workout": workouts[i], "Sets": 3 + (i % 3), "Reps": 8 + (i % 5)}
        for i in range(30)
    ])

st.subheader("Routine Planning")
routine_df = st.session_state['routine_plan']
routine_edit_df = st.data_editor(routine_df, num_rows="dynamic", key="routine_editor")
if st.button("Update Routine"):
    st.session_state['routine_plan'] = routine_edit_df
    st.success("Routine updated")

st.divider()

# Goals and progress (30 example rows if not present)
if 'goal_progress' not in st.session_state:
    st.session_state['goal_progress'] = pd.DataFrame([
        {"Goal": f"Goal {i+1}", "Target": round(5 + i * 0.5, 1), "Week": f"Week {(i % 10) + 1}", "Progress Value": round((5 + i * 0.5) * (0.1 + 0.03 * (i % 10)), 2)}
        for i in range(30)
    ])

st.subheader("Set Your Goals and Track Progress")
goal_df = st.session_state['goal_progress']
edited_goal_df = st.data_editor(goal_df[['Goal','Target','Week','Progress Value']], num_rows="dynamic", key="goal_editor")

def calc_progress(row):
    try:
        if pd.isna(row["Target"]) or row["Target"] == 0:
            return 0.0
        return round((row["Progress Value"] / row["Target"]) * 100, 1)
    except Exception:
        return 0.0

st.divider()
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

API_BASE_URL = "http://localhost:8501"

API_BASE_URL = "http://localhost:4000/api"

# Simplified user page: show editable routine and goals tables without persona-specific Maya UI
SideBarLinks()

st.title("User - Routine & Goals")

# Routine planning (30 example rows if not present)
if 'routine_plan' not in st.session_state:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workouts = [
        "Bench Press", "Running", "Pull-ups", "Squats", "Deadlift", "Cycling", "Yoga",
        "Push-ups", "Plank", "Rowing", "Jump Rope", "Lunges", "Burpees", "Box Jumps",
        "Dumbbell Curl", "Tricep Dip", "Lat Pulldown", "Shoulder Press", "Mountain Climbers",
        "Leg Press", "Chest Fly", "Russian Twist", "Step-ups", "Hamstring Curl", "Calf Raise",
        "Crunches", "Back Extension", "Farmer's Walk", "Sled Push", "Battle Ropes", "Wall Sit"
    ]
    st.session_state['routine_plan'] = pd.DataFrame([
        {"Day": days[i % 7], "Workout": workouts[i], "Sets": 3 + (i % 3), "Reps": 8 + (i % 5)}
        for i in range(30)
    ])

st.subheader("Routine Planning")
routine_df = st.session_state['routine_plan']
routine_edit_df = st.data_editor(routine_df, num_rows="dynamic", key="routine_editor")
if st.button("Update Routine"):
    st.session_state['routine_plan'] = routine_edit_df
    st.success("Routine updated")

st.divider()

# Goals and progress (30 example rows if not present)
if 'goal_progress' not in st.session_state:
    st.session_state['goal_progress'] = pd.DataFrame([
        {"Goal": f"Goal {i+1}", "Target": round(5 + i * 0.5, 1), "Week": f"Week {(i % 10) + 1}", "Progress Value": round((5 + i * 0.5) * (0.1 + 0.03 * (i % 10)), 2)}
        for i in range(30)
    ])

st.subheader("Set Your Goals and Track Progress")
goal_df = st.session_state['goal_progress']
editable_cols = [c for c in goal_df.columns if c in ["Goal", "Target", "Week", "Progress Value"]]
edited_goal_df = st.data_editor(goal_df[editable_cols], num_rows="dynamic", key="goal_editor")

def calc_progress(row):
    try:
        if pd.isna(row["Target"]) or row["Target"] == 0:
            return 0.0
        return round((row["Progress Value"] / row["Target"]) * 100, 1)
    except Exception:
        return 0.0

edited_goal_df["Progress (%)"] = edited_goal_df.apply(calc_progress, axis=1)
if st.button("Update Goals"):
    st.session_state['goal_progress'] = edited_goal_df
    st.success("Goals updated")

st.divider()

# Post progress form
st.write("#### Post Progress for a Goal")
goal_df = st.session_state['goal_progress']
goal_options = goal_df["Goal"].unique().tolist() + ["Create New Goal"]
with st.form("post_progress_form"):
    selected_goal = st.selectbox("Select Goal", goal_options)
    if selected_goal == "Create New Goal":
        new_goal = st.text_input("New Goal Name")
        new_target = st.number_input("Target", min_value=0.0, step=0.1)
        goal_to_use = new_goal
        target_to_use = new_target
    else:
        goal_to_use = selected_goal
        target_to_use = goal_df[goal_df["Goal"] == selected_goal].iloc[0]["Target"]
    selected_week = st.text_input("Week", value="Week 1")
    progress_value = st.number_input("Progress Value", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Post Progress")
    if submitted and goal_to_use and selected_week:
        new_row = {"Goal": goal_to_use, "Target": target_to_use, "Week": selected_week, "Progress Value": progress_value}
        st.session_state['goal_progress'] = pd.concat([st.session_state['goal_progress'], pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Progress posted for {goal_to_use} in {selected_week}")

st.subheader("Your Goals")
display_df = st.session_state['goal_progress'].copy()
display_df["Progress (%)"] = display_df.apply(calc_progress, axis=1)
st.dataframe(display_df, use_container_width=True, hide_index=True)

# Example: Weekly Gym Activity Summary (move this into a suitable tab or section if needed)
summary_data = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'Users': [120, 135, 110, 150, 145, 130, 125],
    'Equipment_Usage': [80, 85, 70, 90, 88, 75, 65]
})

fig = go.Figure()
fig.add_trace(go.Scatter(x=summary_data['Day'], y=summary_data['Users'], name='Daily Users', mode='lines+markers'))
fig.add_trace(go.Scatter(x=summary_data['Day'], y=summary_data['Equipment_Usage'], name='Equipment Usage %', mode='lines+markers'))
fig.update_layout(title='Weekly Gym Activity', xaxis_title='Day', yaxis_title='Count/Percentage')
st.plotly_chart(fig, use_container_width=True)

# Daily Mindfulness Section (removed invalid tab2 context)
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