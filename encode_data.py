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
infile = "Employee.csv"

df=pd.read_csv(infile)

cat_feature=['Education', 'JoiningYear', 'City', 'PaymentTier', 'Gender',
       'EverBenched', 'ExperienceInCurrentDomain']

for col in cat_feature:
    df[col]=le.fit_transform(df[col])

df["LeaveOrNot"].replace({0: -1}, inplace=True) # make all 0s to -1s (critical for evaluating fairness)
X=df.drop(['LeaveOrNot'],axis=1)
y=df.LeaveOrNot
df.to_csv(path_or_buf='Employee.csv', index=False)

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

joblib.dump(model, 'Employee_DecisionTree_Original.pkl')