import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk  # Import for handling images
import subprocess
import threading
import time

class ModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Model Chat")
        self.root.geometry("600x650")
        self.root.resizable(True, True)

        # Set a modern style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        self.style.configure("TButton", font=("Arial", 12), padding=6)
        self.style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        self.style.configure("TOptionMenu", font=("Arial", 12))
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TText", padding=5)
        self.style.configure("TEntry", padding=5)

        # Configure specific button styles
        self.style.configure("Success.TButton", foreground="white", background="#28a745")
        self.style.configure("Primary.TButton", foreground="white", background="#007bff")
        self.style.configure("Danger.TButton", foreground="white", background="#dc3545")

        # Handle icon for PyInstaller packaging using ImageTk
        if getattr(sys, 'frozen', False):
            # If running as a bundled executable, find the icon inside the bundled directory
            icon_path = os.path.join(sys._MEIPASS, "chatbot.ico")
        else:
            # If running as a script, use the local path
            icon_path = "chatbot.ico"

        try:
            # Use ImageTk to open the icon and set it
            icon_image = Image.open(icon_path)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, self.icon_photo)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {str(e)}")
            root.quit()
            return

        # Main container frame
        self.container = ttk.Frame(root, padding=10, style="TFrame")
        self.container.pack(fill=tk.BOTH, expand=True)

        # Top Frame for model selection
        self.top_frame = ttk.Frame(self.container, style="TFrame")
        self.top_frame.pack(pady=10, fill=tk.X)

        self.model_label = ttk.Label(self.top_frame, text="Select Model:", style="TLabel")
        self.model_label.pack(side=tk.LEFT, padx=5)

        self.models = self.get_installed_models()
        if not self.models:
            messagebox.showerror("Error", "No models found. Please install models and try again.")
            root.quit()
            return

        self.model_var = tk.StringVar(value=self.models[0])  # Default to the first model
        self.model_dropdown = ttk.OptionMenu(self.top_frame, self.model_var, self.models[0], *self.models)
        self.model_dropdown.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.container, height=20, width=80, font=("Arial", 11), wrap=tk.WORD)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED, bg="#fefefe")

        # Input and Button Frame
        self.input_frame = ttk.Frame(self.container, style="TFrame")
        self.input_frame.pack(pady=10, fill=tk.X)

        self.input_text = tk.Text(self.input_frame, height=2, width=70, font=("Arial", 11), wrap=tk.WORD, relief=tk.GROOVE, bd=2)
        self.input_text.pack(side=tk.LEFT, pady=5, padx=5, expand=True, fill=tk.X)

        # Save and Quit buttons in the same line at the bottom
        self.bottom_frame = ttk.Frame(self.container, style="TFrame")
        self.bottom_frame.pack(pady=10, fill=tk.X)

        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_to_model, style="Success.TButton")
        self.save_button = ttk.Button(self.bottom_frame, text="Save", command=self.save_chat, style="Primary.TButton")
        self.quit_button = ttk.Button(self.bottom_frame, text="Quit", command=root.quit, style="Danger.TButton")
        
        self.send_button.pack(side=tk.RIGHT, padx=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.quit_button.pack(side=tk.LEFT, padx=5)

    def get_installed_models(self):
        """Fetch the list of installed models using 'ollama list'."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr.strip())
            models = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
            return models
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve models: {str(e)}")
            return []

    def send_to_model(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        selected_model = self.model_var.get()

        if not user_input:
            self.add_output("Please enter some text.", "user")
            return

        self.input_text.delete("1.0", tk.END)
        self.add_output(user_input, "user")
        self.add_output(f"Using Model: {selected_model}", "system")

        # Disable the button while processing
        self.send_button.config(state=tk.DISABLED)

        # Run model in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.run_model_command, args=(user_input, selected_model)).start()

    def run_model_command(self, user_input, model_name):
        try:
            command = ["ollama", "run", model_name]
            
            # If on Windows, use creationflags to hide the terminal window
            if os.name == 'nt':  # Windows
                creation_flags = subprocess.CREATE_NO_WINDOW
            else:  # For other OS like Linux and macOS
                creation_flags = 0
            
            process = subprocess.Popen(
                command, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                encoding="utf-8",
                creationflags=creation_flags
            )
            stdout, stderr = process.communicate(input=user_input)

            response = stdout.strip()
            if response:
                self.add_output(response, "model")
            else:
                self.add_output("Model did not return any output.", "system")
        except Exception as e:
            self.add_output(f"Error: {str(e)}", "system")
        finally:
            self.send_button.config(state=tk.NORMAL)

    def add_output(self, text, sender):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S", time.localtime())

        # Add margin space around tags
        if sender == "user":
            self.chat_display.insert(tk.END, f"{timestamp} You: {text}\n", "user")
        elif sender == "model":
            self.chat_display.insert(tk.END, f"{timestamp} Model: {text}\n", "model")
        else:
            self.chat_display.insert(tk.END, f"{timestamp} System: {text}\n", "system")

        # Adjust tag configurations for background and padding
        self.chat_display.tag_config("user", background="#E6F3FF", foreground="#000000")
        self.chat_display.tag_config("model", background="#F0FFF0", foreground="#000000")
        self.chat_display.tag_config("system", background="#FFF0F5", foreground="#000000")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def save_chat(self):
        """Function to save the chat to a file (simple placeholder)."""
        with open("chat_log.txt", "w") as file:
            file.write(self.chat_display.get("1.0", tk.END))

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModelApp(root)
    root.mainloop()
