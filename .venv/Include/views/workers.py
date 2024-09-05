import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for the workers CSV
file_path = 'workers.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['Name', 'Role', 'Start Date', 'Contact'])
    df.to_csv(file_path, index=False)

# Load workers data
def load_data():
    return pd.read_csv(file_path)

# Save workers data
def save_data(df):
    df.to_csv(file_path, index=False)

# Initialize Streamlit app
st.title('Farm Workers Management App')

# Load data into session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Display workers
st.subheader('Current Workers')
st.dataframe(st.session_state.df)

# Add new worker
st.subheader('Add New Worker')
name = st.text_input('Name')
role = st.text_input('Role')
start_date = st.date_input('Start Date')
contact = st.text_input('Contact')
if st.button('Add Worker'):
    new_worker = pd.DataFrame([{
        'Name': name,
        'Role': role,
        'Start Date': start_date.strftime('%Y-%m-%d'),
        'Contact': contact
    }])
    st.session_state.df = pd.concat([st.session_state.df, new_worker], ignore_index=True)
    save_data(st.session_state.df)
    st.success('Worker added successfully!')

# Update worker
st.subheader('Update Worker')
worker_to_update = st.selectbox('Select Worker to Update', st.session_state.df.index)
new_name = st.text_input('New Name', value=st.session_state.df.at[worker_to_update, 'Name'])
new_role = st.text_input('New Role', value=st.session_state.df.at[worker_to_update, 'Role'])
new_start_date = st.date_input('New Start Date', value=datetime.strptime(st.session_state.df.at[worker_to_update, 'Start Date'], '%Y-%m-%d'))
new_contact = st.text_input('New Contact', value=st.session_state.df.at[worker_to_update, 'Contact'])
if st.button('Update Worker'):
    st.session_state.df.at[worker_to_update, 'Name'] = new_name
    st.session_state.df.at[worker_to_update, 'Role'] = new_role
    st.session_state.df.at[worker_to_update, 'Start Date'] = new_start_date.strftime('%Y-%m-%d')
    st.session_state.df.at[worker_to_update, 'Contact'] = new_contact
    save_data(st.session_state.df)
    st.success('Worker updated successfully!')

# Remove worker
st.subheader('Remove Worker')
worker_to_remove = st.selectbox('Select Worker to Remove', st.session_state.df.index)
if st.button('Remove Worker'):
    st.session_state.df = st.session_state.df.drop(worker_to_remove)
    save_data(st.session_state.df)
    st.success('Worker removed successfully!')
