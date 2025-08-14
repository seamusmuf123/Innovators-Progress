import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import datetime
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('User Goal')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# 1. Gym Equipment Table
st.subheader("Available Gym Equipment")
equipment_data = {
    "Equipment": ["Treadmill", "Bench Press", "Dumbbells", "Pull-up Bar", "Rowing Machine"],
    "Available": ["Yes", "No", "Yes", "Yes", "No"],
    "Location": ["Cardio Zone", "Strength Area", "Strength Area", "Strength Area", "Cardio Zone"]
}
equipment_df = pd.DataFrame(equipment_data)
st.dataframe(equipment_df, use_container_width=True, key="equipment_table")

# 2. Weekly Reminder
st.info("Stay consistent! Remember to log your workouts this week.")

# 3. Routine Planning Table
st.subheader("Routine Planning")
if 'routine_plan' not in st.session_state:
    st.session_state['routine_plan'] = pd.DataFrame([
        {"Day": "Monday", "Workout": "Bench Press", "Sets": 3, "Reps": 10},
        {"Day": "Wednesday", "Workout": "Running", "Sets": 1, "Reps": 20},
        {"Day": "Friday", "Workout": "Pull-ups", "Sets": 4, "Reps": 8},
    ])
routine_df = st.data_editor(
    st.session_state['routine_plan'],
    num_rows="dynamic",
    key="routine_editor"
)
if st.button("Update Routine", key="update_routine"):
    st.session_state['routine_plan'] = routine_df
    st.success("Routine updated!")



# 4. Unified Goal Setting & Progress Tracking Table
st.subheader("Set Your Goals and Track Progress")
if 'goal_progress' not in st.session_state:
    st.session_state['goal_progress'] = pd.DataFrame([
        {"Goal": "Increase bench by 15lbs", "Target": 15, "Deadline": "2025-09-01", "Week": "Week 1", "Progress Value": 2.5},
        {"Goal": "Increase bench by 15lbs", "Target": 15, "Deadline": "2025-09-01", "Week": "Week 2", "Progress Value": 5.0},
        {"Goal": "Decrease mile time", "Target": 1, "Deadline": "2025-10-15", "Week": "Week 1", "Progress Value": 0.2},
        {"Goal": "Decrease mile time", "Target": 1, "Deadline": "2025-10-15", "Week": "Week 2", "Progress Value": 0.4},
    ])


# Post Progress for a Goal (adds a new row to the unified table, with 'Create New Goal' option)
st.write("#### Post Progress for a Goal")
goal_df = st.session_state['goal_progress']
goal_options = goal_df["Goal"].unique().tolist() + ["Create New Goal"]
with st.form("post_progress_form"):
    selected_goal = st.selectbox("Select Goal", goal_options)
    if selected_goal == "Create New Goal":
        new_goal = st.text_input("New Goal Name")
        new_target = st.number_input("Target (e.g., lbs to increase)", min_value=0.0, step=0.1)
        new_deadline = st.text_input("Deadline (YYYY-MM-DD)")
        goal_to_use = new_goal
        target_to_use = new_target
        deadline_to_use = new_deadline
    else:
        goal_to_use = selected_goal
        # Use the first matching row for target and deadline
        goal_row = goal_df[goal_df["Goal"] == selected_goal].iloc[0]
        target_to_use = goal_row["Target"]
        deadline_to_use = goal_row["Deadline"]
    selected_week = st.text_input("Week (e.g., Week 3)")
    progress_value = st.number_input("Progress Value (e.g., lbs increased)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Post Progress")
    if submitted and goal_to_use and selected_week:
        new_row = {
            "Goal": goal_to_use,
            "Target": target_to_use,
            "Deadline": deadline_to_use,
            "Week": selected_week,
            "Progress Value": progress_value
        }
        st.session_state['goal_progress'] = pd.concat([
            st.session_state['goal_progress'],
            pd.DataFrame([new_row])
        ], ignore_index=True)
        st.success(f"Progress posted for {goal_to_use} in {selected_week}!")
        goal_df = st.session_state['goal_progress']


# Always calculate Progress (%) and show only one table
goal_df = goal_df.copy()
goal_df["Progress (%)"] = (goal_df["Progress Value"] / goal_df["Target"] * 100).round(1)
st.session_state['goal_progress'] = goal_df
st.dataframe(goal_df, use_container_width=True, hide_index=True)

# For plotting, aggregate by Goal and Week (take the latest Progress Value for each pair)
chart_df = goal_df.sort_values("Week").drop_duplicates(subset=["Goal", "Week"], keep="last")
st.subheader("Your Progress Over Time (All Goals)")
if not chart_df.empty:
    st.line_chart(chart_df.pivot(index='Week', columns='Goal', values='Progress (%)'))
else:
    st.write("No progress data to display.")

# 5. Visual Progress Tracker
st.subheader("Your Progress Over Time (All Goals)")
if not st.session_state['goal_progress'].empty:
    chart_df = st.session_state['goal_progress'].copy()
    chart_df['Progress (%)'] = pd.to_numeric(chart_df['Progress (%)'], errors='coerce')
    st.line_chart(chart_df.pivot(index='Week', columns='Goal', values='Progress (%)'))
else:
    st.write("No progress data to display.")

# 6. Consistency Tracker (Streak)
st.subheader("Consistency Tracker")
if 'consistency' not in st.session_state:
    st.session_state['consistency'] = 3  # Example: 3 days in a row
st.metric("Current Streak (days)", st.session_state['consistency'])
