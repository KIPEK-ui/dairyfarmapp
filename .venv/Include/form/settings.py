import streamlit as st
import pandas as pd

# Initialize session state for page, user_role, and users
if 'page' not in st.session_state:
    st.session_state.page = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def save_users_to_csv():
    df = pd.DataFrame(st.session_state.users)
    df.to_csv('users.csv', index=False)

def settings():
    st.title('Settings')
    
    # Print user role and users list
    #st.write(f"User role: {st.session_state.user_role}")
    #st.write(st.session_state.users)

    if st.session_state.user_role == 'Admin':
        usernames = [user['username'] for user in st.session_state.users]
        selected_username = st.selectbox('Select Username', usernames, key='selected_username')
        current_user = next((user for user in st.session_state.users if user['username'] == selected_username), None)
    else:
        current_user = next((user for user in st.session_state.users if user['role'] == st.session_state.user_role), None)

    if current_user:
        st.write("### Current Values")
        st.write(f"**Username:** {current_user['username']}")
        
        if st.session_state.user_role == 'Admin' and current_user['username'] != st.session_state.user_role:
            new_role = st.selectbox('Role', options=['Worker', 'Manager', 'Admin'], index=['Worker', 'Manager', 'Admin'].index(current_user['role']), key='new_role')
        else:
            new_role = current_user['role']
            st.write(f"**Role:** {new_role}")

        if st.session_state.user_role in ['Manager', 'Worker']:
          
            new_username = current_user['username']

        new_password = st.text_input('Password', type='password', value=current_user['password'], key='new_password')
        new_phone_number = st.text_input('Phone Number', value=current_user['phone_number'], key='new_phone_number')

        if st.button('Update'):
            if not new_password or not new_phone_number:
                st.error('Password and Phone Number are required fields.')
            else:
                if st.session_state.user_role in ['Manager', 'Worker']:
                    current_user['username'] = new_username
                current_user['password'] = new_password
                current_user['phone_number'] = new_phone_number
                current_user['role'] = new_role
                st.session_state.users = [user if user['username'] != current_user['username'] else current_user for user in st.session_state.users]
                save_users_to_csv()
                st.success('User details updated successfully!')
                st.write(st.session_state.users)
    else:
        st.error('User not found')

# Call the settings function
settings()
