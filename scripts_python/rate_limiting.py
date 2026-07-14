import requests

url: str = "https://mlflow.urbanairlab.hn/"

for i in range(100):
    r = requests.get(url)
    print(r.status_code)