import sys
import os

# Importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

path = os.getcwd()+'\\pyEDA\\'
sys.path.insert(0, path)
# Importing necessary functions for feature extraction
from openShimmerFile import *
from preprocessing import *
from filtering import *
from pyEDA import *
from DNN_Features import *

# You must edit these based on your files
fileName = ['data1.dat', 'data2.csv' , 'data3.dat', 'data4.dat', 'data5.csv']
columnName = 'microSiemens'
X = [] # Input X for classifier
Y = [] # Target Y for input X

for i in fileName:
  Raw_GSR = openShimmerFile(i, columnName)
  gsrdata = np.array(Raw_GSR)
  
  plt.figure(figsize=(12,4))
  plt.plot(gsrdata)
  plt.show()

  ############################################################################
  ############################ Preprocessing Part ############################
  
  # Select the new sample rate, and windowing size
  sample_rate=40
  segment_width=600

  # Resample the data based on original data rate of your device, here: 128Hz
  data = resample_data(gsrdata, 128, sample_rate)

  # Segmentwise the data based on window sizes
  s_working_data, s_measures, gsrdata_segmentwise = segmentwise(data, sample_rate=sample_rate, segment_width=segment_width, segment_overlap=0)
  
  preprocessed_gsr = []
  for i in gsrdata_segmentwise:
    preprocessed_gsr.append(normalization(rolling_mean(i, 1./sample_rate, sample_rate)))
	
  ############################ Preprocessing Part ############################
  ############################################################################
  
  
  
  #################################################################################
  ############################ Feature Extraction Part ############################

  # Statistical Feature Extraction
  for i in preprocessed_gsr:
    working_data, measures = statistical_feature_extraction(i, sample_rate)
    for k in measures.keys():
        s_measures = append_dict(s_measures, k, measures[k])
    for k in working_data.keys():
        s_working_data = append_dict(s_working_data, k, working_data[k])

  wd = s_working_data
  m = s_measures
  
  
  # Deep Learning Feature Extraction
  ###
  
  ##################################
  # Just Need to load the trainde model here and use it for prediction
  
  model = create_1Dcnn()
  path_to_DL_weights = './pyEDA/eda_deep_model.h5'
  model.load_weights(path_to_DL_weights)

  # Features extracted from Deep learning model
  getFeature = deepFeatures(model)

  # Fully Connected Network which can be used for the prediction
  getPrediction = deepPrediction(model)
  ##################################
  ###
  
  ############################ Feature Extraction Part ############################
  #################################################################################
  
  
  
  
  ##########################################################################################
  ############################ Visualizing Statistical Features ############################
  
  # Mapping the indexlist of each window to original data: comment it if you do not use windowing
  for index,i2 in enumerate(wd['indexlist']):
    for index2,j2 in enumerate(i2):
      wd['indexlist'][index][index2] = j2+segment_width*sample_rate*index

  # Storing the peaks for visualization
  peaks = []
  for index,i2 in enumerate(wd['indexlist']):
    for index2,j2 in enumerate(i2):
      peaks.append(j2)

  # Visualize the data with detected peaks marked with "x"
  ng = normalization(rolling_mean(data, 1./sample_rate, sample_rate))
  plt.plot(ng)
  plt.plot(peaks, ng[peaks], "x")
  plt.show()

  print(m['mean_gsr'])
  print(m['number_of_peaks'])
  print(m['max_of_peaks'])
  
  ############################ Visualizing Statistical Features ############################
  ##########################################################################################