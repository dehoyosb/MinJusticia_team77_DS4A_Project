import numpy as np
import pandas as pd
from sklearn import preprocessing

# Featurization 
def reduce_cats(column, max_cat):
    cats = column.value_counts().index.tolist()
    new  = column.map(lambda x: x if x in cats[:max_cat] else 'OTHER')
    return new 

def dummy_helper(column):
    binary = preprocessing.LabelBinarizer()
    x      = column.fillna('MISSING').astype(str)
    temp   = binary.fit_transform(x.values)
    nmes   = [column.name + '_' + i for i in binary.classes_] if temp.shape[1] > 1 else [column.name]
    is_bin = temp.shape[1] == 2
    data   = pd.DataFrame(data = temp, columns = nmes)
    return data, is_bin
    
def binarize(data, column_nme):
    binarized = []
    for nme in column_nme:
        x, is_bin = dummy_helper(data[nme])
        if is_bin:
            data.loc[:,nme] = x
        else:
            data = pd.concat([data, x], axis = 1)
        binarized += list(x.columns)
    return data, binarized

def missing_ind(data, nme_list):
    for nme in nme_list:
        nme_na = 'na_ind_' + nme
        data.loc[:,nme_na] = (data[nme].isnull()).astype(float)
    return data

