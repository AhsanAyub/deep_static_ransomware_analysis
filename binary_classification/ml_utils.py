#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"


import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)
import matplotlib.pyplot as plt

from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier


def ModelCompilation(X, Y, classifier):
    cv = StratifiedKFold(n_splits=5, random_state=None, shuffle=False)
    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []
    
    for train, test in cv.split(X, Y):
        # Spliting the dataset
        X_train, X_test, Y_train, Y_test = X[train], X[test], Y[train], Y[test]
        
        # Fitting the classifier into training set
        classifier = classifier.fit(X_train, Y_train)
        
        # Breakdown of statistical measure based on classes
        Y_pred = classifier.predict(X_test)
        #print(classification_report(Y_test, Y_pred, digits=4))
        
        # Compute the model's performance
        accuracy_scores.append(accuracy_score(Y_test, Y_pred))
        f1_scores_temp = []
        f1_scores_temp.append(f1_score(Y_test, Y_pred, average=None))
        f1_scores.append(np.mean(f1_scores_temp))
        del f1_scores_temp
        
        precision_scores_temp = []
        precision_scores_temp.append(precision_score(Y_test, Y_pred, average=None))
        precision_scores.append(np.mean(precision_scores_temp))
        del precision_scores_temp
        
        recall_scores_temp = []
        recall_scores_temp.append(recall_score(Y_test, Y_pred, average=None))
        recall_scores.append(np.mean(recall_scores_temp))
        del recall_scores_temp
        
    return accuracy_scores, precision_scores, recall_scores, f1_scores


def SupportVectorClassifier(X, Y):
    print("=== SVM (RBF) ===")
    classifier = SVC(kernel = 'rbf', gamma = 'scale')
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))
    
    print("=== SVM (POLY) ===")
    classifier = SVC(kernel = 'poly', gamma = 'scale')
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))
    
    
def DecisionTree(X, Y):
    print("=== Decision Tree ===")
    classifier = tree.DecisionTreeClassifier()
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))
    tree.plot_tree(classifier)
    plt.show()
    
    
def RandomForest(X, Y):
    print("=== Random Forest ===")
    classifier = RandomForestClassifier(n_estimators=100, criterion="gini", random_state=0)
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))


def AdaBoost(X, Y):
    print("=== Ada Boost Classifier ===")
    classifier = AdaBoostClassifier(n_estimators=100, algorithm="SAMME.R", random_state=0)
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))
    
    
def GradientBoosting(X, Y):
    print("=== Gradient Boosting Classifier ===")
    classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, random_state=0)
    accuracy_scores, precision_scores, recall_scores, f1_scores = ModelCompilation(X, Y, classifier)
    
    print("Accuracy: ", np.mean(accuracy_scores))
    print("Precision: ", np.mean(precision_scores))
    print("Recall: ", np.mean(recall_scores))
    print("F1: ", np.mean(f1_scores))


def RunModels(X, Y):
    SupportVectorClassifier(X, Y)
    DecisionTree(X, Y)
    RandomForest(X, Y)
    AdaBoost(X, Y)
    GradientBoosting(X, Y)