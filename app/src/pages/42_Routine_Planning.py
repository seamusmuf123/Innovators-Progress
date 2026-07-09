import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import get, post, put, delete

SideBarLinks()

st.title("Routine Planning")
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")
st.write("Build a routine that aligns with your fitness goals.")

# Fetch plans from DB
def fetch_plans():
    try:
        resp = get('/plans')
        data = resp.json()
        if isinstance(data, dict) and 'error' in data:
            st.warning(f"API error: {data['error']}")
            return []
        return data
    except Exception as e:
        st.warning(f"Could not load plans: {e}")
        return []

plans = fetch_plans()
plans_placeholder = st.empty()

# Display plans as cards
st.subheader("Available Plans")
if plans:
    for p in plans:
        with st.expander(f"📋 {p.get('title', 'Untitled Plan')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Workout:** {p.get('workout_rec', 'N/A')}")
            with col2:
                st.write(f"**Diet:** {p.get('diet', 'N/A')}")
else:
    st.info("No plans found. Create one below!")

st.divider()

# Create Plan
st.subheader("Create New Plan")
with st.form("create_plan_form"):
    c_title      = st.text_input("Plan title (e.g. Weight Loss Plan)", key="plan_title")
    c_workout    = st.text_area("Workout recommendation", key="plan_workout",
                                placeholder="e.g. 30 min cardio + weights 3x/week")
    c_diet       = st.text_input("Diet recommendation", key="plan_diet",
                                 placeholder="e.g. Low carb, high protein")
    create       = st.form_submit_button("Save Plan")

    if create:
        if not c_title:
            st.error("Plan title is required")
        else:
            try:
                post('/plans', json={
                    'title':       c_title,
                    'workout_rec': c_workout,
                    'diet':        c_diet,
                })
                st.success(f'Created plan "{c_title}"')
                plans = fetch_plans()
                st.rerun()
            except Exception as e:
                st.error(f"Failed to create plan: {e}")

st.divider()

# Edit / Delete Plan
st.subheader("Edit or Delete a Plan")
if not plans:
    st.info("No plans available yet.")
else:
    plan_titles = [p['title'] for p in plans]
    sel_title   = st.selectbox("Select plan to edit / delete", plan_titles, key="sel_plan")
    sel_plan    = next((p for p in plans if p['title'] == sel_title), None)

    if sel_plan:
        with st.form("edit_plan_form"):
            e_title   = st.text_input("Plan title",              value=sel_plan.get('title', ''))
            e_workout = st.text_area("Workout recommendation",   value=sel_plan.get('workout_rec', ''))
            e_diet    = st.text_input("Diet recommendation",     value=sel_plan.get('diet', ''))

            col1, col2 = st.columns(2)
            with col1:
                update     = st.form_submit_button("Update Plan")
            with col2:
                delete_btn = st.form_submit_button("Delete Plan", type="primary")

            if update:
                try:
                    put(f"/plans/{sel_plan['plan_ID']}", json={
                        'title':       e_title,
                        'workout_rec': e_workout,
                        'diet':        e_diet,
                    })
                    st.success("Plan updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update failed: {e}")

            if delete_btn:
                try:
                    delete(f"/plans/{sel_plan['plan_ID']}")
                    st.success(f'Deleted plan: {sel_title}')
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")