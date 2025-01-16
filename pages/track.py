import streamlit as st
import subprocess
import time
import requests
import pandas as pd
from pyngrok import ngrok

st.set_page_config(page_title="Track Violators", layout="wide",  page_icon = 'logo.png')
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 0px;
            max-width: 225px;
        }
    </style>
""", unsafe_allow_html=True)
# Sidebar: Image insertion and Cyber Official Guide
with st.sidebar:
    # Insert your image here by replacing 'path_to_image.png' with the actual image file path or URL.
    st.image("aibot.png", caption="Cyber Tracking Dashboard", width=200)
    st.markdown("""
    ## Cyber Guide

    **Hello, Cyber Defender!**

    - **Track:** Start Flask and use the Ngrok link as a hyperlink sent to ther user.
    - **Monitor:** Check live logs for their location.
    - **Act:** Know if they use VPN or proxy according to fluctuating locations.

    **Note:** Use responsibly.
    """)


# Function to start Flask in background with unbuffered output
def start_flask():
    return subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1  # Unbuffered output for real-time logs
    )

# Function to fetch logs in real-time
def get_logs(process):
    logs = []
    while True:
        line = process.stdout.readline()
        if not line:
            continue  # Wait for new logs
        line = line.strip()
        logs.append(line)
        if len(logs) > 10:  # Keep only the last 10 log entries
            logs.pop(0)
        yield logs

# Streamlit UI
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel&display=swap" rel="stylesheet">
<h1 style="font-family: 'Cinzel', serif;">Flask Tracking App with Ngrok</h1>
""", unsafe_allow_html=True)

# Start Flask App
st.subheader("Starting Flask Server... ⏳")
flask_process = start_flask()
time.sleep(3)  # Give Flask time to start

# Start ngrok tunnel
st.subheader("Starting Ngrok Tunnel... 🚀")
ngrok_tunnel = ngrok.connect(5000)
tracking_url = f"{ngrok_tunnel.public_url}/track?user_id=123"

# Display the generated tracking link
st.success(f"Generated Tracking Link: [Click here]({tracking_url})")
st.code(tracking_url, language="markdown")

# Capture and display Flask logs
st.subheader("📜 Flask Logs")
log_container = st.empty()

# Continuously update logs
for logs in get_logs(flask_process):
    if logs:
        df_logs = pd.DataFrame({"Logs": logs})
        log_container.table(df_logs)

# Stop Flask on app exit
st.warning("To stop Flask and Ngrok, close this Streamlit app.")

