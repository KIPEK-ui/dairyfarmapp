import streamlit as st
import pandas as pd
import os

# Initialize session state variables
if 'users' not in st.session_state:
    if os.path.exists('users.csv'):
        try:
            st.session_state.users = pd.read_csv('users.csv').to_dict('records')
        except pd.errors.EmptyDataError:
            st.session_state.users = []
            # Create the users.csv file with the appropriate columns if it doesn't exist or is empty
            df = pd.DataFrame(columns=['username', 'password', 'role', 'name', 'phone_number'])
            df.to_csv('users.csv', index=False)

if 'page' not in st.session_state:
    st.session_state.page = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def save_users_to_csv():
    df = pd.DataFrame(st.session_state.users)
    df.to_csv('users.csv', index=False)

def login():
    st.title('Login')
    username = st.text_input('Username', key='login_username')
    password = st.text_input('Password', type='password', key='login_password')
    role = st.selectbox('Role', ['Worker', 'Manager', 'Admin'], key='login_role')
    login_button = st.button('Login', key='login_button')

    if login_button:
        # Authentication logic
        user = next((user for user in st.session_state.users if user['username'] == username and user['password'] == password and user['role'] == role), None)
        if user:
            st.session_state.user_role = role  # Set the user_role to the role
            st.session_state.logged_in = True
            st.session_state.page = 'Milk Production Tracker'
            st.success(f'Logged in as {role}')
            st.rerun()  # Force a rerun of the script
        else:
            st.error('Invalid username, password, or role')

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.page = None
    st.success('Logged out successfully')

# Call the login function
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    if st.session_state.page == 'Signup':
        from form.signup import signup
        signup()
else:
    st.write(f'Welcome, {st.session_state.user_role}!')
    if st.button('Logout', key='logout_button'):
        logout()
