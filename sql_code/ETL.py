#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Embedding
from matplotlib import pyplot as plt
plt.style.use('dark_background')
from keras.preprocessing.sequence import pad_sequences
import sklearn
import pyodbc
import pandas
from scipy.sparse import csr_matrix
from nltk.corpus import stopwords
import string
import nltk


#### lectura del archivo a traladar




conn = pyodbc.connect('Driver={PostgreSQL Unicode};'
                      #'Server={postgres,5432};'
                       'Server={localhost};'
                       'port={5432};'
                       'Database={minjusticia};'
                       
                       'UID={team77};'
                       'PWD={mintic2020.};')

sqlPersonasColocadas= "select top(1000) * from PersonasColocadas"

PersonasColocadas = pandas.read_sql(sqlPersonasColocadas,conn)

# limpieza de la base de datos

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text


PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"]
PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].str.lower()
PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].apply(remove_punctuations)
PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].str.replace("\n","")
PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
#PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))

PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"]
PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"].str.lower()
PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"].apply(remove_punctuations)
PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"].str.replace("\n","")
PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
#PersonasColocadas["Perfil"] = PersonasColocadas["Perfil"].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))



# definir la matriz de distancias 
def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union



import sys

# funcion para mirar el avance del proceso de generación de distancias
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

PersonasColocadas["DescripcionVacante2"] = PersonasColocadas["DescripcionVacante"]
PersonasColocadas["DescripcionVacante"] = PersonasColocadas["DescripcionVacante"].apply(lambda x: x.split())


distaceMatrix = []
row_ind = []
col_ind = []

for i in range(0,len(PersonasColocadas.index)):
    distaceMatrix.extend(PersonasColocadas["DescripcionVacante"].apply(lambda x: jaccard_similarity(x,PersonasColocadas["DescripcionVacante"][i])))
    row_ind.extend(np.repeat(i, len(PersonasColocadas.index), axis=0))
    col_ind.extend(list(range(0,len(PersonasColocadas.index))))
    update_progress(i/(len(PersonasColocadas.index)))

#distancias = MatrizDistancias(PersonasColocadas["DescripcionVacante"])
#distancias

# escalamiento multidimensional
from sklearn.manifold import MDS
N = len(PersonasColocadas.index)
embedding = MDS(n_components=1)
X_transformed = embedding.fit_transform(csr_matrix((distaceMatrix, (row_ind, col_ind)), shape=(N, N)).toarray())



# clustering usando el algoritmos DBSCAN
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.3, min_samples=1, metric="euclidean", n_jobs=-1)

# asignar los grupos al dataframe original
PersonasColocadas["Grupos"] = dbscan.fit_predict(X_transformed)
PersonasColocadas["Grupos"].unique()
PersonasColocadas["Grupos"].max()


max_words = 8192
phrase_len = PersonasColocadas["DescripcionVacante"].apply(lambda p: len(p))
max_phrase_len = 100#phrase_len.max()

tokenizer = Tokenizer(
    num_words = max_words,
    filters = '"#$%&()*+-/:;<=>@[\]^_`{|}~'
)


#####   selección de los conjuntos de prueba y entrenamiento

#from sklearn import preprocessing

seed = 9
np.random.seed(seed)

entrenamiento= PersonasColocadas.sample(n=math.trunc(N*0.90))
test = PersonasColocadas[PersonasColocadas["Id"].isin(entrenamiento["Id"]) == False]

X_train = entrenamiento["DescripcionVacante2"]
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_train = pad_sequences(X_train, maxlen = max_phrase_len)
print('Shape of data tensor:', X_train.shape)
y_train = entrenamiento["Grupos"]
#y_train = preprocessing.label_binarize(y_train, classes=range(1,entrenamiento["Grupos"].max()))
y_train = pandas.Categorical(y_train)

X_train.shape
y_train.shape


X_test = test["DescripcionVacante2"]
tokenizer.fit_on_texts(X_test)
X_test = tokenizer.texts_to_sequences(X_test)
X_test = pad_sequences(X_test, maxlen = max_phrase_len)
print('Shape of data tensor:', X_test.shape)
y_test = test["Grupos"]
#y_test = preprocessing.label_binarize(y_train, classes=range(1,entrenamiento["Grupos"].max()))

y_test = pandas.Categorical(y_test)

X_test.shape
y_test.shape




# ajuste de la red neuronal

batch_size = 512
#epochs = 8
epochs = 18

model_lstm = Sequential()
model_lstm.add(Embedding(input_dim = max_words, output_dim = 256, input_length = max_phrase_len))
model_lstm.add(SpatialDropout1D(0.3))
model_lstm.add(LSTM(256, dropout = 0.3, recurrent_dropout = 0.3))
#model_lstm.add(Dense(256, activation = 'relu'))
#model_lstm.add(Dropout(0.3))
model_lstm.add(Dense(entrenamiento["Grupos"].max()+1, activation = 'softmax'))
model_lstm.compile(
    #loss='categorical_crossentropy',
    loss = 'sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model_lstm.fit(
    X_train,
    y_train,
#    validation_split = 0.1,
    epochs = epochs,
    batch_size = batch_size
)



# evaluacion del modelo

accr = model_lstm.evaluate(X_test,y_test)
print('Test set/n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))

plt.title('Loss')
plt.plot(history.history['loss'], label='train')
#plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show();


plt.title('Accuracy')
plt.plot(history.history['accuracy'], label='train')
#plt.plot(history.history['val_acc'], label='test')
plt.legend()
plt.show();



y_pred = model_lstm.predict(X_test)
y_pred = y_pred.argmax(axis = 1)
matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)

sum(y_pred ==y_test)/len(y_pred)




# guarda el modelo a un archivo para produccion

model_lstm.save('lstm_model.h5')








