import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
from tkinter import simpledialog

# Duplicate Image Functions

def calculate_image_hash(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def find_duplicate_images(folder_path):
    seen_hashes = {}
    duplicates = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            image_path = os.path.join(folder_path, filename)
            try:
                img_hash = calculate_image_hash(image_path)
                if img_hash in seen_hashes:
                    duplicates.append((image_path, seen_hashes[img_hash]))
                else:
                    seen_hashes[img_hash] = image_path
            except Exception as e:
                print(f"Error hashing {image_path}: {e}")

    return duplicates

def select_folder_for_duplicates():
    folder = filedialog.askdirectory()
    if folder:
        duplicates = find_duplicate_images(folder)
        if not duplicates:
            messagebox.showinfo("No Duplicates", "No duplicate images found.")
        else:
            show_duplicate_images(duplicates)

def show_duplicate_images(duplicates):
    viewer = tk.Toplevel(root)
    viewer.title("Duplicate Image Remover")
    viewer.geometry("900x700")
    viewer.configure(bg="black")

    current_index = [0]

    def update_view():
        if not duplicates:
            messagebox.showinfo("Done", "All duplicate images handled.")
            viewer.destroy()
            return

        img1_path, img2_path = duplicates[current_index[0]]
        img1 = Image.open(img1_path).resize((400, 300))
        img2 = Image.open(img2_path).resize((400, 300))
        img1tk = ImageTk.PhotoImage(img1)
        img2tk = ImageTk.PhotoImage(img2)

        img1_label.config(image=img1tk)
        img1_label.image = img1tk
        img2_label.config(image=img2tk)
        img2_label.image = img2tk
        detail_label.config(text=f"Duplicate {current_index[0]+1} of {len(duplicates)}")

    def delete_duplicate():
        dup_path, _ = duplicates.pop(current_index[0])
        os.remove(dup_path)
        if current_index[0] >= len(duplicates):
            current_index[0] = max(0, len(duplicates) - 1)
        update_view()

    def next_pair():
        if current_index[0] < len(duplicates) - 1:
            current_index[0] += 1
            update_view()

    def prev_pair():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_view()

    img_frame = ttk.Frame(viewer)
    img_frame.pack()

    img1_label = tk.Label(img_frame, bg="black")
    img1_label.grid(row=0, column=0, padx=10, pady=10)

    img2_label = tk.Label(img_frame, bg="black")
    img2_label.grid(row=0, column=1, padx=10, pady=10)

    detail_label = tk.Label(viewer, font=("Arial", 12, "italic"), fg="white", bg="black")
    detail_label.pack(pady=10)

    btn_frame = ttk.Frame(viewer)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="⬅ Prev", command=prev_pair, style="White.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Delete Duplicate 🗑", command=delete_duplicate, style="White.TButton").grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Next ➡", command=next_pair, style="White.TButton").grid(row=0, column=2, padx=10)

    update_view()

# Blurry Image Functions

def calculate_blurriness(image_path):
    image = Image.open(image_path)
    image = image.convert("L")
    image = image.resize((100, 100))
    pixels = list(image.getdata())
    return sum(pixels) / len(pixels)

def find_blurry_images(folder_path, threshold=100):
    blurry_images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            image_path = os.path.join(folder_path, filename)
            try:
                blur_score = calculate_blurriness(image_path)
                if blur_score < threshold:
                    blurry_images.append(image_path)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    return blurry_images

def select_folder_for_blurry():
    folder = filedialog.askdirectory()
    if folder:
        blurry_images = find_blurry_images(folder)
        if not blurry_images:
            messagebox.showinfo("No Blurry Images", "No blurry images found.")
        else:
            show_blurry_images(blurry_images)

