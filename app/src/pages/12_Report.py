from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, List

import streamlit as st

try:
    from modules.nav import SideBarLinks
    SideBarLinks()
except Exception:
    pass

st.set_page_config(page_title="Reports (Jordan – Analyst)", page_icon="📊", layout="wide")

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
