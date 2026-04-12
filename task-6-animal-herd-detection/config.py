# config.py - Configuration file for Animal Herd Detection

# Flask Configuration
FLASK_PORT = 5000
FLASK_DEBUG = True
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# YOLO Detection Configuration
YOLO_MODEL_DIR = 'yolo_models'
YOLO_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detection (0.0-1.0)
YOLO_NMS_THRESHOLD = 0.4  # Non-Maximum Suppression threshold

# Herd Detection Configuration
HERD_ALERT_THRESHOLD = 3  # Minimum animals to trigger herd alert
ALLOW_UPLOAD_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Animal Classes to Detect
ANIMAL_CLASSES = {
    'cow',      # Cattle
    'sheep',    # Sheep/Lamb
    'horse',    # Horses
    'dog',      # Dogs
    'cat',      # Cats
    'bird',     # Birds
    'elephant', # Elephants
    'zebra',    # Zebras
    'giraffe',  # Giraffes
    'bear'      # Bears
}

# Upload Configuration
UPLOAD_FOLDER = 'uploads'
TEMP_IMAGE_RETENTION = 60  # Seconds to keep temp images

# Display Configuration
SHOW_CONFIDENCE_SCORES = True
BOUNDING_BOX_COLOR = (0, 255, 0)  # BGR format: Green
BOUNDING_BOX_THICKNESS = 2
FONT_SCALE = 0.6
FONT_THICKNESS = 2
