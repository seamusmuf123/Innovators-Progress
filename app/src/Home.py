##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('💪 Progress Fitness App')
st.markdown('<h2 style="text-align: center; color: #666;">Data-Driven Personal Fitness App</h2>', unsafe_allow_html=True)
st.write('\n\n')

# Add Today's Routine and Quick Start sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏋️ **Today's Routine**")
    st.markdown("""
    **Morning Workout (30 min)**
    - 10 min warm-up cardio
    - 15 min strength training
    - 5 min cool-down stretch
    
    **Afternoon Activity**
    - 20 min walking or light cardio
    - Focus on consistency over intensity
    """)
    
    # Quick action buttons for routine
    if st.button("✅ Mark Complete", key="morning_routine"):
        st.success("Great job! Morning routine completed!")
    
    if st.button("📝 Log Workout", key="log_workout"):
        st.info("Workout logging feature coming soon!")

with col2:
    st.markdown("### 🚀 **Quick Start**")
    st.markdown("""
    **1. Choose Your Goal**
    - Weight Loss
    - Muscle Building
    - General Fitness
    - Endurance
    
    **2. Pick Your Level**
    - Beginner
    - Intermediate
    - Advanced
    
    **3. Start Your Journey**
    - Set realistic targets
    - Track your progress
    - Stay consistent
    """)
    
    # Quick start action
    if st.button("🎯 Set Goal", key="set_goal"):
        st.info("Goal setting feature coming soon!")

st.markdown("---")
st.markdown("### 🎯 **Our Mission**")
st.markdown("Progress empowers individuals to stay consistent, motivated, and goal-oriented in their fitness journey. Track workouts, monitor progress, and achieve your fitness goals with data-driven insights.")

st.markdown("---")
st.write('#### 🏋️ Choose Your Fitness Role:')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("🏋️ Act as Alex - Gym Desk Attendant", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'desk attendant'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Alex'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Gym Desk Attendant")
    st.switch_page('pages/20_Admin_Home.py')

if st.button('📊 Act as Jordan - Fitness Analyst', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['first_name'] = 'Jordan'
    st.switch_page('pages/10_Analyst_Home.py')

if st.button('⚙️ Act as Naomi - System Administrator', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Naomi'
    st.switch_page('pages/20_Admin_Home.py')

if st.button('👩‍💼 Act as Maya - Fitness User', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'user'
    st.session_state['first_name'] = 'Maya'
    st.switch_page('pages/40_User_Home.py')



