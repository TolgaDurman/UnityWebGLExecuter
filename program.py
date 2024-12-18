import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import webbrowser
import psutil  # For stopping the server process

# Global variables
folder_path = None
server_process = None  # To store the server process

# Function to select folder
def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)

# Function to play/start the server
def play():
    global server_process
    port = int_var.get()

    if folder_path:
        # Kill any existing server processes
        stop_server()

        # Get the directory of the running script/executable
        current_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(current_dir, "SimpleWebServer.exe")

        # Start the server process
        server_process = subprocess.Popen([server_path, folder_path, str(port)])
        webbrowser.open(f'http://localhost:{port}')
        status_label.config(text="Server is running...", fg="green")

        # Update button states
        play_button.config(text="Restart", command=play)
        stop_button.config(state=tk.NORMAL)

# Function to stop the server
def stop_server():
    global server_process

    if server_process and server_process.poll() is None:
        try:
            # Kill the process using psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if "SimpleWebServer.exe" in proc.info['name']:
                    proc.terminate()
            server_process.terminate()
        except Exception as e:
            print(f"Error stopping server: {e}")
    server_process = None
    status_label.config(text="Server stopped.", fg="red")
    stop_button.config(state=tk.DISABLED)
    play_button.config(text="Play", command=play)

# Function to clean up when closing the app
def on_close():
    stop_server()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Unity WebGL Player")
root.geometry("400x300")
root.configure(bg="#f0f0f0")
root.protocol("WM_DELETE_WINDOW", on_close)

# Select Folder Button
select_folder_button = tk.Button(root, text="Select Folder", command=select_folder,
                                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
select_folder_button.pack(pady=10)

# Folder Path Label
folder_path_label = tk.Label(root, text="No folder selected", bg="#f0f0f0", font=("Arial", 10))
folder_path_label.pack(pady=10)

# Port Frame
port_frame = tk.Frame(root, bg="#f0f0f0")
port_frame.pack(pady=10)

# Port Label and Entry
port_label = tk.Label(port_frame, text="Port:", bg="#f0f0f0", font=("Arial", 12))
port_label.pack(side=tk.LEFT)

int_var = tk.IntVar(value=8000)
int_entry = tk.Entry(port_frame, textvariable=int_var, font=("Arial", 12))
int_entry.pack(side=tk.LEFT)

# Play Button
play_button = tk.Button(root, text="Play", command=play, bg="#2196F3", fg="white",
                        font=("Arial", 12, "bold"))
play_button.pack(pady=10)

# Stop Button (Initially Disabled)
stop_button = tk.Button(root, text="Stop", command=stop_server, bg="#F44336", fg="white",
                        font=("Arial", 12, "bold"), state=tk.DISABLED)
stop_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Server not running.", bg="#f0f0f0", fg="gray", font=("Arial", 10))
status_label.pack(pady=10)

# Run the application
root.mainloop()
