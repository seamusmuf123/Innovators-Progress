# app/src/pages/11_Report.py
"""
Report page based on the Jordan (Analyst) diagram.
- Lets Jordan create a simple Report (title, checklist, summaries, goals, efficiency)
- Optionally links a Report to User Device IDs
- Shows existing reports (from API if available, else dummy)
- Safe defaults + friendly failure if API is down

Adjust the API_BASE default if your Flask service uses a different route.
"""
from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, List

import streamlit as st

# RBAC nav
try:
    from modules.nav import SideBarLinks
    SideBarLinks()
except Exception:
    pass

st.set_page_config(page_title="Reports (Jordan – Analyst)", page_icon="📊", layout="wide")

# Configuration for API endpoints
API_BASE = "http://web-api:4000"  # hardcoded per request
REPORTS_ENDPOINT = f"{API_BASE}/reports"
DEVICES_ENDPOINT = f"{API_BASE}/devices"

# Helper funcs 
def safe_get_json(url: str, default: Any) -> Any:
    import requests
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception:
        return default


def safe_post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    import requests
    try:
        r = requests.post(url, json=payload, timeout=10)
        return {"status": r.status_code, "ok": r.ok, "data": try_json(r)}
    except Exception as e:
        return {"status": 0, "ok": False, "error": str(e)}


def try_json(resp) -> Any:
    try:
        return resp.json()
    except Exception:
        return resp.text

# ------------------------- Title --------------------------
st.title("Reports")
st.caption("Persona: Jordan — Role: Analyst")

# Load devices (for the multiselect); fall back to a few dummy IDs
device_data = safe_get_json(DEVICES_ENDPOINT, default=[{"device_id": "dev-001"}, {"device_id": "dev-002"}])
device_options = [d.get("device_id") or d.get("id") or str(d) for d in device_data]

# --------------------- Create/Edit Form -------------------
st.subheader("Create a Report")

with st.form("report_form", border=True):
    analyst_id = st.text_input("Analyst ID", value=st.session_state.get("analyst_id", "analyst-001"))
    report_title = st.text_input("Title", value="Weekly Progress Summary")
    report_date = st.date_input("Date", value=date.today())

    checklist = st.multiselect(
        "Checklist",
        options=[
            "Review device data",
            "Verify completed goals",
            "Identify uncompleted goals",
            "Compute work efficiency",
            "Draft recommendations",
        ],
        default=["Review device data", "Verify completed goals"],
    )

    col_a, col_b = st.columns(2)
    with col_a:
        completed_goals = st.number_input("Completed goals", min_value=0, value=4)
    with col_b:
        uncompleted_goal = st.number_input("Uncompleted goals", min_value=0, value=1)

    work_efficiency = st.slider("Work efficiency (%)", min_value=0, max_value=100, value=78, step=1)

    time_summary = st.text_area(
        "Time-based summary",
        placeholder="e.g., Mon-Wed: cardio & mobility; Thu-Fri: strength focus; weekend: recovery.",
    )

    devices = st.multiselect("Linked User Devices", options=device_options, default=device_options[:1])

    extra_notes = st.text_area("Notes (optional)")

    submitted = st.form_submit_button("Save Report", use_container_width=True, type="primary")

if submitted:
    report_payload: Dict[str, Any] = {
        "analyst_id": analyst_id,
        "title": report_title,
        "date": str(report_date),
        "checklist": checklist,
        "completed_goals": int(completed_goals),
        "uncompleted_goal": int(uncompleted_goal),
        "work_efficiency": int(work_efficiency),
        "time_based_summary": time_summary,
        "device_ids": devices,
        "notes": extra_notes,
    }

    st.write("**Preview**")
    st.json(report_payload)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download JSON",
            data=json.dumps(report_payload, indent=2),
            file_name="report.json",
            mime="application/json",
            use_container_width=True,
        )
    with col2:
        resp = safe_post_json(REPORTS_ENDPOINT, payload=report_payload)
        if resp.get("ok"):
            st.success(f"Saved to API (status {resp['status']}).")
        else:
            st.info(
                "Could not reach the API, so nothing was saved remotely. You can still download the JSON above."
            )
            if resp.get("error"):
                st.caption(f"Error: {resp['error']}")

# -------------------- Existing Reports --------------------
st.divider()
st.subheader("Existing Reports")
existing = safe_get_json(REPORTS_ENDPOINT, default=[
    {
        "report_id": "rep-001",
        "analyst_id": "analyst-001",
        "title": "Weekly Progress Summary",
        "date": str(date.today()),
        "completed_goals": 4,
        "uncompleted_goal": 1,
        "work_efficiency": 78,
    }
])

# Render table compactly
try:
    import pandas as pd
    if isinstance(existing, list):
        st.dataframe(pd.DataFrame(existing), use_container_width=True, hide_index=True)
    elif isinstance(existing, dict) and "items" in existing:
        st.dataframe(pd.DataFrame(existing["items"]), use_container_width=True, hide_index=True)
    else:
        st.json(existing)
except Exception:
    st.json(existing)
