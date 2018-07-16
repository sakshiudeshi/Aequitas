import numpy as np
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import random
from sklearn.neural_network import MLPClassifier
import config


X = []
Y = []
i = 0
neg_count = 0
pos_count = 0
with open("cleaned_train", "r") as ins:
    for line in ins:
        line = line.strip()
        line1 = line.split(',')
        if (i == 0):
            i += 1
            continue
        L = map(int, line1[:-1])
        # L[sens_arg-1]=-1
        X.append(L)

        if (int(line1[-1]) == 0):
            Y.append(-1)
            neg_count = neg_count + 1
        else:
            Y.append(1)
            pos_count = pos_count + 1


X = np.array(X)
Y = np.array(Y)
print neg_count, pos_count

# w = svm.SVC(gamma=0.0025)

# model = MLPClassifier(solver='lbfgs', alpha=1e-5,
#                       hidden_layer_sizes=(7, 5), random_state=1)
model = DecisionTreeClassifier()
model.fit(X, Y)
print cross_val_score(model, X, Y, scoring='accuracy')
joblib.dump(model, 'Decision_tree_standard_unfair.pkl')
