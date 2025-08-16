import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import BASE_URL, set_base_url, get, post, put, delete

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Reports")

st.sidebar.subheader("API")
api_url = st.sidebar.text_input("Base URL", value=BASE_URL)
if api_url:
	set_base_url(api_url)


# --- List Reports
st.subheader("All Reports")
# placeholder for table refresh
reports_placeholder = st.empty()
def fetch_reports():
	try:
		return get('/reports').json()
	except Exception as e:
		st.warning(f'Could not fetch reports: {e}')
		return []

reports = fetch_reports()
reports_placeholder.dataframe(reports, use_container_width=True)

st.divider()


# --- Create / Update Report
st.subheader("Create / Update Report")
with st.form("report_form"):
	report_ID = st.text_input("report_ID (leave empty to create)", key='report_id')
	title = st.text_input("title", key='report_title')
	checklist = st.text_area("checklist", key='report_checklist')
	completed_goals = st.text_area("completed_goals", key='report_completed')
	uncompleted_goals = st.text_area("uncompleted_goals", key='report_uncompleted')
	work_efficiency = st.text_input("work_efficiency", key='report_eff')  # string or %; backend stores as text/BLOB
	time_based_summary = st.text_area("time_based_summary", key='report_summary')
	submitted = st.form_submit_button("Save")

	if submitted:
		payload = {
			"title": title,
			"checklist": checklist,
			"completed_goals": completed_goals,
			"uncompleted_goals": uncompleted_goals,
			"work_efficiency": work_efficiency,
			"time_based_summary": time_based_summary,
		}
		try:
			if report_ID and report_ID.strip():
				put(f"/reports/{report_ID}", json=payload)
			else:
				post("/reports", json=payload)
			st.success("Saved ✅")
			# refresh in-place
			reports = fetch_reports()
			reports_placeholder.dataframe(reports, use_container_width=True)
		except Exception as e:
			st.error(f"Save failed: {e}")

st.divider()


# --- Delete Report
st.subheader("Delete Report")
del_id = st.text_input("report_ID to delete", key='del_report_id')
if st.button("Delete Report", type="primary", use_container_width=True, disabled=not del_id or not del_id.strip(), key='delete_report_btn'):
	try:
		delete(f"/reports/{del_id}")
		st.success("Deleted ✅")
		reports = fetch_reports()
		reports_placeholder.dataframe(reports, use_container_width=True)
	except Exception as e:
		st.error(f"Delete failed: {e}")