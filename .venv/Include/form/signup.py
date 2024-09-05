import streamlit as st
import pandas as pd


# Initialize session states
if 'users' not in st.session_state:
    try:
        st.session_state.users = pd.read_csv('users.csv').to_dict(orient='records')
    except FileNotFoundError:
        st.session_state.users = []
        # Create the users.csv file with the appropriate columns if it doesn't exist
        df = pd.DataFrame(columns=['username', 'password', 'role', 'name', 'phone_number'])
        df.to_csv('users.csv', index=False)
if 'page' not in st.session_state:
    st.session_state.page = None

def save_users_to_csv():
    df = pd.DataFrame(st.session_state.users)
    df.to_csv('users.csv', index=False)

def signup():
    st.title('Signup')
    signup_username = st.text_input('Username', key='signup_username')
    password = st.text_input('Password', type='password', key='signup_password')
    name = st.text_input('Name', key='signup_name')
    role = st.selectbox('Role', ['Worker', 'Manager', 'Admin'], key='signup_role')
    phone_number = st.text_input('Phone Number', key='signup_phone_number')
    signup_button = st.button('Signup', key='signup_button')

    if signup_button:
        if signup_username and password and phone_number:
            user_count = sum(1 for user in st.session_state.users if user['role'] == role)
            if role == 'Manager' and user_count >= 2:
                st.error('Managerial role is full. Please choose a different role.')
            elif role == 'Worker' and user_count >= 6:
                st.error('Worker role is full. Please choose a different role.')
            elif role == 'Admin' and user_count >= 3:
                st.error('Admin role is full. Please choose a different role.')
            else:
                st.session_state.users.append({'username': signup_username, 'password': password, 'name': name, 'role': role, 'phone_number': phone_number})
                save_users_to_csv()
                st.success('Signup successful! Redirecting to login...')
                st.session_state.page = 'Login'
                st.rerun()  # Force a rerun of the script
        else:
            st.error('Please fill in the username, password, and phone number fields')

