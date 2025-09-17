import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from image_sorter_backend import classify_and_sort_image # Ensure this file is in the same directory

# Set a color theme for the UI
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class ImageSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("AI-Powered Image Sorter")
        self.geometry("500x500")
        self.resizable(False, False)

        # UI Elements
        self.title_label = ctk.CTkLabel(self, text="AI-Powered Image Sorter", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        self.instruction_label = ctk.CTkLabel(self, text="Select a folder to automatically sort images by content.", font=ctk.CTkFont(size=14))
        self.instruction_label.pack()
        
        self.select_button = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=10)

        # Status and Log
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 5))
        
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.log_textbox = ctk.CTkTextbox(self.log_frame, wrap="word", state="disabled", corner_radius=10)
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder with images")
        if folder_path:
            self.status_label.configure(text=f"Status: Processing images in {os.path.basename(folder_path)}...")
            self.select_button.configure(state="disabled")
            self.progress_bar.set(0)
            self.log_textbox.configure(state="normal")
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.insert("end", "Starting sorting process...\n")
            self.log_textbox.configure(state="disabled")
            
            # Start the sorting process in a separate thread
            self.sorting_thread = threading.Thread(target=self.start_sorting, args=(folder_path,))
            self.sorting_thread.start()
            
    def start_sorting(self, folder_path):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
        
        if not image_files:
            messagebox.showinfo("Info", "No images found in the selected folder.")
            self.update_ui_on_finish("Status: No images found.", "normal")
            return

        total_images = len(image_files)
        
        for i, image_path in enumerate(image_files):
            # Update status and progress bar
            self.status_label.configure(text=f"Status: Sorting {i+1}/{total_images}")
            progress_value = (i + 1) / total_images
            self.progress_bar.set(progress_value)
            
            # Call the backend function to classify and sort the image
            result = classify_and_sort_image(image_path)
            
            # Log the result
            log_message = f"[{i+1}/{total_images}] {os.path.basename(image_path)}: {result}\n"
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", log_message)
            self.log_textbox.see("end") # Auto-scroll to the bottom
            self.log_textbox.configure(state="disabled")

            # Force UI update
            self.update() 
            
        messagebox.showinfo("Success", "All images have been sorted successfully!")
        self.update_ui_on_finish("Status: Sorting complete.", "normal")

    def update_ui_on_finish(self, status_text, button_state):
        self.status_label.configure(text=status_text)
        self.select_button.configure(state=button_state)
        self.progress_bar.set(1)

if __name__ == "__main__":
    app = ImageSorterApp()
    app.mainloop()