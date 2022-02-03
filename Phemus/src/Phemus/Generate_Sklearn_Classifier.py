# source: https://www.kaggle.com/yemishin/eda-and-employee-future-prediction
import pandas as pd
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
# from sklearn.neural_network import MLPClassifier
# from sklearn import tree
# import random
import joblib
import os
from .Dataset import Dataset

def generate_sklearn_classifier(dataset: Dataset, output_pkl_dir):
    # did exactly as the original authors had processed the data
    input_csv_dir = dataset.dataset_dir
    sensitive_param_name = dataset.sensitive_param_name
    col_to_be_predicted = dataset.col_to_be_predicted
    
    df=pd.read_csv(input_csv_dir)

    cat_feature = list(df.columns)
    # cat_feature=['Education', 'JoiningYear', 'City', 'PaymentTier', 'Gender',
    #        'EverBenched', 'ExperienceInCurrentDomain']

    for col in cat_feature:
        df[col]=le.fit_transform(df[col])

    # df[sensitive_param_name].replace({0: -1}, inplace=True) # make all 0s to -1s (critical for evaluating fairness)

    X=df.drop([col_to_be_predicted],axis=1)
    y=df[col_to_be_predicted]

    df.to_csv(path_or_buf=f"{os.path.splitext(input_csv_dir)[0]}_cleaned.csv", index=False)

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

    joblib.dump(model, output_pkl_dir)