def show_blurry_images(blurry_images):
    viewer = tk.Toplevel(root)
    viewer.title("Blurry Image Remover")
    viewer.geometry("900x700")
    viewer.configure(bg="black")

    current_index = [0]

    def update_view():
        if not blurry_images:
            messagebox.showinfo("Done", "All blurry images handled.")
            viewer.destroy()
            return

        img_path = blurry_images[current_index[0]]
        img = Image.open(img_path).resize((400, 300))
        imgtk = ImageTk.PhotoImage(img)
        img_label.config(image=imgtk)
        img_label.image = imgtk
        detail_label.config(text=f"Blurry {current_index[0]+1} of {len(blurry_images)}")

    def delete_blurry():
        img_path = blurry_images.pop(current_index[0])
        os.remove(img_path)
        if current_index[0] >= len(blurry_images):
            current_index[0] = max(0, len(blurry_images) - 1)
        update_view()

    def next_image():
        if current_index[0] < len(blurry_images) - 1:
            current_index[0] += 1
            update_view()

    def prev_image():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_view()

    img_frame = ttk.Frame(viewer)
    img_frame.pack()

    img_label = tk.Label(img_frame, bg="black")
    img_label.grid(row=0, column=0, padx=10, pady=10)

    detail_label = tk.Label(viewer, font=("Arial", 12, "italic"), fg="white", bg="black")
    detail_label.pack(pady=10)

    btn_frame = ttk.Frame(viewer)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="⬅ Prev", command=prev_image, style="White.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Delete Blurry 🗑", command=delete_blurry, style="White.TButton").grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Next ➡", command=next_image, style="White.TButton").grid(row=0, column=2, padx=10)

    update_view()

# Face Cropping Function

def crop_faces_from_image(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cropped_faces = []

    for (x, y, w, h) in faces:
        cropped_face = image[y:y+h, x:x+w]
        cropped_faces.append(cropped_face)

    return cropped_faces

def select_image_for_face_crop():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        cropped_faces = crop_faces_from_image(image_path)
        if cropped_faces:
            show_cropped_faces(cropped_faces)
        else:
            messagebox.showinfo("No Faces Detected", "No faces were detected in the image.")

def show_cropped_faces(faces):
    viewer = tk.Toplevel(root)
    viewer.title("Face Cropper")
    viewer.geometry("500x300")
    viewer.configure(bg="black")

    current_index = [0]

    def update_view():
        if not faces:
            messagebox.showinfo("Done", "All faces cropped.")
            viewer.destroy()
            return

        img = Image.fromarray(faces[current_index[0]])
        img = img.resize((400, 300))
        imgtk = ImageTk.PhotoImage(img)
        img_label.config(image=imgtk)
        img_label.image = imgtk
        detail_label.config(text=f"Face {current_index[0]+1} of {len(faces)}")

    def save_cropped():
        face = faces[current_index[0]]
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image Files", "*.jpg;*.png")])
        if save_path:
            cv2.imwrite(save_path, face)
            next_face()

    def next_face():
        if current_index[0] < len(faces) - 1:
            current_index[0] += 1
            update_view()

    def prev_face():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_view()

    img_frame = ttk.Frame(viewer)
    img_frame.pack()

    img_label = tk.Label(img_frame, bg="black")
    img_label.grid(row=0, column=0, padx=10, pady=10)

    detail_label = tk.Label(viewer, font=("Arial", 12, "italic"), fg="white", bg="black")
    detail_label.pack(pady=10)

    btn_frame = ttk.Frame(viewer)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="⬅ Prev", command=prev_face, style="White.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Save Face 🗸", command=save_cropped, style="White.TButton").grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Next ➡", command=next_face, style="White.TButton").grid(row=0, column=2, padx=10)

    update_view()

# Main Application

root = tk.Tk()
root.title("Smart Image Toolkit")
root.geometry("600x500")
root.configure(bg="black")

style = ttk.Style()
style.theme_use("clam")
style.configure("White.TButton", foreground="black", background="white", font=("Helvetica", 12, "bold"))
style.map("White.TButton",
          foreground=[("pressed", "white"), ("active", "black")],
          background=[("pressed", "gray"), ("active", "lightgray")])

title_label = tk.Label(root,
                       text="📸 Smart Image Toolkit",
                       font=("Helvetica", 22, "bold"),
                       fg="white", bg="black")
title_label.pack(pady=30)

button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Buttons
ttk.Button(button_frame, text="🧠 Remove Duplicate Images", command=select_folder_for_duplicates, style="White.TButton").pack(pady=15)
ttk.Button(button_frame, text="🌫 Remove Blurry Images", command=select_folder_for_blurry, style="White.TButton").pack(pady=15)
ttk.Button(button_frame, text="👤 Crop Faces from Image", command=select_image_for_face_crop, style="White.TButton").pack(pady=15)

footer_label = tk.Label(root,
                        text="Made with ❤️ for Clean Image Management",
                        font=("Helvetica", 10, "italic"),
                        fg="gray", bg="black")
footer_label.pack(side="bottom", pady=20)

root.mainloop()