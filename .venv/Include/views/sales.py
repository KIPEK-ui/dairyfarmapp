import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import os

# File path for the sales CSV
file_path = 'sales.csv'
milk_production_file_path = 'milk_production.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['Date', 'Customer Name', 'Quantity (Liters)', 'Price per Liter (Ksh)', 'Total (Ksh)', 'Payment Ref', 'Status', 'created_at', 'updated_at'])
    df.to_csv(file_path, index=False)

# Load sales data
def load_data(file_path):
    return pd.read_csv(file_path)

# Save sales data
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Function to update the DataFrame widget
def update_table(date_filtered_data):
    st.dataframe(date_filtered_data)


# Load milk production data
milk_production_df = load_data(milk_production_file_path)

# Initialize Streamlit app
st.title('Milk Sales Tracking App')

# Initialize session state for sales data
if 'df' not in st.session_state:
    st.session_state.df = load_data(file_path)

# Date range selector
st.subheader('Filter by Date Range')
start_date, end_date = st.date_input('Select Date Range', value=[date(2023, 1, 1), date.today()])
if start_date and end_date:
    date_filtered_data = st.session_state.df[(st.session_state.df['Date'] >= start_date.strftime('%Y-%m-%d')) & (st.session_state.df['Date'] <= end_date.strftime('%Y-%m-%d'))]

# Dashboard tiles
st.header('Dashboard')
total_sales = st.session_state.df['Total (Ksh)'].sum()
total_quantity = st.session_state.df['Quantity (Liters)'].sum()
cleared_sales = st.session_state.df[st.session_state.df['Status'] == 'Paid']['Total (Ksh)'].sum()
not_cleared_sales = st.session_state.df[st.session_state.df['Status'] == 'Not Cleared']['Total (Ksh)'].sum()
total_milk_production = milk_production_df['Total'].sum()
milk_remaining = total_milk_production - total_quantity
best_customer = st.session_state.df.groupby('Customer Name')['Quantity (Liters)'].sum().idxmax()if not st.session_state.df.empty else "N/A"
best_customer_quantity = st.session_state.df.groupby('Customer Name')['Quantity (Liters)'].sum().max() if not st.session_state.df.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Total Sales</h4>
            <p style='color: #e69b00'>{total_sales:.2f}Ksh</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Total Quantity</h4>
            <p style='color: #e69b00'>{total_quantity:.2f} L</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Cleared Sales</h4>
            <p style='color: #3b8132'>{cleared_sales:.2f}Ksh</p>
        </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Not Cleared Sales</h4>
            <p style='color: #3b8132'>{not_cleared_sales:.2f}Ksh</p>
        </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Milk Remaining</h4>
            <p style='color: #e69b00'>{milk_remaining:.2f} L</p>
        </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
        <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Best Customer</h4>
            <p style='color: #e44b8d'>{best_customer}</p>
            <p style='color: #e44b8d'>{best_customer_quantity:.2f} L</p>
        </div>
    """, unsafe_allow_html=True)
# Search and Filter
st.subheader("Search and Filter")
search_term = st.text_input("Search by Customer Name or Status")

# Filter the data based on the search term
date_filtered_data = date_filtered_data[
    date_filtered_data['Customer Name'].str.contains(search_term, case=False, na=False) |
    date_filtered_data['Status'].str.contains(search_term, case=False, na=False)
]
# Create interactive widgets

if st.session_state.user_role in ['Manager', 'Admin']:
    st.subheader("Select Sale Record To Update")
    selected_index = st.selectbox(
        'Select Record to Edit',
        options=[None] + list(date_filtered_data.index),
        format_func=lambda x: 'No selection' if x is None else x
    )
st.subheader('Input Sale')
sale_date = st.date_input('Sale Date', value=date.today())
customer_name = st.text_input('Customer Name')
quantity = st.number_input('Quantity (Liters)', min_value=0.0, step=0.1)
price_per_liter = st.selectbox('Price per Liter (Ksh)', [50, 55, 60])
payment_ref = st.text_input('Payment Ref')
status = st.selectbox('Status', ['Paid', 'Not Cleared'])
# Arrange buttons in a row format
col1, col2, col3 = st.columns(3)
with col1:
    add_button = st.button('Add Sale', key='add_button')

# Debugging print to check the user role
#st.write(f"User role: {st.session_state.user_role}")

if st.session_state.user_role in ['Manager']:
    with col2:
        edit_button = st.button('Update Sale', key='edit_button')

if st.session_state.user_role in ['Admin']:  
    with col3:
        delete_button = st.button('Delete Sale', key='delete_button')

# Function to add a new sale
def add_sale():
    total = quantity * price_per_liter
    new_sale = pd.DataFrame([{
        'Date': sale_date.strftime('%Y-%m-%d'),
        'Customer Name': customer_name,
        'Quantity (Liters)': quantity,
        'Price per Liter (Ksh)': price_per_liter,
        'Total (Ksh)': total,
        'Payment Ref': payment_ref,
        'Status': status,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    st.session_state.df = pd.concat([st.session_state.df, new_sale], ignore_index=True)
    save_data(st.session_state.df, file_path)
    st.success('Sale added successfully!')
    st.rerun()  # Refresh the page

# Function to update a sale
def update_sale():
    st.session_state.df.at[selected_index, 'Quantity (Liters)'] = quantity
    st.session_state.df.at[selected_index, 'Price per Liter (Ksh)'] = price_per_liter
    st.session_state.df.at[selected_index, 'Total (Ksh)'] = quantity * price_per_liter
    st.session_state.df.at[selected_index, 'Payment Ref'] = payment_ref
    st.session_state.df.at[selected_index, 'Status'] = status
    st.session_state.df.at[selected_index, 'updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_data(st.session_state.df, file_path)
    st.success('Sale updated successfully!')
    st.rerun()  # Refresh the page

# Function to remove a sale
def remove_sale():
    st.session_state.df = st.session_state.df.drop(selected_index).reset_index(drop=True)
    save_data(st.session_state.df, file_path)
    st.success('Sale removed successfully!')
    st.rerun()  # Refresh the page
# Handle button clicks
if add_button:
    add_sale()

if st.session_state.user_role in ['Manager']:
    if edit_button:
        update_sale()
if st.session_state.user_role in ['Admin']:
    if delete_button:
        remove_sale()

# Display sales
st.subheader('Sales Records')
update_table(date_filtered_data)

# Update charts based on date range
st.header('Sales Status Distribution')
status_distribution = date_filtered_data['Status'].value_counts().reset_index()
status_distribution.columns = ['Status', 'Count']
fig = px.pie(status_distribution, values='Count', names='Status', title='Sales Status Distribution')
st.plotly_chart(fig, use_container_width=True)

st.header('Sales by Customer')
sales_by_customer = date_filtered_data.groupby('Customer Name')['Total (Ksh)'].sum().reset_index()
fig = px.bar(sales_by_customer, x='Customer Name', y='Total (Ksh)', title='Sales by Customer')
st.plotly_chart(fig, use_container_width=True)

st.header('Sales Over Time')
sales_over_time = date_filtered_data.groupby('Date')['Total (Ksh)'].sum().reset_index()
fig = px.line(sales_over_time, x='Date', y='Total (Ksh)', title='Sales Over Time')
st.plotly_chart(fig, use_container_width=True)
