import os
import shutil
from ultralytics import YOLO
from collections import Counter
from PIL import Image

# Load a pre-trained YOLO model
try:
    # Use a smaller, faster model (n for nano)
    model = YOLO('yolov8n.pt') 
    print("YOLOv8n model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    # Exit or handle the error gracefully
    model = None

def classify_and_sort_image(image_path, base_folder='sorted_images'):
    """
    Classifies an image and sorts it into a folder based on the detected objects.
    
    Args:
        image_path (str): The path to the image file.
        base_folder (str): The root directory for sorted images.
        
    Returns:
        str: A status message indicating the result of the classification.
    """
    if not model:
        return "Error: YOLO model not loaded."

    # Validate image path
    if not os.path.isfile(image_path):
        return f"Error: Image not found at {image_path}"
    
    # Create the base sorting directory if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    try:
        # Use a temporary file to ensure the image format is compatible with YOLO
        temp_img_path = "temp_yolo_input.jpg"
        img = Image.open(image_path)
        img.save(temp_img_path)
        
        # Perform object detection with a minimum confidence score of 0.5
        results = model.predict(temp_img_path, save=False, conf=0.5)

        # Get the names of the detected objects
        detected_objects = []
        for r in results:
            for c in r.boxes.cls:
                detected_objects.append(model.names[int(c)])

        if detected_objects:
            # Get the most common detected object to name the folder
            most_common_object = Counter(detected_objects).most_common(1)[0][0]
            target_folder = os.path.join(base_folder, most_common_object)
            
            # Create the category folder if it doesn't exist
            os.makedirs(target_folder, exist_ok=True)
            
            # Move the image to the new folder
            shutil.move(image_path, os.path.join(target_folder, os.path.basename(image_path)))
            
            return f"Classified and moved to '{most_common_object}'"
        else:
            # If no objects are detected, move to an 'uncategorized' folder
            target_folder = os.path.join(base_folder, 'uncategorized')
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(image_path, os.path.join(target_folder, os.path.basename(image_path)))
            return "No objects detected, moved to 'uncategorized'"
            
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {e}"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

if __name__ == '__main__':
    # This block is for testing the backend logic independently
    # Create some dummy image files for demonstration
    dummy_folder = "test_images"
    if not os.path.exists(dummy_folder):
        os.makedirs(dummy_folder)
        with open(os.path.join(dummy_folder, "test_dog.jpg"), 'w') as f:
            f.write("dummy")
        with open(os.path.join(dummy_folder, "test_car.jpg"), 'w') as f:
            f.write("dummy")
    
    print(f"Testing the backend with images in '{dummy_folder}'...")
    for filename in os.listdir(dummy_folder):
        filepath = os.path.join(dummy_folder, filename)
        if os.path.isfile(filepath):
            print(f"Processing {filename}: {classify_and_sort_image(filepath)}")