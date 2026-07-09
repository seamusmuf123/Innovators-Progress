import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import BASE_URL, set_base_url, get, post, put, delete

st.set_page_config(page_title="Analysts - Team", layout='wide')
SideBarLinks()

st.title("Analysts — Team")

st.sidebar.subheader("API")
api_url = st.sidebar.text_input("Base URL", value=BASE_URL)
if api_url:
	set_base_url(api_url)


# Fetch lookups (optional; if endpoints don't exist yet, page still works)
def _safe_get(path):
	try:
		return get(path).json()
	except Exception:
		return []


reports = _safe_get("/reports")
plans = _safe_get("/plans")  # if you have it
admins = _safe_get("/system-admins")  # for admin_ID
devices = _safe_get("/user-devices")


# --- List Analysts
st.subheader("All Analysts")
analysts = []
try:
	analysts = get("/analysts").json()
except Exception as e:
	st.warning(f"Could not fetch analysts: {e}")
st.dataframe(analysts, use_container_width=True)

st.divider()


# --- Create / Update Analyst
st.subheader("Create / Update Analyst")
with st.form("analyst_form"):
	analyst_ID = st.text_input("analyst_ID (leave empty to create)")
	name = st.text_input("name")
	email = st.text_input("email")

	# Use selects if lookups are available; else free text
	rep_options = [("", "")] + [
		(str(r.get("report_ID") or r.get("id")), r.get("title") or "") for r in reports
	]
	plan_options = [("", "")] + [
		(str(p.get("plan_ID") or p.get("id")), p.get("title") or "") for p in plans
	]
	admin_options = [("", "")] + [
		(str(a.get("admin_ID") or a.get("id")), a.get("name") or "") for a in admins
	]
	device_options = [("", "")] + [
		(str(d.get("device_ID") or d.get("id")), d.get("transfer") or "") for d in devices
	]

	rep_choice = st.selectbox(
		"report_ID", rep_options, index=0, format_func=lambda x: x[1] or "—"
	)
	plan_choice = st.selectbox(
		"plan_ID", plan_options, index=0, format_func=lambda x: x[1] or "—"
	)
	admin_choice = st.selectbox(
		"admin_ID", admin_options, index=0, format_func=lambda x: x[1] or "—"
	)
	device_choice = st.selectbox(
		"device_ID", device_options, index=0, format_func=lambda x: x[1] or "—"
	)

	submitted = st.form_submit_button("Save")

	if submitted:
		payload = {
			"name": name,
			"email": email,
			"report_ID": rep_choice[0] or None,
			"plan_ID": plan_choice[0] or None,
			"admin_ID": admin_choice[0] or None,
			"device_ID": device_choice[0] or None,
		}
		try:
			if analyst_ID and analyst_ID.strip():
				put(f"/analysts/{analyst_ID}", json=payload)
			else:
				post("/analysts", json=payload)
			st.success("Saved ✅")
			st.experimental_rerun()
		except Exception as e:
			st.error(f"Save failed: {e}")


st.divider()


# --- Delete Analyst
st.subheader("Delete Analyst")
del_id = st.text_input("analyst_ID to delete")
if st.button("Delete Analyst", type="primary", use_container_width=True, disabled=not del_id or not del_id.strip()):
	try:
		delete(f"/analysts/{del_id}")
		st.success("Deleted ✅")
		st.experimental_rerun()
	except Exception as e:
		st.error(f"Delete failed: {e}")