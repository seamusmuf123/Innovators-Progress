from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, List

import streamlit as st

#RBAC implementation
try:
    from modules.nav import SideBarLinks
    SideBarLinks()
except Exception:
    pass

st.set_page_config(page_title="Reports (Jordan – Analyst)", page_icon="📊", layout="wide")

# Configuration for API endpoints
API_BASE = st.secrets.get("API_BASE", "http://web-api:4000")  # override with .streamlit/secrets.toml if desired
REPORTS_ENDPOINT = f"{API_BASE}/reports"
DEVICES_ENDPOINT = f"{API_BASE}/devices"


# Helper functions for API calls
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
    

# Title and description
st.title("Reports")
st.caption("Persona: Jordan — Role: Analyst")

left, right = st.columns([3, 2], gap="large")

SideBarLinks()

st.write("# Accessing a REST API from Within Streamlit")
"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""

data = {} 
try:
  data = requests.get('http://web-api:4000/data').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)
