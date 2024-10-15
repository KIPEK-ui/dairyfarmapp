import streamlit as st
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

st.title("Wi-Fi Security Tester")

# User input for interface and target BSSID
interface = st.text_input("Enter your network interface (e.g., wlan0):")
bssid = st.text_input("Enter the target BSSID:")

# Toggle between WPS and WPA/WPA2
mode = st.radio("Select mode:", ("WPS", "WPA/WPA2"))

if st.button("Run"):
    if mode == "WPS":
        st.write("Running Reaver for WPS...")
        command = f"reaver -i {interface} -b {bssid} -vv"
    else:
        st.write("Running Airodump-ng for WPA/WPA2...")
        command = f"airodump-ng --bssid {bssid} {interface}"
    
    output = run_command(command)
    st.text_area("Output", output)

