import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import BASE_URL, set_base_url, get, post, put, delete

st.set_page_config(layout='wide')
SideBarLinks()

st.title('User Devices')

st.write('Admin view for User Devices; list, inspect, and remove devices as needed.')

# --- API configuration in sidebar
st.sidebar.subheader('API')
api_url = st.sidebar.text_input('Base URL', value=BASE_URL)
if api_url:
    set_base_url(api_url)


# Placeholder for table so we can update it in-place without rerunning
table_placeholder = st.empty()

# --- Fetch devices
def fetch_devices():
    devices = []
    try:
        devices = get('/user_devices').json()
    except Exception as e:
        st.warning(f'Could not fetch user devices: {e}')
    return devices

devices = fetch_devices()
table_placeholder.dataframe(devices, use_container_width=True)

st.divider()

# --- Create / Update Device
st.subheader('Create / Update Device')
with st.form('device_form', clear_on_submit=False):
    device_ID = st.text_input('device_ID (leave empty to create)', key='device_id')
    user_ID = st.text_input('user_ID', key='device_user')
    device_type = st.text_input('device_type', key='device_type')
    os_info = st.text_input('os', key='device_os')
    last_seen = st.text_input('last_seen', key='device_lastseen')
    submitted = st.form_submit_button('Save', use_container_width=True)

    if submitted:
        payload = {
            'user_ID': user_ID,
            'device_type': device_type,
            'os': os_info,
            'last_seen': last_seen,
        }
        try:
            if device_ID and device_ID.strip():
                put(f'/user_devices/{device_ID}', json=payload)
            else:
                post('/user_devices', json=payload)
            st.success('Saved ✅')
            # Refresh the table in-place
            devices = fetch_devices()
            table_placeholder.dataframe(devices, use_container_width=True)
        except Exception as e:
            st.error(f'Save failed: {e}')

st.divider()

# --- Delete Device
st.subheader('Delete Device')
del_id = st.text_input('device_ID to delete', key='del_device_id')
if st.button('Delete Device', type='primary', use_container_width=True, disabled=not del_id or not del_id.strip(), key='delete_device_btn'):
    try:
        delete(f'/user_devices/{del_id}')
        st.success('Deleted ✅')
        devices = fetch_devices()
        table_placeholder.dataframe(devices, use_container_width=True)
    except Exception as e:
        st.error(f'Delete failed: {e}')
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('User Devices')

st.write('Admin view for User Devices; list, inspect, and remove devices as needed.')

if st.button('Refresh'):
    st.experimental_rerun()
systems = []
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import BASE_URL, set_base_url, get, post, put, delete


st.set_page_config(layout='wide')
SideBarLinks()

st.title("Systems")

# Allow changing API URL from sidebar
st.sidebar.subheader("API")
api_url = st.sidebar.text_input("Base URL", value=BASE_URL)
if api_url:
    set_base_url(api_url)


# --- List Systems
st.subheader("All Systems")
systems = []
try:
    systems = get("/systems").json()
except Exception as e:
    st.warning(f"Could not fetch systems: {e}")
st.dataframe(systems, use_container_width=True)

st.divider()


# --- Create / Update System
st.subheader("Create / Update System")
with st.form("system_form"):
    system_ID = st.text_input("system_ID (leave empty to create)")
    logs = st.text_area("logs")
    updates = st.text_input("updates")
    alerts = st.text_input("alerts")
    accounts = st.text_area("accounts (optional)")
    submitted = st.form_submit_button("Save")

    if submitted:
        payload = {"logs": logs, "updates": updates, "alerts": alerts, "accounts": accounts}
        try:
            if system_ID and system_ID.strip():
                resp = put(f"/systems/{system_ID}", json=payload)
            else:
                resp = post("/systems", json=payload)
            st.success("Saved ✅")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

st.divider()


# --- Delete System
st.subheader("Delete System")
del_id = st.text_input("system_ID to delete")
if st.button("Delete System", type="primary", use_container_width=True, disabled=not del_id or not del_id.strip()):
    try:
        delete(f"/systems/{del_id}")
        st.success("Deleted ✅")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Delete failed: {e}")
systems = []
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import BASE_URL, set_base_url, get, post, put, delete


st.set_page_config(layout='wide')
SideBarLinks()

st.title("Systems")

# Allow changing API URL from sidebar
st.sidebar.subheader("API")
api_url = st.sidebar.text_input("Base URL", value=BASE_URL)
if api_url:
	set_base_url(api_url)


# --- List Systems
st.subheader("All Systems")
systems = []
try:
	systems = get("/systems").json()
except Exception as e:
	st.warning(f"Could not fetch systems: {e}")
st.dataframe(systems, use_container_width=True)

st.divider()


# --- Create / Update System
st.subheader("Create / Update System")
with st.form("system_form"):
	system_ID = st.text_input("system_ID (leave empty to create)")
	logs = st.text_area("logs")
	updates = st.text_input("updates")
	alerts = st.text_input("alerts")
	accounts = st.text_area("accounts (optional)")  # seen in ERD
	submitted = st.form_submit_button("Save")

	if submitted:
		payload = {"logs": logs, "updates": updates, "alerts": alerts, "accounts": accounts}
		try:
			if system_ID and system_ID.strip():
				resp = put(f"/systems/{system_ID}", json=payload)
			else:
				resp = post("/systems", json=payload)
			st.success("Saved ✅")
			st.experimental_rerun()
		except Exception as e:
			st.error(f"Save failed: {e}")

st.divider()


# --- Delete System
st.subheader("Delete System")
del_id = st.text_input("system_ID to delete")
if st.button("Delete System", type="primary", use_container_width=True, disabled=not del_id or not del_id.strip()):
	try:
		delete(f"/systems/{del_id}")
		st.success("Deleted ✅")
		st.experimental_rerun()
	except Exception as e:
		st.error(f"Delete failed: {e}")