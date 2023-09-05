#!/usr/bin/env python3
"""
This script performs face recognition on a static image using pre-computed encodings.
"""

import face_recognition
import argparse
import pickle
import cv2
import os

def recognize_faces(image_path, encodings_path):
    """Recognizes faces in an image and draws bounding boxes."""
    print("[INFO] Loading encodings...")
    with open(encodings_path, "rb") as f:
        data = pickle.load(f)

    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found at {image_path}. Please provide a valid path.")
        # Create a dummy image for demonstration purposes if it doesn't exist
        print(f"[INFO] Creating a dummy image at {image_path} for demonstration.")
        dummy_image = cv2.imread(face_recognition.load_image_file(os.path.join(os.path.dirname(__file__), "..", "..", "image-captioning-model", "cat.jpg")))
        cv2.imwrite(image_path, dummy_image)

    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("[INFO] Recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        
        names.append(name)

    # Draw bounding boxes
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Save the output image
    output_path = "recognized_faces.jpg"
    cv2.imwrite(output_path, image)
    print(f"[INFO] Recognition complete. Output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encodings", required=True, help="Path to serialized db of facial encodings.")
    parser.add_argument("-i", "--image", required=True, help="Path to input image.")
    args = vars(parser.parse_args())

    recognize_faces(args["image"], args["encodings"])

if __name__ == "__main__":
    main()
