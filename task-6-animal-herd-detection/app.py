from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from yolo_detector import YOLODetector
import cv2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize YOLO detector (will download models on first run)
detector = None

def init_detector():
    """Initialize the YOLO detector"""
    global detector
    if detector is None:
        print("Initializing YOLO detector...")
        detector = YOLODetector()
        print("YOLO detector ready!")
    return detector

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Handle image upload and detection"""
    try:
        # Initialize detector on first use
        init_detector()

        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only jpg, jpeg, png, gif allowed'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run detection
        annotated_image, animal_count = detector.detect(filepath)

        # Check if herd alert should be triggered
        herd_alert = animal_count >= 3

        # Convert image to base64 for display
        _, buffer = cv2.imencode('.jpg', annotated_image)
        img_base64 = base64.b64encode(buffer).decode()

        # Prepare response
        response = {
            'success': True,
            'animal_count': animal_count,
            'herd_alert': herd_alert,
            'image': f'data:image/jpeg;base64,{img_base64}',
            'message': generate_message(animal_count, herd_alert)
        }

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if file is allowed"""
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_message(count, herd_alert):
    """Generate a message based on detection results"""
    if count == 0:
        return "No animals detected in this image."
    elif count == 1:
        return f"Detected 1 animal."
    elif herd_alert:
        return f"🚨 HERD ALERT! Detected {count} animals in the image!"
    else:
        return f"Detected {count} animals."

if __name__ == '__main__':
    # Pre-initialize detector to download models
    print("Starting Animal Herd Detection Flask App...")
    init_detector()
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
