import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report
from utils.preprocess import load_data

model = load_model("model/model.h5")

X, y, le = load_data()
X = X.reshape(X.shape[0], X.shape[1], 1)

pred = model.predict(X)
pred_classes = np.argmax(pred, axis=1)

print(classification_report(y, pred_classes))