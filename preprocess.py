import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_data():

    # 🔥 universal separator fix
    df = pd.read_csv("data/KDDTrain+.txt", header=None, delimiter=r"\s+|,", engine='python')

    # drop last column (difficulty)
    df = df.iloc[:, :-1]

    label_col = df.columns[-1]

    y = df[label_col]
    X = df.drop(label_col, axis=1)

    # encode categorical
    for col in [1, 2, 3]:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))

    # convert to numeric
    X = X.apply(pd.to_numeric, errors='coerce')
    X = X.fillna(0)

    print("Check columns:", X.shape)

    # normalize
    X = StandardScaler().fit_transform(X)

    y = LabelEncoder().fit_transform(y.astype(str))

    return X, y, None