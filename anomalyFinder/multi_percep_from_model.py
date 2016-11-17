import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

numpy.random.seed(7)
# load the dataset
dataframe = pd.read_csv('parsedOutputarima_model.csv',usecols=[1], engine='python', skipfooter=0)
dataset = dataframe.values
dataset = dataset.astype('float32')

test_size = len(dataset)
test = dataset[0:test_size,:]
print len(dataset)
print(len(test))
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)
# reshape into X=t and Y=t+1
look_back = 1
testX, testY = create_dataset(test, look_back)

print testX[36:40],testY[36:40]

#load model from disk
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

loaded_model.compile(loss='mean_squared_error', optimizer='adam')

# generate predictions for testing
testPredict = loaded_model.predict(testX)


# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[look_back:len(testPredict)+look_back, :] = testPredict

print testPredict[36:40]
# plot baseline and predictions
plt.plot(dataset)
plt.plot(testPredictPlot)
plt.show()