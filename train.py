import csv
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.cross_validation import KFold
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np
import operator

def train():
    
    with open("I.csv", 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        features = []
        labels = []
        for row in reader:
            feature = []
            feature.append(float(row['name']))
            feature.append(float(row['addr']))
            feature.append(float(row['post']))
            feature.append(float(row['phone']))
            features.append(feature)
            labels.append(int(row['label']))
    
    X = np.array(features)
    y = np.array(labels)
    kf = KFold(250, n_folds=10)
    t_same = (0,0,0)
    svm_same = (0,0,0)
    rf_same = (0,0,0)
    nb_same = (0,0,0)
    lr_same = (0,0,0)
    for train_index, test_index in kf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        t_clf = tree.DecisionTreeClassifier()
        t_same = tuple(map(operator.add, t_same, train_with_clf(t_clf,  X_train, X_test, y_train, y_test)))

        svm_clf = svm.SVC()
        svm_same = tuple(map(operator.add, svm_same, train_with_clf(svm_clf,  X_train, X_test, y_train, y_test)))

        rf_clf = RandomForestClassifier(n_estimators=10, max_depth=3)
        rf_same = tuple(map(operator.add, rf_same, train_with_clf(rf_clf,  X_train, X_test, y_train, y_test)))

        nb_clf = GaussianNB()
        nb_same = tuple(map(operator.add, nb_same, train_with_clf(nb_clf,  X_train, X_test, y_train, y_test)))

        lr_clf = linear_model.SGDClassifier(loss='log')
        lr_same = tuple(map(operator.add, lr_same, train_with_clf(lr_clf,  X_train, X_test, y_train, y_test)))
    
    print tuple(i / 10 for i in t_same)
    print tuple(i / 10 for i in svm_same)
    print tuple(i / 10 for i in rf_same)
    print tuple(i / 10 for i in nb_same)
    print tuple(i / 10 for i in lr_same)

def train_with_clf(clf, X_train, X_test, y_train, y_test):
    clf = clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    return precision_score(y_test, y_predict), recall_score(y_test, y_predict), f1_score(y_test, y_predict)


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

if __name__ == "__main__":
    train()
