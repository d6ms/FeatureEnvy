# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 11:32:28 2018

@author: xzf0724
"""
import numpy as np
import time
import os
import sys
np.random.seed(1337)

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json  

project = sys.argv[1]
if not project:
    raise Error('specify target project')

MAX_SEQUENCE_LENGTH = 15 

TESTPATH = f'../Data/test/{project}/'
MODELPATH = './'
FILENAME = f'../Data/test/{project}/test_MethodId.txt'
values = []

print ("start time:"+time.strftime("%Y/%m/%d  %H:%M:%S"))
start = time.clock()

    
f = open(FILENAME, 'r', encoding = 'utf-8')
for line in f:
    value = line.split()
    values.append(value)

NUM_CORRECT = 0
TOTAL = len(values)
model = model_from_json(open(MODELPATH + 'my_model.json').read())  
model.load_weights(MODELPATH + 'my_model_weights.h5')
ii = 0
for sentence in values:
    ii=ii+1
    test_distances = []
    test_labels = []
    test_texts = []
    targetClassNames=[]
    classId = sentence[0]
    label = sentence[1]
    if(os.path.exists(TESTPATH + 'test_Distances'+classId+'.txt')):
        with open(TESTPATH + 'test_Distances'+classId+'.txt','r') as file_to_read:
            for line in file_to_read.readlines():
                values = line.split()
                test_distance = values[:2]
        
                test_distances.append(test_distance)
                test_label =values[2:]
                test_labels.append(test_label)
        
                
        with open(TESTPATH + 'test_Names'+classId+'.txt','r') as file_to_read:
            for line in file_to_read.readlines():
                test_texts.append(line)
                line = line.split()
                targetClassNames.append(line[10:])
        
        tokenizer1 = Tokenizer(num_words=None)
        tokenizer1.fit_on_texts(test_texts)
        test_sequences = tokenizer1.texts_to_sequences(test_texts)
        test_word_index = tokenizer1.word_index
        test_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)  
        test_distances = np.asarray(test_distances)
        test_labels1 = test_labels
        test_labels = np.asarray(test_labels)

        
        x_val = []
        x_val_names = test_data
        x_val_dis = test_distances
        x_val_dis = np.expand_dims(x_val_dis, axis=2)
        x_val.append(x_val_names)
        x_val.append(np.array(x_val_dis))
        y_val = np.array(test_labels) 
        
        preds = model.predict_classes(x_val)
        preds_double = model.predict(x_val)

        if all(pred == 0 for pred in preds):
            NUM_CORRECT += 1


        
print('accuracy--------', NUM_CORRECT / TOTAL)
