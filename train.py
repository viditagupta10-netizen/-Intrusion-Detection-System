import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv1D, LSTM, Dense
from utils.preprocess import load_data
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

model_path = "model/model.h5"

# 🔥 ALWAYS load data first
X, y, le = load_data()

# reshape for CNN-LSTM
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 🔥 train-test split (VERY IMPORTANT)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔥 load or train
if os.path.exists(model_path):
    print("Model already trained ✅ Loading model...")
    model = load_model(model_path)

else:
    print("Training model first time 🚀")

    model = Sequential([
        Conv1D(32, 2, activation='relu', input_shape=(X.shape[1],1)),
        LSTM(64),
        Dense(32, activation='relu'),
        Dense(len(set(y)), activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(X_train, y_train, epochs=10, batch_size=64)

    model.save(model_path)
    print("Model trained and saved ✅")

# 🔥 Evaluate ALWAYS (important)
pred = model.predict(X_test)
pred_classes = np.argmax(pred, axis=1)

print("Accuracy:", accuracy_score(y_test, pred_classes))
print(classification_report(y_test, pred_classes))