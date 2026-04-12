# 🦁 Animal Herd Detection Flask Application

A web-based animal herd detection system using YOLOv3 object detection, OpenCV, and Flask. Upload an image to detect animals and see if a herd alert should be triggered (3+ animals detected).

## Features

- ✅ **YOLOv3 Object Detection**: Detects 10 animal classes (cow, sheep, horse, dog, cat, bird, elephant, zebra, giraffe, bear)
- ✅ **Real-time Processing**: Instant detection results with annotated images
- ✅ **Herd Alert System**: Automatic alert when 3+ animals are detected
- ✅ **Auto-Download Models**: YOLOv3 weights, config, and COCO names download automatically on first run
- ✅ **Beautiful Web Interface**: Modern, responsive HTML frontend with drag-and-drop upload
- ✅ **Bounding Box Annotations**: Labeled boxes with confidence scores on detected animals
- ✅ **Animal Counting**: Accurate count of detected animals in the image

## Tech Stack

- **Backend**: Python, Flask
- **ML Framework**: OpenCV, YOLOv3
- **Frontend**: HTML5, CSS3, JavaScript
- **Object Detection**: YOLOv3 (COCO dataset)

## Project Structure

```
animal-herd-detection/
├── app.py                 # Flask application (main entry point)
├── yolo_detector.py       # YOLOv3 detection module
├── requirements.txt       # Python dependencies
├── yolo_models/           # Downloaded YOLO models (auto-created)
├── uploads/               # Temporary upload storage (auto-created)
├── templates/
│   └── index.html         # Web interface
└── static/
    └── css/
        └── style.css      # Styling
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

**First run will automatically download:**
- `yolov3.weights` (~237 MB) - Pre-trained YOLOv3 weights
- `yolov3.cfg` - Network architecture configuration
- `coco.names` - COCO dataset class names

This may take 5-10 minutes depending on your internet speed. Subsequent runs will use cached models.

### 3. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Upload an Image**
   - Click the upload area or drag & drop an image (JPG, JPEG, PNG, GIF)
   - Maximum file size: 16 MB

2. **Detect Animals**
   - Click the "Detect Animals" button
   - Wait for processing (usually 5-15 seconds depending on image size)

3. **View Results**
   - See the annotated image with bounding boxes and labels
   - View the total animal count
   - 🚨 **HERD ALERT** displays if 3+ animals detected
   - Each detected animal shows confidence score

4. **Upload Another**
   - Click "Upload Another Image" to process a new image

## Animal Classes Detected

The system detects these animal classes from the COCO dataset:
- 🐄 Cow
- 🐑 Sheep
- 🐴 Horse
- 🐕 Dog
- 🐈 Cat
- 🐦 Bird
- 🐘 Elephant
- 🦓 Zebra
- 🦒 Giraffe
- 🐻 Bear

## Configuration & Customization

### Adjust Detection Confidence Threshold

Edit `yolo_detector.py`, line 53:
```python
if confidence > 0.5:  # Change 0.5 to your desired threshold (0.0-1.0)
```

### Change Herd Alert Threshold

Edit `app.py`, line 54:
```python
herd_alert = animal_count >= 3  # Change 3 to desired minimum count
```

### Modify Animal Classes

Edit `yolo_detector.py`, line 10:
```python
ANIMAL_CLASSES = {
    'cow', 'sheep', 'horse', 'dog', 'cat', 'bird',
    'elephant', 'zebra', 'giraffe', 'bear'  # Add/remove classes here
}
```

### Change Flask Port

Edit `app.py`, line 82:
```python
app.run(debug=True, port=5000)  # Change 5000 to your desired port
```

## Performance Tips

- Use images with good lighting and clear animal subjects for best results
- Larger/clearer animals tend to get detected more reliably
- The first detection takes longer as YOLO models load into memory
- Subsequent detections are faster (model stays in memory)

## Troubleshooting

### "Connection refused" or "Cannot connect to localhost:5000"
- Ensure Flask is running: `python app.py`
- Check if port 5000 is available on your system
- Try a different port: modify last line in `app.py`

### "Out of Memory" error
- YOLOv3 requires ~2 GB RAM during detection
- Close other applications
- Reduce image size before uploading

### Model download fails
- Check your internet connection
- Ensure firewall allows urllib connections
- Try running again (if temporary network issue)
- Manual download alternative: download files from:
  - Weights: https://pjreddie.com/media/files/yolov3.weights
  - Config: https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
  - Names: https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
  - Place in `yolo_models/` folder

### Image not being detected
- Ensure image format is supported (JPG, JPEG, PNG, GIF)
- Check file size is under 16 MB
- Verify animals are clearly visible in the image
- Try adjusting confidence threshold in code

## System Requirements

- **Python**: 3.7 or higher
- **RAM**: Minimum 2 GB (for YOLOv3 model)
- **Storage**: ~250 MB for YOLOv3 weights
- **Processor**: Any modern CPU (GPU recommended for faster inference)
- **OS**: Windows, macOS, or Linux

## Performance Notes

- **Model Download**: 5-10 minutes (first run only)
- **First Inference**: 20-40 seconds (model loading)
- **Subsequent Inferences**: 5-15 seconds per image
- **Network Processing**: 2-5 MB/s upload speed required for 16 MB images

## Note on YOLOv3

The application uses YOLOv3, a fast and accurate object detection model trained on the COCO dataset. It's pre-trained on 80 object classes, but this app filters to show only animal classes for herd detection.

For alternatives, consider:
- **YOLOv5**: Faster and more accurate (requires PyTorch)
- **YOLOv8**: Latest version (requires ultralytics library)
- **Custom models**: Train on specific animal datasets for higher accuracy

## License

This project uses YOLOv3, which is available under the Unlicense. COCO dataset is under Creative Commons Attribution 4.0 License.

## Disclaimer

This system is for demonstration and educational purposes. Accuracy depends on image quality and animal visibility. Always verify results visually before using for any critical applications.

---

Built with ❤️ for animal detection and herd monitoring.
