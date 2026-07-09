Project summary — what we set out to do
This repo is a Streamlit frontend + Flask REST API + MySQL template used for course work and experimentation. The main objective was to make the Streamlit pages persistent (Goals / Progress) by exposing and using REST endpoints and a MySQL schema, plus add administrative pages and stabilize the front-end interactions. Over the session we implemented backend endpoints, seeded the DB, added and fixed Streamlit pages, and resolved multiple runtime issues caused by duplicated widgets and incompatible Streamlit calls.

High-level changes performed
Implemented many Flask CRUD endpoints (Goals, Plans, Reports, Analysis_Team, System, User_Device, etc.) inside the api backend.
Seeded my.sql with many sample rows (including ~30 rows for Goal) so the UI has data to display.

Created/updated Streamlit pages in pages:
Login (40_User_Home.py), Goals UI (41_User_Goal.py), multiple admin pages (20_Admin_Home.py, 22_Analyst_Team.py, 23_Reports.py, 24_Systems.py, 25_User_Devices.py) and helpers.
Added a small api_client.py helper and nav.py for sidebar navigation.
Fixed multiple Streamlit runtime issues:
Removed duplicated widget creation and multiple SideBarLinks() calls.
Replaced st.experimental_rerun() / st.rerun() usages with in-place placeholders or safe refresh patterns.
Removed unsupported kwargs on st.form_submit_button() (some Streamlit versions disallow key=).
Added explicit key= arguments to text inputs/selectboxes/button widgets when needed to avoid auto-ID collisions.
Verified edits with local Python compile checks (py -3 -m py_compile) for updated pages.

Files changed / added (concise)
api/backend/... (many route files) — Added/extended CRUD endpoints for Goals, Plans, Reports, Analysis_Team, System, User_Device and other nested resources (no DB schema changes).
my.sql — Seed data added (Goal table and many others).
20_Admin_Home.py — Admin landing page with navigation buttons to admin pages.
22_Analyst_Team.py — Admin page for Analysts; cleaned duplicate UI; placeholder refresh.
23_Reports.py — Reports admin page; switched rerun -> placeholder, added keys.
24_Systems.py — Systems admin page; switched rerun -> placeholder, added keys.
25_User_Devices.py — User Devices admin page; removed duplicated blocks, added placeholder refresh and keys.
40_User_Home.py — Login form; sets st.session_state user attributes.
41_User_Goal.py — Goals CRUD UI (in-session) with charting; bound sample goals to logged-in user_ID.
nav.py — Sidebar link generation (RBAC based) — inspected and left intact except ensuring single invocation usage.
api_client.py — API helper functions (GET/POST/PUT/DELETE) used by admin pages.
Implementation notes and patterns

Backend:
Flask Blueprints per resource; routes use db.get_db().cursor() and parameterized SQL. Endpoints were added to map to the DB schema (Goal columns: user_ID, goal_name, task, tracking, records, reminders).
No database schema changes were made — we conformed to the explicit constraint.

Frontend (Streamlit):
Use st.session_state to persist logged-in user and page-scoped state.
Avoid duplicated widget creation (StreamlitDuplicateElementId). Use key= on widgets when needed.
Avoid st.experimental_rerun() where unavailable. Instead, refresh a st.empty() placeholder in-place after create/update/delete actions.
Navigation: SideBarLinks() builds RBAC-aware sidebar links; call it only once per page.
Dev / ops:
Docker Compose used to run app (Streamlit), api (Flask), and mysql_db. We used detached runs (docker compose up -d) during testing.

Quick per-file syntax checks were used frequently:
Example: py -3 -m py_compile [25_User_Devices.py](http://_vscodecontentref_/39)"
Key bug fixes (what caused the issues and how they were fixed)
Duplicate sidebar and widget errors:
Cause: Files contained duplicated content (multiple imports and repeated SideBarLinks() calls) after iterative edits. Streamlit throws a StreamlitDuplicateElementId when two identical widget instances are created.
Fix: Consolidated each page to a single flow; removed duplicated blocks; added explicit key= where needed.
Missing submit button / unsupported form kwargs:
Cause: Some forms had no st.form_submit_button() inside the with st.form(...) block, or st.form_submit_button() used unsupported kwargs like key= for the runtime version in use.
Fix: Ensured every with st.form block includes st.form_submit_button(); removed unsupported keyword args from form_submit_button.
st.experimental_rerun() not available:
Cause: Streamlit version mismatch; method unavailable in the environment.
Fix: Use st.empty() placeholders and re-fetch data after actions instead of forcing a rerun.
Other small fixes:
Added try/except wrappers around API calls to show warnings instead of throwing runtime errors.
Standardized sidebar API text input usage so the BASE_URL can be changed from the UI.