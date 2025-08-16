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

# 2. Weekly Reminder
st.info("Stay consistent! Remember to log your workouts this week.")


# 4. Unified Goal Setting & Progress Tracking Table
st.subheader("Set Your Goals and Track Progress")

# Initialize goals store in session_state (Goal fields: user_ID, goal_name, task, tracking, records, reminders)
if 'goals' not in st.session_state:
    # bind all sample goals to the logged-in user
    current_user = st.session_state.get('user_ID') or 1
    # persist the chosen current_user back to session (so create/edit uses same id)
    st.session_state['user_ID'] = current_user
    st.session_state['goals'] = [
        ({"user_ID": current_user, "goal_name": "Lose Weight", "task": "Cardio & Diet", "tracking": "Daily", "records": "Progress Weekly", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Build Muscle", "task": "Strength Training", "tracking": "Bi-weekly", "records": "Photos Monthly", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Improve Stamina", "task": "HIIT Routines", "tracking": "Weekly", "records": "Pulse Tracker", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Run 5k", "task": "Running", "tracking": "Daily", "records": "Time Tracker", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Swim 1 Mile", "task": "Swimming", "tracking": "Weekly", "records": "Lap Counter", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Cycle 100 Miles", "task": "Cycling", "tracking": "Monthly", "records": "Distance Log", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Bench Press 200lbs", "task": "Strength Training", "tracking": "Weekly", "records": "Weight Log", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Yoga Mastery", "task": "Yoga", "tracking": "Daily", "records": "Flexibility Chart", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "10 Pull-ups", "task": "Bodyweight", "tracking": "Weekly", "records": "Reps Log", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Squat 250lbs", "task": "Strength Training", "tracking": "Bi-weekly", "records": "Weight Log", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Deadlift 300lbs", "task": "Strength Training", "tracking": "Monthly", "records": "Weight Log", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Lose 10lbs", "task": "Cardio & Diet", "tracking": "Weekly", "records": "Progress Photos", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Gain 5lbs Muscle", "task": "Strength Training", "tracking": "Monthly", "records": "Body Scan", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Stretch Daily", "task": "Flexibility", "tracking": "Daily", "records": "Stretch Log", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Walk 10,000 Steps", "task": "Walking", "tracking": "Daily", "records": "Step Counter", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Climb 50 Flights", "task": "Stair Climbing", "tracking": "Weekly", "records": "Flight Log", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Row 2k", "task": "Rowing", "tracking": "Weekly", "records": "Time Tracker", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Jump Rope 500x", "task": "Jump Rope", "tracking": "Daily", "records": "Reps Log", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "50 Push-ups", "task": "Bodyweight", "tracking": "Weekly", "records": "Reps Log", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Plank 3 Minutes", "task": "Core", "tracking": "Daily", "records": "Time Tracker", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Track Calories", "task": "Nutrition", "tracking": "Daily", "records": "Calorie Log", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Sleep 8 Hours", "task": "Sleep", "tracking": "Daily", "records": "Sleep Tracker", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Drink 2L Water", "task": "Hydration", "tracking": "Daily", "records": "Water Log", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Meal Prep Weekly", "task": "Nutrition", "tracking": "Weekly", "records": "Meal Log", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Try New Sport", "task": "Recreation", "tracking": "Monthly", "records": "Activity Log", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Join Group Class", "task": "Group Fitness", "tracking": "Weekly", "records": "Attendance Log", "reminders": "SMS"}),
        ({"user_ID": current_user, "goal_name": "Log Workouts Daily", "task": "Tracking", "tracking": "Daily", "records": "Workout Log", "reminders": "Push Notification"}),
        ({"user_ID": current_user, "goal_name": "Increase Vertical Jump", "task": "Plyometrics", "tracking": "Weekly", "records": "Jump Log", "reminders": "App Alert"}),
        ({"user_ID": current_user, "goal_name": "Improve Balance", "task": "Balance Training", "tracking": "Daily", "records": "Balance Log", "reminders": "Email"}),
        ({"user_ID": current_user, "goal_name": "Reduce Resting HR", "task": "Cardio", "tracking": "Weekly", "records": "Heart Rate Log", "reminders": "SMS"}),
    ]
    with st.form('create_goal_form'):
        # use session user id (not editable)
        current_user = st.session_state.get('user_ID', 1)
        st.write(f"Creating goal for User ID: {current_user}")
        c_user_id = current_user
        c_goal_name = st.text_input('Goal name')
        c_task = st.text_input('Task (short)')
        c_tracking = st.selectbox('Tracking frequency', ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Other'])
        c_records = st.text_area('Records (how you track progress)')
        c_reminders = st.text_input('Reminders (email/sms/app)')
        create = st.form_submit_button('Create Goal')
        if create:
            if not c_goal_name:
                st.error('Goal name is required')
            else:
                st.session_state['goals'].append({
                    'user_ID': int(c_user_id),
                    'goal_name': c_goal_name,
                    'task': c_task,
                    'tracking': c_tracking,
                    'records': c_records,
                    'reminders': c_reminders,
                })
                st.success(f'Created goal "{c_goal_name}"')


    st.subheader('Your Goals (table)')
    goals_df = pd.DataFrame(st.session_state['goals'])
    # show only goals for the logged-in user
    current_user = st.session_state.get('user_ID', 1)
    user_goals_df = goals_df[goals_df['user_ID'] == current_user].reset_index(drop=True)
    st.dataframe(user_goals_df, use_container_width=True)


    st.subheader('Edit or Delete an Existing Goal')
    if not st.session_state['goals']:
        st.info('No goals available to edit or delete')
    else:
        # only allow editing the logged-in user's goals
        current_user = st.session_state.get('user_ID', 1)
        user_goals = [g for g in st.session_state['goals'] if g['user_ID'] == current_user]
        key_list = [f"{g['user_ID']} - {g['goal_name']}" for g in user_goals]
        sel = st.selectbox('Select goal', key_list)
        sel_goal_name = sel.split(' - ', 1)[1]
        # find the index in the global goals list
        sel_index = next(i for i,g in enumerate(st.session_state['goals']) if g['user_ID']==current_user and g['goal_name']==sel_goal_name)
        g = st.session_state['goals'][sel_index]

        with st.form('edit_goal_form'):
            e_user_id = st.number_input('User ID', min_value=1, value=g['user_ID'])
            e_goal_name = st.text_input('Goal name', value=g['goal_name'])
            e_task = st.text_input('Task (short)', value=g.get('task',''))
            e_tracking = st.selectbox('Tracking frequency', ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Other'], index=['Daily','Weekly','Bi-weekly','Monthly','Other'].index(g.get('tracking','Daily')))
            e_records = st.text_area('Records (how you track progress)', value=g.get('records',''))
            e_reminders = st.text_input('Reminders (email/sms/app)', value=g.get('reminders',''))
            update = st.form_submit_button('Update Goal')
            delete = st.form_submit_button('Delete Goal')

            if update:
                st.session_state['goals'][sel_index] = {
                    'user_ID': int(e_user_id),
                    'goal_name': e_goal_name,
                    'task': e_task,
                    'tracking': e_tracking,
                    'records': e_records,
                    'reminders': e_reminders,
                }
                st.success('Goal updated')

            if delete:
                removed = st.session_state['goals'].pop(sel_index)
                st.success(f"Deleted goal: {removed['goal_name']}")


    # Chart: distribution of goals by tracking frequency for the logged-in user
    st.subheader('Goals by Tracking Frequency')
    if not user_goals_df.empty:
        chart_df = user_goals_df.copy()
        counts = chart_df['tracking'].value_counts().reset_index()
        counts.columns = ['tracking', 'count']
        st.bar_chart(data=counts.set_index('tracking'))
        # also show which goals fall into each category
        grouped = chart_df.groupby('tracking')['goal_name'].apply(list).reset_index()
        st.write('Goals by category:')
        for _, row in grouped.iterrows():
            st.write(f"**{row['tracking']}**: {', '.join(row['goal_name'])}")
    else:
        st.write('No goals to chart')
