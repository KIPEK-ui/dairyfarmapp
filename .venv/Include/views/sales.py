import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for the sales CSV
file_path = 'sales.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['Date', 'Customer', 'Quantity (Liters)', 'Price per Liter (Ksh)', 'Total (Ksh)'])
    df.to_csv(file_path, index=False)

# Load sales data
def load_data():
    return pd.read_csv(file_path)

# Save sales data
def save_data(df):
    df.to_csv(file_path, index=False)

# Initialize Streamlit app
st.title('Milk Sales Tracking App')

# Load data into session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Display sales
st.subheader('Sales Records')
st.dataframe(st.session_state.df)

# Add new sale
st.subheader('Add New Sale')
customer = st.text_input('Customer Name')
quantity = st.number_input('Quantity (Liters)', min_value=0.0, step=0.1)
price_per_liter = st.selectbox('Price per Liter (Ksh)', [50, 55, 60])
if st.button('Add Sale'):
    total = quantity * price_per_liter
    new_sale = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Customer': customer,
        'Quantity (Liters)': quantity,
        'Price per Liter (Ksh)': price_per_liter,
        'Total (Ksh)': total
    }])
    st.session_state.df = pd.concat([st.session_state.df, new_sale], ignore_index=True)
    save_data(st.session_state.df)
    st.success('Sale added successfully!')

# Update sale
st.subheader('Update Sale')
sale_to_update = st.selectbox('Select Sale to Update', st.session_state.df.index)
new_quantity = st.number_input('New Quantity (Liters)', min_value=0.0, step=0.1)
new_price_per_liter = st.selectbox('New Price per Liter (Ksh)', [50, 55, 60])
if st.button('Update Sale'):
    st.session_state.df.at[sale_to_update, 'Quantity (Liters)'] = new_quantity
    st.session_state.df.at[sale_to_update, 'Price per Liter (Ksh)'] = new_price_per_liter
    st.session_state.df.at[sale_to_update, 'Total (Ksh)'] = new_quantity * new_price_per_liter
    st.session_state.df.at[sale_to_update, 'Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_data(st.session_state.df)
    st.success('Sale updated successfully!')

# Remove sale
st.subheader('Remove Sale')
sale_to_remove = st.selectbox('Select Sale to Remove', st.session_state.df.index)
if st.button('Remove Sale'):
    st.session_state.df = st.session_state.df.drop(sale_to_remove)
    save_data(st.session_state.df)
    st.success('Sale removed successfully!')
