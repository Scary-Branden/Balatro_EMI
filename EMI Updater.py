import os
import subprocess
import tkinter as tk
import requests
import threading
import sys
from tkinter import messagebox
from pathlib import Path

VERSION_NUMBER = "v1.00"
CONSOLE = 1

# Path to your icon file
icon_path = "resources/madness.ico"


# GitHub repo details
REPO_OWNER_AND_NAME = "Scary-Branden/Balatro_EMI"

if getattr(sys, 'frozen', False):  
    # If running as an executable, use the folder where the .exe is located
    base_path = os.path.dirname(sys.argv[0])  # Get the directory of the .exe
else:
    # If running as a script, use the directory where the script is located
    base_path = os.path.dirname(os.path.abspath(__file__))

# Path to store the downloaded .exe
#script_dir = Path(__file__).parent
exe_path = os.path.join(base_path, "Balatro EMI.exe")  # Change this if needed

# Get the script's directory
#script_dir = Path(__file__).parent
#exe_path = script_dir / "Balatro EMI.exe"  # Change this to the actual .exe name


def download_and_launch():
    """Download the latest version of EMI and launch it."""
    try:
        # Get latest release data from GitHub
        api_url = f"https://api.github.com/repos/{REPO_OWNER_AND_NAME}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        release_data = response.json()

        # Find the latest .exe asset
        download_url = None
        for asset in release_data.get("assets", []):
            if "EMI" in asset["name"] and "Updater" not in asset["name"] and "Installer" not in asset["name"]:
                download_url = asset["browser_download_url"]
                break

        if not download_url:
            messagebox.showerror("Error", "No .exe file found in the latest release.")
            return

        # Download the .exe
        messagebox.showinfo("Downloading", "Downloading the latest EMI update...")
        file_response = requests.get(download_url, stream=True)
        with open(exe_path, "wb") as file:
            for chunk in file_response.iter_content(chunk_size=8192):
                file.write(chunk)

        messagebox.showinfo("Download Complete", f"Update successfully downloaded to {exe_path}!")

    except Exception as e:
        messagebox.showerror("Download Failed", f"Error: {e}")
    
    # Launch the program
    if os.path.exists(exe_path):
        subprocess.Popen([str(exe_path)], shell=True)
        sys.exit(0)  # Gracefully exit the program
    else:
        messagebox.showerror("Error", "Executable not found!")

# download on startup
download_and_launch()
