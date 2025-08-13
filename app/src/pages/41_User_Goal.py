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

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('User Goal')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# You can access the session state to make a more customized/personalized app experience
st.write('Your Goal:')


# get the goal the user has set for themselves
data = {
    "Goal": ["Increase weight for bench by 15lbs", "Decrease time for running a mile", "Do 10 pull-ups nonstop"],
    "Progress": ["50%", "20%", "80%"],
    "Deadline": ["2025-09-01", "2025-10-15", "2025-08-20"]
}

df = pd.DataFrame(data)

st.dataframe(df)  

# To edit table
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

#To update the session state with the edited data
if st.button("Update Goal"):
    st.session_state['goal'] = edited_df.to_dict(orient='records')
    st.success("Goal updated successfully!")

