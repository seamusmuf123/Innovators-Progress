import logging
from __future__ import annotations


logger = logging.getLogger(__name__)

import streamlit as st
import json
from pathlib import Path
from typing import Dict, list
from modules.nav import SideBarLinks
import requests

# Set the page configuration/setup for the Workout Plan page
st.set_page_config(page_title="Create Workout Plan (Jordan – Analyst)", page_icon="🏋️", layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Prediction with Regression")

# ---- LEFT: Plan Builder ----
with left:
    st.subheader("Plan Details")
    with st.form("plan_form", clear_on_submit=False, border=True):
        plan_title = st.text_input("Plan Title", value="Jordan's Starter Plan")
        goal = st.selectbox("Primary Goal", options=GOALS, index=0)
        difficulty = st.selectbox("Difficulty", options=DIFFICULTY, index=0)
        split = st.selectbox("Training Split", options=SPLITS, index=0)
        weeks = st.number_input("Duration (weeks)", min_value=1, max_value=12, value=4, step=1)
        days_per_week = st.slider("Days / Week", min_value=2, max_value=6, value=3)
        notes = st.text_area("Notes (optional)", placeholder="Constraints, equipment, schedule limits, etc.")

        submit = st.form_submit_button("Generate Schedule", use_container_width=True, type="primary")

    def generate_schedule(split: str, days: int) -> Dict[str, List[str]]:
        # Keep this intentionally simple and readable
        schedule: Dict[str, List[str]] = {}
        if split.startswith("Full Body"):
            day_block = EXERCISE_LIBRARY["Full Body"]
            template = [day_block, day_block, day_block]
        elif split.startswith("Upper"):
            template = [EXERCISE_LIBRARY["Upper"], EXERCISE_LIBRARY["Lower"], EXERCISE_LIBRARY["Upper"], EXERCISE_LIBRARY["Lower"]]
        else:  # PPL
            template = [EXERCISE_LIBRARY["Push"], EXERCISE_LIBRARY["Pull"], EXERCISE_LIBRARY["Legs"],
                        EXERCISE_LIBRARY["Push"], EXERCISE_LIBRARY["Pull"], EXERCISE_LIBRARY["Legs"]]
        # Trim / extend to match days requested
        template = template[:days]
        for i, exs in enumerate(template, start=1):
            schedule[f"Day {i}"] = exs
        return schedule

    if submit:
        schedule = generate_schedule(split, days_per_week)
        plan = {
            "persona": "Jordan",
            "role": st.session_state.get("role", "Analyst"),
            "title": plan_title,
            "goal": goal,
            "difficulty": difficulty,
            "split": split,
            "weeks": int(weeks),
            "days_per_week": int(days_per_week),
            "notes": notes,
            "schedule": schedule,
        }
        st.success("Plan generated.")

        st.subheader("Preview")
        st.json(plan)

        # Download JSON
        st.download_button(
            label="Download Plan JSON",
            file_name=f"{plan_title.replace(' ', '_').lower()}_plan.json",
            mime="application/json",
            data=json.dumps(plan, indent=2),
            use_container_width=True,
        )

        with st.expander("Optional: Save to API (POST)", expanded=False):
            api_url = st.text_input("POST endpoint (e.g., http://web-api:4000/plans)", value="")
            if st.button("Send Plan to API", use_container_width=True, disabled=not api_url):
                import requests
                try:
                    resp = requests.post(api_url, json=plan, timeout=10)
                    st.write(f"Status: {resp.status_code}")
                    try:
                        st.json(resp.json())
                    except Exception:
                        st.write(resp.text)
                except Exception as e:
                    st.error(f"Failed to POST: {e}")
