import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import get, post, put, delete
 
SideBarLinks()
 
st.header('User Goal')
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")
st.info("Stay consistent! Remember to log your workouts this week.")
 
current_user = st.session_state.get('user_ID', 1)
 
# Fetch goals from DB
def fetch_goals():
    try:
        resp = get('/goals')
        all_goals = resp.json()
        # filter to this user only
        return [g for g in all_goals if g.get('user_ID') == current_user]
    except Exception as e:
        st.warning(f"Could not load goals from database: {e}")
        return []
 
goals = fetch_goals()
goals_df = pd.DataFrame(goals) if goals else pd.DataFrame(
    columns=['user_ID', 'goal_name', 'task', 'tracking', 'records', 'reminders']
)
 
# Display goals table
st.subheader("Your Goals")
goals_placeholder = st.empty()
goals_placeholder.dataframe(goals_df, use_container_width=True)
 
st.divider()
 
# Create Goal
st.subheader("Create New Goal")
with st.form('create_goal_form'):
    st.write(f"Creating goal for User ID: {current_user}")
    c_goal_name  = st.text_input('Goal name')
    c_task       = st.text_input('Task (short description)')
    c_tracking   = st.selectbox('Tracking frequency',
                                ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Other'])
    c_records    = st.text_area('Records (how you track progress)')
    c_reminders  = st.text_input('Reminders (email / sms / app)')
    create       = st.form_submit_button('Create Goal')
 
    if create:
        if not c_goal_name:
            st.error('Goal name is required')
        else:
            try:
                post('/goals', json={
                    'user_ID':   current_user,
                    'goal_name': c_goal_name,
                    'task':      c_task,
                    'tracking':  c_tracking,
                    'records':   c_records,
                    'reminders': c_reminders,
                })
                st.success(f'Created goal "{c_goal_name}"')
                goals = fetch_goals()
                goals_df = pd.DataFrame(goals) if goals else goals_df
                goals_placeholder.dataframe(goals_df, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to create goal: {e}")
 
st.divider()
 
# Edit / Delete Goal 
st.subheader("Edit or Delete an Existing Goal")
if not goals:
    st.info("No goals yet — create one above.")
else:
    key_list    = [g['goal_name'] for g in goals]
    sel_name    = st.selectbox('Select goal to edit / delete', key_list, key='sel_goal')
    sel_goal    = next((g for g in goals if g['goal_name'] == sel_name), None)
 
    if sel_goal:
        tracking_opts = ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Other']
        default_track = sel_goal.get('tracking', 'Daily')
        track_index   = tracking_opts.index(default_track) if default_track in tracking_opts else 0
 
        with st.form('edit_goal_form'):
            e_goal_name = st.text_input('Goal name',  value=sel_goal.get('goal_name', ''))
            e_task      = st.text_input('Task',       value=sel_goal.get('task', ''))
            e_tracking  = st.selectbox('Tracking frequency', tracking_opts, index=track_index)
            e_records   = st.text_area('Records',     value=sel_goal.get('records', ''))
            e_reminders = st.text_input('Reminders',  value=sel_goal.get('reminders', ''))
 
            col1, col2  = st.columns(2)
            with col1:
                update = st.form_submit_button('Update Goal')
            with col2:
                delete_btn = st.form_submit_button('Delete Goal', type='primary')
 
            if update:
                try:
                    # If name changed, delete old and create new
                    if e_goal_name != sel_goal['goal_name']:
                        delete(f"/goals/{current_user}/{sel_goal['goal_name']}")
                        post('/goals', json={
                            'user_ID':   current_user,
                            'goal_name': e_goal_name,
                            'task':      e_task,
                            'tracking':  e_tracking,
                            'records':   e_records,
                            'reminders': e_reminders,
                        })
                    else:
                        put(f"/goals/{current_user}/{sel_goal['goal_name']}", json={
                        'task':      e_task,
                        'tracking':  e_tracking,
                        'records':   e_records,
                        'reminders': e_reminders,
                    })
                    st.success('Goal updated')
                    goals = fetch_goals()
                    goals_df = pd.DataFrame(goals) if goals else goals_df
                    goals_placeholder.dataframe(goals_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Update failed: {e}")
 
            if delete_btn:
                try:
                    delete(f"/goals/{current_user}/{sel_name}")
                    st.success(f'Deleted goal: {sel_name}')
                    goals = fetch_goals()
                    goals_df = pd.DataFrame(goals) if goals else goals_df
                    goals_placeholder.dataframe(goals_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Delete failed: {e}")
 
st.divider()
 
# Chart: goals by tracking frequency
st.subheader('Goals by Tracking Frequency')
if not goals_df.empty and 'tracking' in goals_df.columns:
    counts = goals_df['tracking'].value_counts().reset_index()
    counts.columns = ['tracking', 'count']
    st.bar_chart(data=counts.set_index('tracking'))
 
    grouped = goals_df.groupby('tracking')['goal_name'].apply(list).reset_index()
    for _, row in grouped.iterrows():
        st.write(f"**{row['tracking']}**: {', '.join(row['goal_name'])}")
else:
    st.write('No goals to chart yet.')