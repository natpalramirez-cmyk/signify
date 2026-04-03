from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import logging
from datetime import datetime
from gesture_detector import GestureDetector
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize gesture detector
gesture_detector = None
try:
    gesture_detector = GestureDetector()
    logger.info("Gesture detector initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize gesture detector: {e}")

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/foto", methods=["POST"])
def foto():
    try:
        if 'foto' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['foto']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gesture_{timestamp}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        logger.info(f"Photo saved to {filepath}")
        
        # Process image for gesture detection
        if gesture_detector:
            detected_letter, current_word = gesture_detector.process_image(filepath)
            
            return jsonify({
                "success": True,
                "filename": filename,
                "detected_letter": detected_letter,
                "current_word": current_word
            })
        else:
            return jsonify({
                "success": True,
                "filename": filename,
                "message": "Gesture detector not available"
            })
            
    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/reset_word", methods=["POST"])
def reset_word():
    try:
        if gesture_detector:
            gesture_detector.reset_word()
            return jsonify({"success": True, "message": "Word reset successfully"})
        else:
            return jsonify({"error": "Gesture detector not available"}), 500
    except Exception as e:
        logger.error(f"Error resetting word: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "gesture_detector": gesture_detector is not None
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
    

