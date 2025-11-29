from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

if not os.path.exists('./iris_model.pkl'):
    print("Training model...")
    iris = datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, './iris_model.pkl')
    print("Model trained and saved.")

print("Loading model into memory...")
loaded_model = joblib.load('./iris_model.pkl')

def predict(features):
    prediction = loaded_model.predict([features])[0]
    return prediction.item()
