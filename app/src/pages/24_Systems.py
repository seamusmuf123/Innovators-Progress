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
# placeholder for table so we can refresh in-place
systems_placeholder = st.empty()
def fetch_systems():
	try:
		return get('/systems').json()
	except Exception as e:
		st.warning(f'Could not fetch systems: {e}')
		return []

systems = fetch_systems()
systems_placeholder.dataframe(systems, use_container_width=True)

st.divider()


# --- Create / Update System
st.subheader("Create / Update System")
with st.form("system_form"):
	system_ID = st.text_input("system_ID (leave empty to create)", key='system_id')
	logs = st.text_area("logs", key='system_logs')
	updates = st.text_input("updates", key='system_updates')
	alerts = st.text_input("alerts", key='system_alerts')
	accounts = st.text_area("accounts (optional)", key='system_accounts')  # seen in ERD
	submitted = st.form_submit_button("Save")

	if submitted:
		payload = {"logs": logs, "updates": updates, "alerts": alerts, "accounts": accounts}
		try:
			if system_ID and system_ID.strip():
				resp = put(f"/systems/{system_ID}", json=payload)
			else:
				resp = post("/systems", json=payload)
			st.success("Saved ✅")
			# refresh in-place
			systems = fetch_systems()
			systems_placeholder.dataframe(systems, use_container_width=True)
		except Exception as e:
			st.error(f"Save failed: {e}")

st.divider()


# --- Delete System
st.subheader("Delete System")
del_id = st.text_input("system_ID to delete", key='del_system_id')
if st.button("Delete System", type="primary", use_container_width=True, disabled=not del_id or not del_id.strip(), key='delete_system_btn'):
	try:
		delete(f"/systems/{del_id}")
		st.success("Deleted ✅")
		systems = fetch_systems()
		systems_placeholder.dataframe(systems, use_container_width=True)
	except Exception as e:
		st.error(f"Delete failed: {e}")