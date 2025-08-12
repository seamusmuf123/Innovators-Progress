from __future__ import annotations
import logging



logger = logging.getLogger(__name__)

import streamlit as st
import json
from pathlib import Path
from typing import Dict, List
from modules.nav import SideBarLinks
import requests

# Set the page configuration/setup for the Workout Plan page
st.set_page_config(page_title="Create Workout Plan (Jordan – Analyst)", page_icon="🏋️", layout="wide")
if SideBarLinks:
    try:
        SideBarLinks()  # shows role-based links if your nav module sets them based on session_state
    except Exception:
        pass

# Ensure a role exists in session state; default this page to "Analyst" for Jordan
st.session_state.setdefault("role", "Analyst")


# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

#Setup Layout
st.title("Create a Workout Plan")
st.caption("Persona: Jordan — Role: Analyst")

left, right = st.columns([3, 2], gap="large")

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
    # ---- RIGHT: Diagram Viewer ----
    with right:
        st.subheader("Related System Diagram")

        DEFAULT_PATH = Path("/mnt/data/Screenshot 2025-08-12 at 19.22.47.png")
        uploaded = st.file_uploader("Upload a diagram (PNG/JPG)", type=["png", "jpg", "jpeg"])

        # Prefer uploaded file; else try default path; else show placeholder
        if uploaded is not None:
            st.image(uploaded, caption="Uploaded diagram", use_container_width=True)
        elif DEFAULT_PATH.exists():
            st.image(str(DEFAULT_PATH), caption="User Persona 3: Jordan, Analyst — Diagram", use_container_width=True)
        else:
            st.info("No diagram found. Upload an image to display it here.")

        st.caption(
            "Tip: Keep this view open while editing the plan so you can align plan fields with entities like Plan, Report, and User Device from the diagram."
        )