import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import plotly.express as px
import os

# Initialize session state for milk_data
if 'milk_data' not in st.session_state:
    try:
        st.session_state.milk_data = pd.read_csv('milk_production.csv', parse_dates=['Date'])
        if st.session_state.milk_data.empty:
            start_date_default = None
            end_date_default = None
        else:
            start_date_default = date.today() - timedelta(days=1)
            end_date_default = date.today()
    except FileNotFoundError:
        st.session_state.milk_data = pd.DataFrame(columns=['Date', 'Cow Name', 'Morning', 'Noon', 'Evening', 'Total', 'created_at', 'updated_at'])
        st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Create the CSV file
        start_date_default = None
        end_date_default = None

# Ensure start_date_default and end_date_default are defined
if 'start_date_default' not in locals():
    start_date_default = date.today() - timedelta(days=1)
if 'end_date_default' not in locals():
    end_date_default = date.today()

# Read cow names from cows.csv
cows_df = pd.read_csv('cattle.csv')

# Initialize Streamlit app
st.title('Milk Production Tracker')

# Function to load the CSV file
def load_data():
 if os.path.exists('milk_production.csv'):
        data = pd.read_csv('milk_production.csv')
        data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date column is datetime
        return data
# Function to save the DataFrame to the CSV file
def save_data(df):
    df.to_csv('milk_production.csv', index=False)

# Function to update the DataFrame widget
def update_table(filtered_data):
    st.dataframe(filtered_data)

# Function to get the highest milk producer for the filtered data
def get_highest_producer(filtered_data):
    try:
        if not filtered_data.empty:
            filtered_data['Total'] = filtered_data['Morning'] + filtered_data['Noon'] + filtered_data['Evening']
            highest_producer = filtered_data.loc[filtered_data['Total'].idxmax()]
            return highest_producer['Cow Name'], highest_producer['Total']
    except Exception as e:
        st.error(f"Error in get_highest_producer: {e}")
    return None, 0.0

# Function to get the highest producer for a specific time
def get_highest_producer_by_time(filtered_data, time):
    try:
        if not filtered_data.empty:
            highest_producer = filtered_data.loc[filtered_data[time].idxmax()]
            return highest_producer['Cow Name'], highest_producer[time]
    except Exception as e:
        st.error(f"Error in get_highest_producer_by_time: {e}")
    return None, 0.0

# Function to get the total milk produced for the filtered data
def get_total_milk_produced(filtered_data):
    try:
        if not filtered_data.empty:
            filtered_data['Total'] = filtered_data['Morning'] + filtered_data['Noon'] + filtered_data['Evening']
            return filtered_data['Total'].sum()
    except Exception as e:
        st.error(f"Error in get_total_milk_produced: {e}")
    return 0

# Function to get the overall total milk produced
def get_overall_total_milk_produced():
    try:
        if not st.session_state.milk_data.empty:
            st.session_state.milk_data['Total'] = st.session_state.milk_data['Morning'] + st.session_state.milk_data['Noon'] + st.session_state.milk_data['Evening']
            return st.session_state.milk_data['Total'].sum()
    except Exception as e:
        st.error(f"Error in get_overall_total_milk_produced: {e}")
    return 0

# Create interactive widgets
start_date, end_date = st.slider(
    "Select Date Range",
    min_value=date(2023, 1, 1),
    max_value=date.today(),
    value=(date(2023, 1, 1), date.today())
)

# Filter the DataFrame based on the selected date range
if start_date and end_date:
    filtered_data = st.session_state.milk_data[(st.session_state.milk_data['Date'] >= pd.to_datetime(start_date)) & (st.session_state.milk_data['Date'] <= pd.to_datetime(end_date))]
else:
    filtered_data = st.session_state.milk_data

# Create dashboard tiles
highest_producer, highest_production = get_highest_producer(filtered_data)
total_milk_produced = get_total_milk_produced(filtered_data)
overall_total_milk_produced = get_overall_total_milk_produced()

