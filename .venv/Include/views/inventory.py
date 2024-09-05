import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for the inventory CSV
file_path = 'inventory.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['Item', 'Category', 'Quantity', 'Last Updated'])
    df.to_csv(file_path, index=False)

# Load inventory data
def load_data():
    return pd.read_csv(file_path)

# Save inventory data
def save_data(df):
    df.to_csv(file_path, index=False)

# Initialize Streamlit app
st.title('Inventory Management App')

# Load data into session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Display inventory
st.subheader('Current Inventory')
st.dataframe(st.session_state.df)

# Add new item
st.subheader('Add New Item')
item = st.text_input('Item Name')
category = st.selectbox('Category', ['Feed', 'Machines', 'Other'])
quantity = st.number_input('Quantity', min_value=0, step=1)
if st.button('Add Item'):
    new_item = pd.DataFrame([{'Item': item, 'Category': category, 'Quantity': quantity, 'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}])
    st.session_state.df = pd.concat([st.session_state.df, new_item], ignore_index=True)
    save_data(st.session_state.df)
    st.success('Item added successfully!')

# Update item quantity
st.subheader('Update Item Quantity')
item_to_update = st.selectbox('Select Item', st.session_state.df['Item'].unique())
new_quantity = st.number_input('New Quantity', min_value=0, step=1)
if st.button('Update Quantity'):
    st.session_state.df.loc[st.session_state.df['Item'] == item_to_update, 'Quantity'] = new_quantity
    st.session_state.df.loc[st.session_state.df['Item'] == item_to_update, 'Last Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_data(st.session_state.df)
    st.success('Quantity updated successfully!')

# Remove item
st.subheader('Remove Item')
item_to_remove = st.selectbox('Select Item to Remove', st.session_state.df['Item'].unique())
if st.button('Remove Item'):
    st.session_state.df = st.session_state.df[st.session_state.df['Item'] != item_to_remove]
    save_data(st.session_state.df)
    st.success('Item removed successfully!')
