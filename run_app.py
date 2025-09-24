import subprocess
import time
import webview
import requests

STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"

# Step 1: Start Streamlit in background
process = subprocess.Popen(
    ["streamlit", "run", "app.py", "--server.headless", "true", f"--server.port={STREAMLIT_PORT}"],
    shell=True
)

# Step 2: Wait until Streamlit is ready
print("Waiting for Streamlit server to start...")
while True:
    try:
        res = requests.get(STREAMLIT_URL)
        if res.status_code == 200:
            break
    except requests.exceptions.ConnectionError:
        pass
    time.sleep(0.5)

print("Streamlit is ready! Opening webview...")

# Step 3: Open in pywebview
webview.create_window("Excel Sheet Selector", STREAMLIT_URL)
webview.start()

# Optional: terminate Streamlit when webview closes
process.terminate()
