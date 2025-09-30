# from flask import Flask, render_template, request, jsonify
# from gtts import gTTS
# import numpy as np
# import base64
# import io
# import os
# from PIL import Image
# from tensorflow.keras.models import load_model

# app = Flask(__name__, static_folder='static', template_folder='templates')

# MODEL_PATH = 'model/driver_fatigue_model.h5'

# # Load the model
# if os.path.exists(MODEL_PATH):
#     model = load_model(MODEL_PATH)
#     print("✅ Model loaded successfully from:", MODEL_PATH)
# else:
#     print("❌ Model not found at:", MODEL_PATH)
#     model = None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded'}), 500

#     try:
#         data = request.get_json()
#         image_data = data['image'].split(',')[1]
#         img_bytes = base64.b64decode(image_data)

#         img = Image.open(io.BytesIO(img_bytes)).resize((64, 64))
#         img = np.array(img) / 255.0
#         img = img.reshape(1, 64, 64, 3)

#         prediction = model.predict(img)[0][0]
#         label = 'Drowsy' if prediction > 0.5 else 'Alert'

#         # Save audio alert only if drowsy
#         if label == 'Drowsy':
#             tts = gTTS("You are in danger. Press brake!", lang='en')
#             tts.save("static/alert.mp3")

#         return jsonify({'label': label})

#     except Exception as e:
#         print("🔥 Error during prediction:", str(e))
#         return jsonify({'error': 'Prediction failed'}), 500

# if __name__ == '__main__':
#     app.run()


from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import numpy as np
import base64
import io
import os
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__, static_folder='static', template_folder='templates')

MODEL_PATH = 'model/driver_fatigue_model.h5'
ALERT_FILE = "static/alert.mp3"

# ✅ Ensure alert.mp3 exists at startup
if not os.path.exists(ALERT_FILE):
    tts = gTTS("You are in danger. Press brake!", lang='en')
    tts.save(ALERT_FILE)
    print("🔊 Default alert.mp3 created at startup")

# ✅ Load model
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully from:", MODEL_PATH)
else:
    print("❌ Model not found at:", MODEL_PATH)
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(image_data)

        # Preprocess image
        img = Image.open(io.BytesIO(img_bytes)).resize((64, 64))
        img = np.array(img) / 255.0
        img = img.reshape(1, 64, 64, 3)

        # Run prediction
        prediction = model.predict(img)[0][0]
        label = 'Drowsy' if prediction > 0.5 else 'Alert'

        # Overwrite audio alert only if drowsy
        if label == 'Drowsy':
            tts = gTTS("You are in danger. Press brake!", lang='en')
            tts.save(ALERT_FILE)
            print("⚠️ Alert audio updated: Drowsy detected")

        return jsonify({'label': label})

    except Exception as e:
        print("🔥 Error during prediction:", str(e))
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
