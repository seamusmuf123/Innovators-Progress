# app/src/pages/13_User_Devices.py
"""
User Devices — Persona: Jordan (Analyst)

Purpose:
- View, filter, and register user devices that feed data into reports/plans
- Minimal UI with graceful fallbacks if API is unavailable

Assumptions:
- API endpoints:
    GET  /devices               -> list of devices
    POST /devices               -> create/register a device
  Example device fields (aligned with your diagram):
    device_id, user_id, device_type, model, platform, last_sync, status, notes
"""
from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any, Dict, List

import streamlit as st

# Optional RBAC nav
try:
    from modules.nav import SideBarLinks
    SideBarLinks()
except Exception:
    pass

st.set_page_config(page_title="User Devices (Jordan – Analyst)", page_icon="📱", layout="wide")

#  Config 
API_BASE = "http://web-api:4000"  # hardcoded per your preference
DEVICES_ENDPOINT = f"{API_BASE}/devices"

#  Helper 
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

st.title("User Devices")
st.caption("Persona: Jordan — Role: Analyst")

#  Filters  
with st.container():
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.2])
    with c1:
        f_user = st.text_input("Filter by User ID", value="")
    with c2:
        f_type = st.selectbox("Device Type", options=["(any)", "watch", "phone", "band", "scale", "other"], index=0)
    with c3:
        f_status = st.selectbox("Status", options=["(any)", "active", "inactive", "error"], index=0)
    with c4:
        f_query = st.text_input("Search (model/platform)", value="")

# Fetch data 
_dummy_devices: List[Dict[str, Any]] = [
    {
        "device_id": "dev-001",
        "user_id": "user-001",
        "device_type": "watch",
        "model": "FitPro X",
        "platform": "FitOS",
        "last_sync": str(date.today()),
        "status": "active",
        "notes": "Primary tracker",
    },
    {
        "device_id": "dev-002",
        "user_id": "user-002",
        "device_type": "phone",
        "model": "iPhone 14",
        "platform": "iOS",
        "last_sync": str(date.today()),
        "status": "inactive",
        "notes": "App not opened this week",
    },
]

raw = safe_get_json(DEVICES_ENDPOINT, default=_dummy_devices)

# Normalize list shape
if isinstance(raw, dict) and "items" in raw:
    devices: List[Dict[str, Any]] = list(raw["items"])  # type: ignore
elif isinstance(raw, list):
    devices = raw  # type: ignore
else:
    devices = _dummy_devices

#  Filter data 
filtered: List[Dict[str, Any]] = []
for d in devices:
    if f_user and str(d.get("user_id", "")).strip() != f_user.strip():
        continue
    if f_type != "(any)" and str(d.get("device_type", "")).lower() != f_type:
        continue
    if f_status != "(any)" and str(d.get("status", "")).lower() != f_status:
        continue
    hay = (str(d.get("model", "")) + " " + str(d.get("platform", ""))).lower()
    if f_query and f_query.lower() not in hay:
        continue
    filtered.append(d)

#  Table 
st.subheader("Devices")
if not filtered:
    st.info("No devices match your filters yet.")
else:
    try:
        import pandas as pd
        df = pd.DataFrame(filtered)
        preferred = ["device_id", "user_id", "device_type", "model", "platform", "last_sync", "status", "notes"]
        cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
        df = df[cols]
        st.dataframe(df, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name="devices.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "Download JSON",
                data=json.dumps(filtered, indent=2),
                file_name="devices.json",
                mime="application/json",
                use_container_width=True,
            )
    except Exception:
        st.json(filtered)

#  Register Device 
st.divider()
st.subheader("Register a New Device")
with st.form("register_device", border=True):
    user_id = st.text_input("User ID", value="user-001")
    device_id = st.text_input("Device ID", value="")
    device_type = st.selectbox("Device Type", options=["watch", "phone", "band", "scale", "other"], index=0)
    model = st.text_input("Model", value="")
    platform = st.text_input("Platform", value="")
    last_sync = st.date_input("Last Sync", value=date.today())
    status = st.selectbox("Status", options=["active", "inactive", "error"], index=0)
    notes = st.text_area("Notes (optional)")

    submit_dev = st.form_submit_button("Register Device", use_container_width=True, type="primary")

if submit_dev:
    payload = {
        "user_id": user_id,
        "device_id": device_id or None,
        "device_type": device_type,
        "model": model,
        "platform": platform,
        "last_sync": str(last_sync),
        "status": status,
        "notes": notes,
    }
    st.write("**Preview**")
    st.json(payload)

    resp = safe_post_json(DEVICES_ENDPOINT, payload)
    if resp.get("ok"):
        st.success(f"Registered (status {resp['status']}).")
    else:
        st.info("Could not reach the API, so nothing was saved remotely. You can still download the JSON below.")
        if resp.get("error"):
            st.caption(f"Error: {resp['error']}")

    st.download_button(
        "Download JSON",
        data=json.dumps(payload, indent=2),
        file_name="device.json",
        mime="application/json",
        use_container_width=True,
    )
