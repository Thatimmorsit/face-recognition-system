'''
This script encodes faces from a directory of known people and saves the encodings.
'''
import face_recognition
import argparse
import pickle
import os

def encode_known_faces(known_faces_dir, encodings_path):
    print(f"[INFO] Encoding faces from '{known_faces_dir}'...")
    known_encodings = []
    known_names = []

    # Loop over the image paths
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        for filename in os.listdir(person_dir):
            image_path = os.path.join(person_dir, filename)
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations and encodings
            boxes = face_recognition.face_locations(image, model="hog")
            encodings = face_recognition.face_encodings(image, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(person_name)
                print(f"  + Encoded {person_name} from {filename}")

    # Save the encodings
    print(f"\n[INFO] Serializing {len(known_encodings)} encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    with open(encodings_path, "wb") as f:
        f.write(pickle.dumps(data))
    print(f"[INFO] Encodings saved to {encodings_path}")

def main():
    parser = argparse.ArgumentParser(description="Encode faces from a directory.")
    parser.add_argument("-i", "--known-faces-dir", required=True, help="Path to input directory of known faces.")
    parser.add_argument("-e", "--encodings", required=True, help="Path to save serialized db of facial encodings.")
    args = vars(parser.parse_args())

    # Create dummy directories and images for demonstration
    if not os.path.exists(args["known_faces_dir"]):
        print(f"Creating dummy directory: {args['known_faces_dir']}")
        os.makedirs(os.path.join(args["known_faces_dir"], "David_Morris"))
        # This is a placeholder; real images would be needed.
        with open(os.path.join(args["known_faces_dir"], "David_Morris", "face1.jpg"), "w") as f:
            f.write("dummy image")

    encode_known_faces(args["known_faces_dir"], args["encodings"])

if __name__ == "__main__":
    main()
