from flask import Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import face_recognition
import cv2
from pyfingerprint.pyfingerprint import PyFingerprint
import uuid
import logging
from werkzeug.exceptions import HTTPException
from skimage.feature import local_binary_pattern
import numpy as np

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pranjal')
mongo = PyMongo(app)

@app.route('/')
def home():
    return "Welcome to the face recognition system."

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.set_data(jsonify(success=False, message=str(e)).get_data())
    response.content_type = "application/json"
    return response, e.code

def texture_analysis_lbp(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # LBP computation
    radius = 1
    n_points = 8 * radius
    lbp = local_binary_pattern(gray_image, n_points, radius, method="uniform")
    
    # Histogram analysis can be added if needed to make decisions
    # hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))

    # Assuming a threshold for LBP (This should be experimentally determined)
    lbp_threshold = 0.5
    if np.mean(lbp) < lbp_threshold:
        return False  # Texture likely from a photo
    return True

def detect_blink():
    total_frames = 20
    blink_detected = False
    camera = cv2.VideoCapture(0)
    frame_count = 0

    while frame_count < total_frames:
        ret, frame = camera.read()
        if not ret:
            continue
        
        # Detect eyes
        eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_eyes = eyes.detectMultiScale(gray, 1.3, 5)
        
        # If no eyes are detected in several frames, it might be a blink
        if len(detected_eyes) == 0:
            blink_detected = True
            break
        
        frame_count += 1
    
    camera.release()
    return blink_detected

def motion_analysis():
    camera = cv2.VideoCapture(0)
    try:
        if not camera.isOpened():
            raise ValueError("Could not open video device")
        
        print("Please nod your head...")
        frames = []
        frame_count = 0
        
        while frame_count < 20:  # Capture 20 frames for analysis
            ret, frame = camera.read()
            if not ret:
                continue
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            frame_count += 1

        # Calculate motion between frames
        motion_detected = False
        for i in range(1, len(frames)):
            diff = cv2.absdiff(frames[i], frames[i-1])
            count = np.sum(diff > 25)  # Threshold to determine 'significant' motion
            if count > 500:  # Threshold for amount of 'significant' motion to consider
                motion_detected = True
                break

        if not motion_detected:
            raise ValueError("No significant motion detected!")
        return True
    finally:
        camera.release()

def noise_analysis(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    noise_level = np.var(gray_frame)
    if noise_level < 10:  # This threshold can be adjusted based on experimentation
        raise ValueError("Potential spoof detected based on screen noise!")
    return True

def capture_face(prompt_message=""):
    # If you have a prompt message, show it here (like "Look left").
    if prompt_message:
        print(prompt_message)

    camera = cv2.VideoCapture(0)
    try:
        if not camera.isOpened():
            raise ValueError("Could not open video device")

        ret, frame = camera.read()
        if not ret:
            raise ValueError("Could not capture frame")

        # Anti-Spoofing: Texture Analysis
        if not texture_analysis_lbp(frame):
            raise ValueError("Potential spoof detected based on texture!")

        # Anti-Spoofing: Noise Analysis
        if not noise_analysis(frame):
            raise ValueError("Potential spoof detected based on screen noise!")

        # Anti-Spoofing: Blink Detection
        if prompt_message == "Look straight" and not detect_blink():  
            raise ValueError("No blink detected, potential spoof!")

        # Anti-Spoofing: Motion Analysis
        if prompt_message == "Look straight" and not motion_analysis():
            raise ValueError("No motion detected, potential spoof!")

        rgb_frame = frame[:, :, ::-1]
        face_encodings = face_recognition.face_encodings(rgb_frame)
        
        if face_encodings:
            return face_encodings[0]
    except Exception as e:
        logging.error(f"Error in capturing face: {e}")
        raise HTTPException(description="Error in capturing face!", code=500)
    finally:
        camera.release()
        cv2.destroyAllWindows()

def capture_fingerprint():
    """Captures and returns the fingerprint encoding."""
    try:
        # Initialize the fingerprint reader
        f = PyFingerprint('COM1', 57600, 0xFFFFFFFF, 0x00000000)

        # Verify the password of the fingerprint reader
        if not f.verifyPassword():
            raise ValueError('The fingerprint sensor password is incorrect.')

        # Read the fingerprint image
        while not f.readImage():
            pass

        # Convert the image to a template and retrieve the characteristics
        f.convertImage(0x01)
        return f.downloadCharacteristics(0x01)
    except Exception as e:
        logging.error(f"Fingerprint capture failed: {e}")
        raise HTTPException(description="Error in capturing fingerprint!", code=500)

def capture_multiple_faces_encodings():
    encodings = []
    for prompt in ["Look straight", "Look left", "Look right", "Look up", "Look down"]:
        encoding = capture_face(prompt)
        if encoding:
            encodings.append(encoding.tolist())
    return encodings

def capture_multiple_fingerprints():
    fingerprints = []
    for _ in range(8):  
        fingerprint = capture_fingerprint()
        if fingerprint:
            fingerprints.append(fingerprint)
    return fingerprints

def is_face_recognized(stored_encodings, captured_encoding):
    recognized_encodings = [face_recognition.compare_faces([stored], captured_encoding) for stored in stored_encodings]
    return sum(recognized_encodings) > 2  # A majority vote mechanism

def is_fingerprint_recognized(stored_fingerprints, captured_fingerprint):
    """Compares the captured fingerprint encoding with stored encodings."""
    matched_fingerprints = [face_recognition.compare_faces([stored], captured_fingerprint) for stored in stored_fingerprints]
    return sum(matched_fingerprints) > 2  # A majority vote mechanism

@app.route('/signup', methods=['POST'])
def signup():
    face_encodings = capture_multiple_faces_encodings()
    if not face_encodings:
        raise HTTPException(description="Face encodings failed. Try again.", code=400)

    fingerprint_encodings = capture_multiple_fingerprints()
    if None in fingerprint_encodings:
        raise HTTPException(description="Fingerprint encodings failed. Try again.", code=400)

    # Using the uuid as a temporary token for the frontend to use
    temp_token = uuid.uuid4().hex

    # Storing the encodings with the temporary token. We won't store the user in the main user collection until all details are provided
    temp_user = {
        "_id": temp_token,
        "fingerprints": fingerprint_encodings,
        "face_encodings": face_encodings
    }
    mongo.db.temp_users.insert_one(temp_user)

    return jsonify(success=True, temp_token=temp_token, message='Face and fingerprints captured successfully!'), 200

@app.route('/complete_signup', methods=['POST'])
def complete_signup():
    temp_token = request.json.get("temp_token")
    name = request.json.get("name")
    region = request.json.get("region")
    role = request.json.get("role")

    if not all([temp_token, name, region, role]):
        raise HTTPException(description="Missing details. Ensure temp_token, name, region, and role are provided.", code=400)

    temp_user = mongo.db.temp_users.find_one({"_id": temp_token})
    if not temp_user:
        raise HTTPException(description="Invalid token provided.", code=400)

    # Once verified, move the data from temp_users to users collection
    user = {
        "_id": uuid.uuid4().hex,  # Assigning a final user ID
        "name": name,
        "region": region,
        "role": role,
        "fingerprints": temp_user["fingerprints"],
        "face_encodings": temp_user["face_encodings"]
    }
    try:
        mongo.db.users.insert_one(user)
        mongo.db.temp_users.delete_one({"_id": temp_token})  # Deleting the temporary data
        return jsonify(success=True, user_id=user["_id"], message='Signup completed successfully!'), 200
    except Exception as e:
        logging.error(f"Error during signup completion: {e}")
        raise HTTPException(description="Error during signup completion!", code=400)

@app.route('/login', methods=['POST'])
def login():
    captured_face_encoding = capture_face()
    if captured_face_encoding is None:
        raise HTTPException(description="No face detected, please try again!", code=400)

    users_data = list(mongo.db.users.find({}))
    if not users_data:
        raise HTTPException(description="No users in the database!", code=400)

    recognized_user = None
    for user_data in users_data:
        recognized_encodings = [face_recognition.compare_faces([stored], captured_face_encoding) for stored in user_data['face_encodings']]
        if sum(recognized_encodings) > 2:  # A majority vote mechanism
            recognized_user = user_data
            break

    if recognized_user:
        captured_fingerprint = capture_fingerprint()
        if is_fingerprint_recognized(recognized_user["fingerprints"], captured_fingerprint):
            return jsonify(success=True, message='Face and fingerprint recognized!', user_id=recognized_user['_id']), 200
            
        else:
            raise HTTPException(description="Fingerprint not recognized!", code=400)
    else:
        raise HTTPException(description="Face not recognized!", code=400)

if __name__ == "__main__":
    app.run(debug=True)