import sys
import os

# 🔥 Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model

# 🔥 RAG import
# from rag import explain_attack
def explain_attack(label):
    explanations = {
        0: "Normal traffic - Safe network activity",
        1: "DoS attack - Server overload attempt",
        2: "Probe attack - Network scanning detected",
        3: "R2L attack - Unauthorized access attempt",
        4: "U2R attack - Privilege escalation attack"
    }
    return explanations.get(label, "Unknown attack")

app = Flask(__name__)

# 🔥 Load trained model once
model = load_model("../model/model.h5")

# 🔥 Label mapping (important)
labels = ["Normal", "DoS", "Probe", "R2L", "U2R"]


# 🏠 Home route
@app.route('/')
def home():
    return render_template("index.html")


# 🔍 Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # user input
        data = request.form['features']

        # convert to float list
        values = list(map(float, data.split(",")))

        # check length
        if len(values) != 41:
            return render_template("index.html",
                                   prediction="Invalid Input ❌",
                                   explanation="Please enter exactly 41 values")

        # reshape for model
        sample = np.array(values).reshape(1, 41, 1)

        # prediction
        pred = model.predict(sample)
        result = np.argmax(pred)

        # label convert
        result_label = labels[result]

        # RAG explanation
        explanation = explain_attack(result)

        return render_template("index.html",
                               prediction=result_label,
                               explanation=explanation)

    except Exception as e:
        return render_template("index.html",
                               prediction="Error ❌",
                               explanation=str(e))


# ▶️ Run server
if __name__ == "__main__":
    app.run(debug=True)