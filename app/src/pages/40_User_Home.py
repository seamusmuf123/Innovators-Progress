import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Ensure session state keys exist
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = ''

st.title(f"Welcome {st.session_state.get('first_name') or 'User'}")
st.write('')

st.write('### Please sign in or enter your details')

with st.form(key='login_form'):
    first_name = st.text_input('First name', value=st.session_state.get('first_name', ''))
    last_name = st.text_input('Last name', value=st.session_state.get('last_name', ''))
    email = st.text_input('Email', value=st.session_state.get('email', ''))
    password = st.text_input('Password', type='password')
    address = st.text_input('Address', value=st.session_state.get('address', ''))
    # Gym choices come from sample data in database-files/my.sql
    gym_options = ['Downtown Gym', 'Westside Gym', 'Eastside Gym']
    current = st.session_state.get('gym_location', '')
    try:
        default_index = gym_options.index(current) if current in gym_options else 0
    except Exception:
        default_index = 0
    gym_location = st.selectbox('Gym location', options=gym_options, index=default_index)
    submit = st.form_submit_button('Save / Login')
    if submit:
        # Persist small set of attributes in session state for the demo
        st.session_state['first_name'] = first_name or st.session_state.get('first_name', '')
        st.session_state['last_name'] = last_name
        st.session_state['email'] = email
        # NOTE: password handling here is minimal for demo purposes only
        st.session_state['password'] = password
        st.session_state['address'] = address
        st.session_state['gym_location'] = gym_location
        st.success('Saved. You are now signed in.')

st.write('')
st.write('### What would you like to do today?')

if st.button('Goal', type='primary', use_container_width=True):
    # keep existing navigation target
    st.switch_page('pages/41_User_Goal.py')