# smart-image-toolkit
Smart Image Toolkit is a Python-based GUI application that helps users automatically detect and manage blurry, duplicate, and face-croppable images from a folder. Built with Tkinter, OpenCV, and PIL, this tool streamlines photo organization by identifying and allowing users to delete unwanted or low-quality images.

Features
📷 Blur Detection – Automatically detects blurry images using Laplacian variance.

📁 Duplicate Detection – Identifies duplicate images using hashing.

😶 Face Cropper – Crops faces from images and saves them separately.

🖼️ Image Viewer – Preview blurry/duplicate images before deletion.

🧹 Clean Interface – Simple GUI with folder selection, threshold input, and result summary.

Technologies Used
Python 3
Tkinter
OpenCV (cv2)
Pillow (PIL)
NumPy
os / shutil

Installation
Clone the repository:
bash
Copy
Edit
git clone https://github.com/Ritikapuri23/smart-image-toolkit.git
cd smart-image-toolkit
Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist, manually install:
bash
Copy
Edit
pip install opencv-python pillow numpy
How to Use
Run the main script:
bash
Copy
Edit
python smart_image_toolkit.py
Enter a blur threshold (e.g., 100).

Click on "Select Folder and Process".

The app will:
Detect and display blurry images in a slideshow.
Detect duplicate images.
Crop faces (if feature is enabled).
Use navigation and delete buttons to manage images
