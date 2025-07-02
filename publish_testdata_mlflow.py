import mlflow
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import os


os.environ['MLFLOW_TRACKING_USERNAME'] = "admin"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "password1234"

inputs, targets = datasets.load_iris(return_X_y=True)
x_train, x_test, y_train, y_test = train_test_split(inputs, targets, test_size=0.2, random_state=42)

params = {
    "solver": "lbfgs",
    "max_iter": 100,
    "multi_class": "auto",
    "random_state": 8888
}

lr = LogisticRegression(**params)
lr.fit(x_train, y_train)

y_predict = lr.predict(x_test)

accuracy = accuracy_score(y_test, y_predict)
precision = precision_score(y_test, y_predict, average='micro')
recall = recall_score(y_test, y_predict, average='micro')
f1 = f1_score(y_test, y_predict, average='micro')

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Test")

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)

    mlflow.set_tag("Traning Info", "Basic model for testing purposes")

    signature = mlflow.models.infer_signature(x_train, lr.predict(x_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        name="iris_model",
        signature=signature,
        input_example=x_train,
        registered_model_name="test_model"
    )

