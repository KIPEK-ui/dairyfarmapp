import streamlit as st
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from form.login import login, logout
from form.signup import signup

# Initialize session state for user_role, logged_in, page, and users
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = None
# Initialize session state variables
if 'users' not in st.session_state:
    if os.path.exists('users.csv'):
        try:
            st.session_state.users = pd.read_csv('users.csv').to_dict('records')
        except pd.errors.EmptyDataError:
            st.session_state.users = []


# Auto-refresh every 60 seconds
count = st_autorefresh(interval=60000, limit=100, key="refresh")

# Check for inactivity
if 'last_active' not in st.session_state:
    st.session_state.last_active = count

if st.session_state.logged_in:
    if count - st.session_state.last_active > 3:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.page = None
        st.success('Logged out due to inactivity')
else:
        st.session_state.last_active = count

# --- PAGE SETUP ---
milk_page = st.Page(
    "views/milk.py",
    title="Milk Production Tracker",
    icon=":material/account_circle:",
    default=True,
)
sales_page = st.Page(
    "views/sales.py",
    title="Sales Dashboard",
    icon=":material/receipt_long:",
)
inventory_page = st.Page(
    "views/inventory.py",
    title="Inventory",
    icon=":material/store:",
)
workers_page = st.Page(
    "views/workers.py",
    title="Workers",
    icon=":material/person_add:",
)
cattle_page = st.Page(
    "views/cattle.py",
    title="Cattle",
    icon=":material/agriculture:",
)
settings_page = st.Page(
    "form/settings.py",
    title="Settings",
    icon=":material/manage_accounts:",
)
dashboard_page = st.Page(
    "views/dashboard.py",
    title="Dashboard",
    icon=":material/menu:",
)
correlation_page = st.Page(
    "views/correlation.py",
    title="Correlation Analysis",
    icon=":material/monitoring:",
)

feed_page = st.Page(
    "views/feed.py",
    title="Feed Management",
    icon=":material/agriculture:",
)

health_page = st.Page(
    "views/health.py",
    title="Cattle Health Monitoring",
    icon=":material/heart_plus:",
)

finance_page = st.Page(
    "views/finance.py",
    title="Finance",
    icon=":material/trending_up:",
)

analysis_page = st.Page(
    "views/analysis.py",
    title="Economic Analysis",
    icon=":material/analytics:",
)
# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Miginon Dairy Farm Management App": [dashboard_page],
        "Farm Operations": [correlation_page],
        "Milk Management": [milk_page,sales_page],
        "Feed Management": [feed_page],
        "Cattle Management": [cattle_page,health_page],
        "Farm Management": [workers_page, inventory_page],
        "Finance Management": [finance_page, analysis_page],
        "Settings": [settings_page],
    }
)

# --- SHARED ON ALL PAGES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, 'assets', 'logo.png')
image_path_2 = os.path.join(current_dir, 'assets', 'logo.png')
st.logo(image_path)  
#st.image(image_path_2, width=100)# Adjust the width as needed
st.sidebar.markdown("Made with Prescision")

# --- LOGIN/LOGOUT ---
if not st.session_state.logged_in:
    if st.session_state.page == 'Signup':
        signup()
    else:
        login()
        if st.sidebar.button('Create an Account', key='create_account_button'):
            st.session_state.page = 'Signup'
            st.rerun()  # Force a rerun of the script
else:
    st.sidebar.button('Logout', on_click=logout)
    # --- RUN NAVIGATION ---
    if st.session_state.page == 'Milk Production Tracker':
        pg.run()
