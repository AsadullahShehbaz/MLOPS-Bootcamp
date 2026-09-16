import pandas as pd 
import pickle
from sklearn.metrics import accuracy_score
import yaml 
import os 
import mlflow 

# Configure MLFlow Tracking 
os.environ['MLFLOW_TRACKING_URI'] = ("https://dagshub.com/asadullahcreative/end-to-end-ml-pipeline.mlflow")
os.environ['MLFLOW_TRACKING_USERNAME'] = "asadullahcreative"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "8d3de8fa2edb760785718bbd8ded966e4c2b7419"

params = yaml.safe_load(open("params.yaml"))['train']

def evaluate(data_path , model_path):
    data = pd.read_csv(data_path)
    X = data.drop(columns=['Outcome'])
    y = data['Outcome']

    model = pickle.load(open(model_path,'rb'))

    predictions = model.predict(X)
    accuracy = accuracy_score(y,predictions)

    mlflow.log_metric('accuracy',accuracy)
    print(f'Model Accuracy : {accuracy}')

if __name__ == "__main__":
    evaluate(params['data'],params['model'])

