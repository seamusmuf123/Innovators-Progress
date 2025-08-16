import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')
cols = st.columns(2)

with cols[0]:
    if st.button('Update ML Models', type='primary', use_container_width=True):
        st.switch_page('pages/21_ML_Model_Mgmt.py')

    if st.button('Manage Analyst Team', type='secondary', use_container_width=True):
        st.switch_page('pages/22_Analyst_Team.py')

    if st.button('View Reports', type='secondary', use_container_width=True):
        st.switch_page('pages/23_Reports.py')

with cols[1]:
    if st.button('Manage Systems', type='secondary', use_container_width=True):
        st.switch_page('pages/24_Systems.py')

    if st.button('User Devices', type='secondary', use_container_width=True):
        st.switch_page('pages/25_User_Devices.py')