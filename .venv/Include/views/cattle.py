import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import plotly.express as px

# File path for the cattle health CSV
file_path = 'cattle.csv'

# Create the CSV file if it doesn't exist or is empty
if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
    df = pd.DataFrame(columns=['Cow ID', 'Name', 'Breed', 'DoB', 'DoA'])
    df.to_csv(file_path, index=False)

# Load cattle health data
def load_data():
    return pd.read_csv(file_path, dtype={'Cow ID': str})

# Save cattle health data
def save_data(df):
    df.to_csv(file_path, index=False)

# Function to calculate age from date of birth
def calculate_age(dob):
    today = date.today()
    dob = datetime.strptime(dob, '%Y-%m-%d').date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Initialize Streamlit app
st.title('Cattle Management App')

# Load data
df = load_data()

# Calculate ages and add to dataframe
df['Age'] = df['DoB'].apply(calculate_age)

# Dashboard values
oldest_cow = df.loc[df['Age'].idxmax()] if not df.empty else None
youngest_cow = df.loc[df['Age'].idxmin()] if not df.empty else None
average_age = df['Age'].mean() if not df.empty else 0
total_cows = len(df)

# Dashboard display
st.header("Dashboard")
col1, col2 = st.columns(2)
with col2:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Average Age of Cows</h4>
            <p style='color: #e69b00'>{average_age:.2f} years</p>
        </div>
    """, unsafe_allow_html=True)
with col1:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Total Number of Cows</h4>
            <p style='color: #3b8132'>{total_cows}</p>
        </div>
    """, unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Oldest Cow</h4>
            <p style='color: #e44b8d'>{oldest_cow['Name'] if oldest_cow is not None else 'N/A'} : {oldest_cow['Age'] if oldest_cow is not None else 'N/A'} years (DoB: {oldest_cow['DoB'] if oldest_cow is not None else 'N/A'})</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Youngest Cow</h4>
            <p style='color: #e44b8d'>{youngest_cow['Name'] if youngest_cow is not None else 'N/A'} : {youngest_cow['Age'] if youngest_cow is not None else 'N/A'} years (DoB: {youngest_cow['DoB'] if youngest_cow is not None else 'N/A'})</p>
        </div>
    """, unsafe_allow_html=True)

# Search and Filter section
st.subheader('Search and Filter')
search_name = st.text_input('Search by Cow Name')
search_breed = st.selectbox('Search by Breed', ['All', 'Freshian', 'Aryshire', 'Jersey', 'Flekviev'])
search_id = st.text_input('Search by Cow ID')

filtered_df = df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
if search_breed != 'All':
    filtered_df = filtered_df[filtered_df['Breed'] == search_breed]
if search_id:
    filtered_df = filtered_df[filtered_df['Cow ID'].str.contains(search_id)]



# Input section for adding new records
st.subheader('Add New Record')
id_input = st.text_input('Cow ID')
name_input = st.text_input('Name')
breed_input = st.selectbox('Breed', ['Freshian', 'Aryshire', 'Jersey', 'Flekviev'])
dob_input = st.date_input('Date of Birth')
doa_input = st.date_input('Date of Arrival')

if st.button('Submit'):
    new_record = pd.DataFrame({'Cow ID': [id_input], 'Name': [name_input], 'Breed': [breed_input], 
                               'DoB': [dob_input.strftime('%Y-%m-%d')], 'DoA': [doa_input.strftime('%Y-%m-%d')]})
    df = pd.concat([df, new_record], ignore_index=True)
    save_data(df)
    st.success('Record added successfully!')
    st.rerun()

# Cattle Records display
st.subheader('Cattle Records')
st.dataframe(filtered_df)

# Plot graphs for breed distribution and age distribution

# Breed Distribution Pie Chart
st.header("Breed Distribution")
fig1 = px.pie(df, names='Breed', title='Breed Distribution')
st.plotly_chart(fig1, use_container_width=True)

# Age Distribution Bar Chart
st.header("Age Distribution")
fig2 = px.bar(df, x='Name', y='Age', title='Age Distribution')
st.plotly_chart(fig2, use_container_width=True)
