import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Create a Workout Plan', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Workout_Plan.py')

if st.button('Create a Report', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Report.py')

if st.button("Check User Device",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Classification.py')
  