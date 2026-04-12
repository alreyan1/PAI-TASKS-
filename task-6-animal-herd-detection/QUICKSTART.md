# Quick Start Guide

## ⚡ Get Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 2: Start the App (1 minute)
```bash
python app.py
```

**Output should show:**
```
Starting Animal Herd Detection Flask App...
Initializing YOLO detector...
Downloading yolov3.weights... (this may take a while on first run)
Downloaded yolov3.weights
Downloaded yolov3.cfg
Downloaded coco.names
YOLO detector ready!
Starting Flask server on http://localhost:5000
```

### Step 3: Open in Browser (30 seconds)
Click: **http://localhost:5000**

### Step 4: Test Detection (1-2 minutes)
1. Upload an animal image
2. Click "Detect Animals"
3. See results with bounding boxes and animal count
4. 🚨 Gets "HERD ALERT" if 3+ animals detected

---

## 📁 Files Included

| File | Purpose |
|------|---------|
| `app.py` | Flask server & detection endpoint |
| `yolo_detector.py` | YOLOv3 detection logic |
| `templates/index.html` | Web interface |
| `static/css/style.css` | Styling |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `yolo_models/` | Auto-downloaded YOLO files |

---

## 🎯 What It Does

✅ Detects: cow, sheep, horse, dog, cat, bird, elephant, zebra, giraffe, bear
✅ Draws: Bounding boxes with labels and confidence scores
✅ Counts: Total animals detected
✅ Alerts: Shows "HERD ALERT" if 3+ animals found
✅ Display: Shows annotated image on webpage

---

## 🔧 Troubleshooting

### Issue: Port 5000 already in use
**Solution:** Edit `app.py` line 82, change `port=5000` to `port=5001` (or any free port)

### Issue: Model download failed
**Solution:** Check internet connection and run again. First run takes 5-10 minutes.

### Issue: No animals detected
**Possible causes:**
- Animals not clearly visible
- Poor lighting
- Very small animals
- Unusual animal poses
- Try a different image with clear animal subjects

### Issue: Out of Memory
**Solution:** Close other applications. YOLOv3 needs ~2GB RAM.

---

## 📊 Expected Performance

| Metric | Time |
|--------|------|
| Model Download (first run) | 5-10 min |
| Model Load-up (first inference) | 20-40 sec |
| Subsequent Inferences | 5-15 sec per image |
| Image Upload | <5 sec |
| Results Display | <1 sec |

---

## 🐘 Example Use Cases

1. **Wildlife Monitoring**: Upload photos from wildlife cameras
2. **Farm Management**: Count livestock in pasture photos
3. **Zoo Monitoring**: Detect and count animals in exhibits
4. **Research**: Track animal populations in field survey images
5. **Education**: Learn about object detection and YOLOv3

---

## 💡 Pro Tips

- Drag & drop images for faster upload
- High-resolution images may take longer but detect more animals
- Clear, bright photos work best
- Test with multiple images for consistent results
- Animals at different distances get different confidence scores

---

## 🚀 Next Steps

1. Test with your own animal images
2. Try adjusting confidence threshold for more/fewer detections
3. Experiment with different animal categories
4. Deploy to production (consider using Gunicorn instead of Flask debug mode)
5. Explore YOLOv5/v8 for faster/more accurate detection

---

Enjoy! 🦁🐄🦓
