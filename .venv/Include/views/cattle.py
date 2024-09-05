import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for the cattle health CSV
file_path = 'cattle.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['ID', 'Name', 'Breed', 'Age', 'Status', 'DoB', 'DoA'])
    df.to_csv(file_path, index=False)

# Load cattle health data
def load_data():
    return pd.read_csv(file_path)

# Save cattle health data
def save_data(df):
    df.to_csv(file_path, index=False)

# Function to calculate age from date of birth
def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Function to add a new record
def add_record(id, name, breed, age, status, dob, doa):
    df = load_data()
    new_entry = pd.DataFrame({'ID': [id], 'Name': [name], 'Breed': [breed], 'Age': [age], 'Status': [status], 'DoB': [dob], 'DoA': [doa]})
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.success('Entry added successfully!')
    st.rerun()  # Refresh the page

# Function to edit an existing record
def edit_record(selected_index, id, name, breed, age, status, dob, doa):
    df = load_data()
    if selected_index is not None:
        df.at[selected_index, 'ID'] = id
        df.at[selected_index, 'Name'] = name
        df.at[selected_index, 'Breed'] = breed
        df.at[selected_index, 'Age'] = age
        df.at[selected_index, 'Status'] = status
        df.at[selected_index, 'DoB'] = dob
        df.at[selected_index, 'DoA'] = doa
        save_data(df)
        st.success('Successfully Edited!')
        st.rerun()  # Refresh the page
    else:
        st.error('Selected index is None!')

# Function to delete a record
def delete_record(selected_index):
    df = load_data()
    if selected_index is not None:
        df = df.drop(selected_index)
        save_data(df)
        st.success('Entry deleted successfully!')
        st.rerun()  # Refresh the page
    else:
        st.error('Selected index is None!')

# Initialize Streamlit app
st.title('Cattle Health Management App')

# Load data
df = load_data()

# Select index for editing/deleting
selected_index = st.selectbox('Select Index', df.index)

# Input widgets for column names
id = st.text_input('ID')
name = st.text_input('Name')
breed = st.selectbox('Breed',['Freshian','Aryshire','Jersey','Flekviev'])
dob = st.date_input('Date of Birth')
doa = st.date_input('Date of Arrival')
status = st.selectbox('Status', ['Sick', 'Out of Farm', 'Milking', 'Incalf', 'Dry Cow', 'Calf', 'Heifers', 'Bulling'])

# Calculate age from date of birth
age = calculate_age(dob)



# Arrange buttons in a row
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Submit'):
        add_record(id, name, breed, age, status, dob, doa)

with col2:
    if st.button('Edit'):
        edit_record(selected_index, id, name, breed, age, status, dob, doa)

with col3:
    if st.button('Delete'):
        delete_record(selected_index)

# Display data
st.dataframe(df)
