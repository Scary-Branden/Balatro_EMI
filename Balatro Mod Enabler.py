import os
import subprocess
import tkinter as tk
import sys

# Define paths globally
base_file_path = "C:/Program Files (x86)/Steam/steamapps/common/Balatro/"
enabler_file = "version.dll"
game_file = "Balatro.exe"
enabler_file_path = base_file_path + enabler_file
game_file_path = base_file_path + game_file

def rename_file(*args):
    # Determine the current file path
    if os.path.exists(enabler_file_path + ".disabled"):
        file_path = enabler_file_path + ".disabled"
    else:
        file_path = enabler_file_path

    new_name = enabler_file_path + ".disabled" if option_var.get() == "disabled" else enabler_file_path

    try:
        if file_path != new_name and os.path.exists(file_path):
            os.rename(file_path, new_name)
            print(f"File renamed to: {new_name}")
    except Exception as e:
        print(f"Error: {e}")

def launch_program():
    try:
        # Launch the Balatro program
        subprocess.Popen([game_file_path], shell=True)
        # subprocess.run([game_file_path], shell=True)
        sys.exit(0)  # Gracefully exit the program
        # os._exit(0)  # Forcefully exit the program
    except Exception as e:
        print(f"Error launching program: {e}")

# Hide the console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Create the GUI
root = tk.Tk()
root.title("Balatro Mods Enabler")
root.geometry("300x175")  # Set window size to 400x200 pixels

option_var = tk.StringVar(value="enabled")
option_var.trace_add("write", rename_file)  # Automatically rename on selection

label = tk.Label(root, text="Select Version:")
label.pack(pady=10)

option1 = tk.Radiobutton(root, text="Mods Enabled", variable=option_var, value="enabled")
option1.pack()

option2 = tk.Radiobutton(root, text="Play Vanilla", variable=option_var, value="disabled")
option2.pack()

launch_button = tk.Button(root, text="Launch Balatro", command=launch_program)
launch_button.pack(pady=20)

root.mainloop()
