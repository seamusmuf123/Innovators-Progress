import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import datetime
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('User Goal')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# You can access the session state to make a more customized/personalized app experience
st.write('Your Goal:')

# Initialize combined DataFrame in session state
if 'goal_progress' not in st.session_state:
    st.session_state['goal_progress'] = pd.DataFrame([
        {"Goal": "Increase bench by 15lbs", "Deadline": "2025-09-01", "Week": "Week 1", "Progress (%)": 10},
        {"Goal": "Increase bench by 15lbs", "Deadline": "2025-09-01", "Week": "Week 2", "Progress (%)": 30},
        {"Goal": "Decrease mile time", "Deadline": "2025-10-15", "Week": "Week 1", "Progress (%)": 20},
        {"Goal": "Decrease mile time", "Deadline": "2025-10-15", "Week": "Week 2", "Progress (%)": 40},
    ])

# Editable table for all fields except Progress
edited_df = st.data_editor(
    st.session_state['goal_progress'],
    column_config={
        "Goal": {"editable": True},
        "Deadline": {"editable": True},
        "Week": {"editable": True},
        "Progress (%)": {"editable": True}
    },
    num_rows="dynamic"
)

# Update session state with edits
if st.button("Update Goals & Progress"):
    st.session_state['goal_progress'] = edited_df
    st.success("Goals and progress updated!")

# Show the updated table
st.subheader("Your Goals and Weekly Progress")
st.dataframe(st.session_state['goal_progress'], use_container_width=True)

# Show the progress chart
progress_df = pd.DataFrame(st.session_state['progress_data'])
st.subheader("Your Progress Over Time")
st.line_chart(progress_df.set_index("Week"))


