# source: https://www.kaggle.com/yemishin/eda-and-employee-future-prediction
import pandas as pd
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
import joblib
import config

# did exactly as the original authors had processed the data
infile = config.original_inputs

df=pd.read_csv(infile)

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
df.to_csv(path_or_buf=infile, index=False)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=12)

model= DecisionTreeClassifier(random_state=42,criterion='entropy',splitter='random')
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
joblib.dump(model, file_to_save_model)