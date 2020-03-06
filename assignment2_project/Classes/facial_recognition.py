"""Creates FacialRecognition class"""
import pickle
import argparse
import time
import os
from Classes.socket_connection import SocketConnection
# Disable packages not found locally linting error
# pylint: disable=E0401
import cv2
import imutils
from imutils import paths
from imutils.video import VideoStream
import face_recognition

class FacialRecognition:
    """Handles facial recognition features"""
    def __init__(self):
        self.__socket = SocketConnection()

    # pylint: disable=R0914
    def register_face(self, user):
        """
        Registers a new user's face

        Parameters:
            name (str) = Username of the logged in User

        Returns:
            Associates the logged in user with the photos that will be taken.
        """
        name = user
        folder = "./user_faces/{}".format(name)

        if not os.path.exists(folder):
            os.makedirs(folder)

        cam = cv2.VideoCapture(0)
        # Set video width
        cam.set(3, 640)
        # Set video height
        cam.set(4, 480)
        # Get the pre-built classifier that had been trained on 3 million faces
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        print("\nPlease take at least 5 photos of yourself")

        img_counter = 0
        while img_counter < 5:
            key = input("\nPress q to quit or ENTER to take a picture: ")
            if key == "q":
                break

            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            # Disable linting warning on checking if empty
            # pylint: disable=C1801
            if len(faces) == 0:
                print("No face detected, please try again")
                continue

            # Disable snake case variable name linting warning
            # pylint: disable=C0103
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img_name = "{}/{:04}.jpg".format(folder, img_counter)
                cv2.imwrite(img_name, frame[y : y + h, x : x + w])
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()
        self.face_encoding()


    @staticmethod
    def face_encoding():
        """Encodes facial data into pickle file"""
        # construct the argument parser and parse the arguments
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            "-i",
            "--user_faces",
            default="user_faces",
            help="path to input directory of faces + images"
        )
        argument_parser.add_argument(
            "-e", "--encodings",
            default="encodings.pickle",
            help="path to serialized db of facial encodings"
        )
        argument_parser.add_argument(
            "-d",
            "--detection-method",
            type=str,
            default="hog",
            help="face detection model to use: either `hog` or `cnn`"
        )
        args = vars(argument_parser.parse_args())

        # grab the paths to the input images in our face folder (user_faces)
        print("\n[INFO] Encoding faces into database! Please be patient.")
        image_paths = list(paths.list_images(args["user_faces"]))
        known_encodings = []
        known_names = []

        # loop over the image paths
        for (i, image_path) in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
            name = image_path.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model=args["detection_method"])

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                known_encodings.append(encoding)
                known_names.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        print("Face registration complete!\n")
        data = {"encodings": known_encodings, "names": known_names}

        with open(args["encodings"], "wb") as file:
            file.write(pickle.dumps(data))

    @staticmethod
    def face_scan():
        """Captures and recognises face"""
        # construct the argument parser and parse the arguments
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            "-e",
            "--encodings",
            default="encodings.pickle",
            help="path to serialized db of facial encodings"
        )
        argument_parser.add_argument(
            "-r",
            "--resolution",
            type=int,
            default=240,
            help="Resolution of the video feed"
        )
        argument_parser.add_argument(
            "-d",
            "--detection-method",
            type=str,
            default="hog",
            help="face detection model to use: either `hog` or `cnn`"
        )
        args = vars(argument_parser.parse_args())
        print("[INFO] loading encodings...")
        data = pickle.loads(open(args["encodings"], "rb").read())
        print("[INFO] starting video stream...")
        video_stream = VideoStream(src=0).start()
        time.sleep(2.0)
        while True:
            frame = video_stream.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=args["resolution"])
            boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"
                if True in matches:
                    matched_index = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matched_index:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                names.append(name)
            for name in names:
                print("Person found: {}".format(name))
                video_stream.stop()
                return name
