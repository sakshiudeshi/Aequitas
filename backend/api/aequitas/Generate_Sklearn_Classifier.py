# source: https://www.kaggle.com/yemishin/eda-and-employee-future-prediction
import pandas as pd
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import tree
import random
import joblib
import config as config
import os

def run():
    # did exactly as the original authors had processed the data
    infile = config.original_inputs

    df=pd.read_csv(f"TrainingInputs/{infile}")

    cat_feature = list(df.columns)
    # cat_feature=['Education', 'JoiningYear', 'City', 'PaymentTier', 'Gender',
    #        'EverBenched', 'ExperienceInCurrentDomain']

    for col in cat_feature:
        df[col]=le.fit_transform(df[col])

    sensitive_param_name = config.sensitive_param_name
    df[sensitive_param_name].replace({0: -1}, inplace=True) # make all 0s to -1s (critical for evaluating fairness)

    col_to_be_predicted = config.col_to_be_predicted
    X=df.drop([col_to_be_predicted],axis=1)
    y=df[col_to_be_predicted]
    df.to_csv(path_or_buf=f"TrainingInputs/{os.path.splitext(infile)[0]}_cleaned.csv", index=False)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=12)

    model= DecisionTreeClassifier(random_state=42,criterion='entropy',splitter='random') # should be modifiable
    # w = svm.SVC(gamma=0.0025)

    # model = MLPClassifier(solver='lbfgs', alpha=1e-5,
    #                       hidden_layer_sizes=(7, 5), random_state=1)

    model.fit(X_train,y_train)

    pred=model.predict(X_test)

    scores=[]
    scores.append({
            'model': 'DecisionTreeClassifier',
            'score': model.score(X_test,y_test),
            'f1_score' : f1_score(y_test,pred)
        })

    model.score(X_test, y_test)

    file_to_save_model = config.classifier_name
    joblib.dump(model, f'TrainedModels/{file_to_save_model}')

if __name__ == "__main__":
    run()