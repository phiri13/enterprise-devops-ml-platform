import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def train():
    data = load_iris()
    X, y = data.data, data.target

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, "model/model.joblib")

if __name__ == "__main__":
    train()
