import numpy as np
from tensorflow.keras.models import load_model

# 🔥 Load trained model (only once)
model = load_model("model/model.h5")

# 🔥 Label mapping (same order as training)
labels = ["Normal", "DoS", "Probe", "R2L", "U2R"]

def predict(row):
    try:
        # Convert input to numpy
        row = np.array(row, dtype=float)

        # Reshape for CNN-LSTM → (1, features, 1)
        row = row.reshape(1, 41, 1)

        # Prediction
        pred = model.predict(row, verbose=0)

        # Get class index
        label_index = int(np.argmax(pred))
        if label_index > 4:
          label_index = 0 # default to Normal if out of range

        return label_index

    except Exception as e:
        print("Prediction Error:", e)
        return 0   # default Normal