highest_morning_producer, highest_morning_production = get_highest_producer_by_time(filtered_data, 'Morning')
highest_noon_producer, highest_noon_production = get_highest_producer_by_time(filtered_data, 'Noon')
highest_evening_producer, highest_evening_production = get_highest_producer_by_time(filtered_data, 'Evening')

total_morning = filtered_data['Morning'].sum()
total_noon = filtered_data['Noon'].sum()
total_evening = filtered_data['Evening'].sum()

# Sections
st.header("Dashboard")
col1, col2, col3 = st.columns(3)
with col1:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Highest Milk Producer</h4>
                <p style='color: #e44b8d'>{highest_producer if highest_producer else 'N/A'} : {highest_production:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying highest producer: {e}")
with col2:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4 style="font-size: 23.6px;">Total Milk Produced (Start-End Date)</h4>
                <p style='color: #e69b00'>{total_milk_produced:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying total milk produced: {e}")
with col3:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Overall Total Milk Produced</h4>
                <p style='color: #3b8132'>{overall_total_milk_produced:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying overall total milk produced: {e}")

col4, col5, col6 = st.columns(3)
with col4:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Highest Morning Producer</h4>
                <p style='color: #e44b8d'>{highest_morning_producer if highest_morning_producer else 'N/A'} : {highest_morning_production:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying highest morning producer: {e}")
with col5:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Highest Noon Producer</h4>
                <p style='color: #e69b00'>{highest_noon_producer if highest_noon_producer else 'N/A'} : {highest_noon_production:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying highest noon producer: {e}")
with col6:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Highest Evening Producer</h4>
                <p style='color: #3b8132'>{highest_evening_producer if highest_evening_producer else 'N/A'} : {highest_evening_production:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying highest evening producer: {e}")

col7, col8, col9 = st.columns(3)
with col7:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Total Morning Production</h4>
                <p style='color: #e44b8d'>{total_morning:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying total morning production: {e}")
with col8:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Total Noon Production</h4>
                <p style='color: #e69b00'>{total_noon:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying total noon production: {e}")
with col9:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Total Evening Production</h4>
                <p style='color: #3b8132'>{total_evening:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying total evening production: {e}")

# Search and Filter
st.header("Search and Filter")
search_term = st.text_input("Search by Cow Name")
filtered_data = filtered_data[filtered_data['Cow Name'].str.contains(search_term, case=False, na=False)]

# Create interactive widgets
if st.session_state.user_role in ['Manager', 'Admin']:
    selected_index = st.selectbox(
        'Select Record to Edit/Delete',
        options=[None] + list(filtered_data.index),
        format_func=lambda x: 'No selection' if x is None else x
    )
input_date = st.date_input('Input Date', value=date.today())
cow_name_input = st.selectbox('Cow Name', cows_df['Name'])
production_time = st.selectbox('Select Production Time', ['Morning', 'Noon', 'Evening'])
quantity_input = st.number_input('Quantity (L)', step=0.1)
#update_checkbox = st.checkbox('Update Existing Record')

# Arrange buttons in a row format
col1, col2, col3 = st.columns(3)
with col1:
    add_button = st.button('Add Record', key='add_button')

# Debugging print to check the user role
#st.write(f"User role: {st.session_state.user_role}")

if st.session_state.user_role in ['Manager']:
    with col2:
        edit_button = st.button('Edit Record', key='edit_button')

if st.session_state.user_role in ['Admin']:  
    with col3:
        delete_button = st.button('Delete Record', key='delete_button')
# Load the existing data
st.session_state.milk_data = load_data()

# Function to add or update a record in the DataFrame
def add_record():
    if not cow_name_input:
        st.error('Cow Name cannot be empty')
        return
    
    # Check if there's an existing record for the same cow on the same date
    existing_record = st.session_state.milk_data[(st.session_state.milk_data['Date'] == pd.to_datetime(input_date)) & (st.session_state.milk_data['Cow Name'] == cow_name_input)]
    
    if not existing_record.empty:
        index = existing_record.index[0]
        # Update the existing record based on the selected production time
        st.session_state.milk_data.at[index, production_time] = quantity_input
        st.session_state.milk_data.at[index, 'Total'] = (
            st.session_state.milk_data.at[index, 'Morning'] +
            st.session_state.milk_data.at[index, 'Noon'] +
            st.session_state.milk_data.at[index, 'Evening']
        )
        st.session_state.milk_data.at[index, 'updated_at'] = datetime.now()
        st.success('Successfully Updated!')
    else:
        # Add a new record
        new_record = pd.DataFrame({
            'Date': [pd.to_datetime(input_date)],
            'Cow Name': [cow_name_input],
            'Morning': [quantity_input if production_time == 'Morning' else 0],
            'Noon': [quantity_input if production_time == 'Noon' else 0],
            'Evening': [quantity_input if production_time == 'Evening' else 0],
            'Total': [quantity_input],
            'created_at': [datetime.now()],
            'updated_at': [datetime.now()]
        })
        st.session_state.milk_data = pd.concat([st.session_state.milk_data, new_record], ignore_index=True)
        st.success('Successfully Added!')
    
    save_data(st.session_state.milk_data)  # Save to CSV
    st.rerun()  # Refresh the page

# Function to edit a selected record in the DataFrame
def edit_record():
    if not cow_name_input:
        st.error('Cow Name cannot be empty')
        return
    if selected_index is not None:
        st.session_state.milk_data.at[selected_index, 'Date'] = pd.to_datetime(input_date)
        st.session_state.milk_data.at[selected_index, 'Cow Name'] = cow_name_input
        st.session_state.milk_data.at[selected_index, production_time] = quantity_input
        st.session_state.milk_data.at[selected_index, 'Total'] = (
            st.session_state.milk_data.at[selected_index, 'Morning'] +
            st.session_state.milk_data.at[selected_index, 'Noon'] +
            st.session_state.milk_data.at[selected_index, 'Evening']
        )
        st.session_state.milk_data.at[selected_index, 'updated_at'] = datetime.now()
        save_data(st.session_state.milk_data)  # Save to CSV
        st.success('Successfully Edited!')
        st.rerun()  # Refresh the page

# Function to delete a selected record from the DataFrame
def delete_record():
    if selected_index is not None:
        st.session_state.milk_data = st.session_state.milk_data.drop(selected_index).reset_index(drop=True)
        save_data(st.session_state.milk_data)  # Save to CSV
        st.success('Successfully Deleted!')
        st.rerun()  # Refresh the page

# Handle button clicks
if add_button:
    add_record()

if st.session_state.user_role in ['Manager']:
    if edit_button:
        edit_record()
if st.session_state.user_role in ['Admin']:
    if delete_button:
        delete_record()

# Display the DataFrame 
update_table(filtered_data)

# Calculate totals for Morning, Noon, and Evening production
total_morning = filtered_data['Morning'].sum()
total_noon = filtered_data['Noon'].sum()
total_evening = filtered_data['Evening'].sum()

# Display a pie chart of the production times
production_totals = pd.DataFrame({
    'Production Time': ['Morning', 'Noon', 'Evening'],
    'Total': [total_morning, total_noon, total_evening]
})

st.write("### Milk Production Distribution")
fig = px.pie(production_totals, values='Total', names='Production Time', title='Production Distribution')
st.plotly_chart(fig, use_container_width=True)

# Create bar chart for total milk production over time
st.bar_chart(filtered_data.set_index('Date')['Total'])

# Create line chart for milk production over time for each cow
line_chart_data = filtered_data.pivot(index='Date', columns='Cow Name', values='Total')
st.line_chart(line_chart_data)
