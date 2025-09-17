### **AI-Powered Image Sorter** 🤖🖼️

This project is a desktop application that automatically sorts images into folders based on their content using computer vision. The system detects objects within images and moves them to a new, categorized directory, demonstrating an automated workflow for AI-driven data management.

-----

### **Features**

  * **Intelligent Classification:** Uses a pre-trained **YOLOv8** model to detect over 80 different objects in images.
  * **Automated Sorting:** Automatically creates new folders (e.g., `cars`, `dogs`, `persons`) and moves the corresponding images into them.
  * **Modern UI:** A clean and user-friendly interface built with **`CustomTkinter`**.
  * **Real-time Feedback:** Displays a progress bar and a detailed log of which image is being sorted and its classification result.
  * **Multi-threading:** The sorting process runs in a separate thread, keeping the UI responsive and preventing it from freezing.

-----

### **Prerequisites**

Before running the application, you need to have **Python 3.8+** installed on your system.

-----

### **Installation**

1.  **Clone the repository** (if applicable) or **download the two Python files** (`app.py` and `image_sorter_backend.py`) into the same directory.

2.  **Install the required libraries** by running the following command in your terminal:

    ```bash
    pip install customtkinter opencv-python ultralytics Pillow
    ```

      * `customtkinter`: For the modern-looking UI.
      * `opencv-python`: For image processing.
      * `ultralytics`: Provides the easy-to-use YOLOv8 model for object detection.
      * `Pillow`: A library for image handling, used by `CustomTkinter`.

-----

### **How to Use**

1.  Run the application by executing the main script from your terminal:

    ```bash
    python app.py
    ```

2.  The application window will appear. Click the **"Select Folder"** button.

3.  A file dialog will open. Choose the folder containing the images you want to sort.

4.  The application will begin processing the images. You will see a progress bar update and a log of each file's sorting status.

5.  Once the process is complete, a new folder named `sorted_images` will be created in the same directory where the original images were located. This folder will contain sub-folders with names corresponding to the detected objects (e.g., `car`, `dog`, `person`).

-----

### **Project Structure**

  * `app.py`: The frontend script that creates the GUI and manages user interaction.
  * `image_sorter_backend.py`: The backend script that contains the core computer vision logic, including the object detection model and file-moving operations.
  * `sorted_images/`: This directory is automatically created by the application to store the categorized images.

-----

### **Future Enhancements**

  * **Customizable Settings:** Add an option for users to choose the output directory or adjust the object detection confidence score.
  * **Support for More Formats:** Expand the list of image extensions to include formats like `.tiff` and `.webp`.
  * **Stand-alone Executable:** Use a tool like `PyInstaller` to package the application into a single executable file, making it easy to distribute to users who don't have Python installed.
