import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, precision_recall_curve, confusion_matrix, f1_score

# Evaluation 
# t: threshold 

def binprob(y_hat, t):
    threshold = np.sort(y_hat)[::-1][int(t*len(y_hat))]
    binary    = [1 if i >= threshold else 0 for i in y_hat]
    y_pred    = np.asarray(binary)
    return y_pred

def accuracy_t(y, y_hat, t):
    y_pred = binprob(y_hat, t)
    score  = accuracy_score(y, y_pred)
    return score 

def precision_t(y, y_hat, t):
    y_pred = binprob(y_hat, t)
    score  = precision_score(y, y_pred)
    return score 

def recall_t(y, y_hat, t):
    y_pred = binprob(y_hat, t)
    score  = recall_score(y, y_pred)
    return score

def f1_t(y, y_hat, t):
    y_pred = binprob(y_hat, t)
    score  = f1_score(y, y_pred)
    return score