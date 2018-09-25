import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, metrics, preprocessing
from sklearn.model_selection import train_test_split

# load dataset
input_file = 'demo.txt'

X = []
y = []
X_new = []
X_subset = []
pltscore = []
count = 0
with open(input_file, 'r') as f:
    for line in f.readlines():
    	data = line[:-1].split(',')
    	print("[Row no]----[Column no]: {}----{}".format(count,len(data)))
    	# print("No of column: {}".format(len(data)))
    	X.append(data)
    	count = count + 1
# Convert to numpy array
X = np.array(X)
print("column: {}".format(X.shape[1]))

# Convert string data to numerical data with label encoder 
# which uses One Hot encoding to represent a string from a set of string
label_encoder = [] 
X_encoded = np.empty(X.shape)
for i,item in enumerate(X[0]):
	if item.isdigit():
		X_encoded[:, i] = X[:, i]
	else:
		label_encoder.append(preprocessing.LabelEncoder())
		X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])

# X contains all rows and all columns of X_encoded except last column
# Y contains last column
X = X_encoded[:, :-1].astype(int)
y = X_encoded[:, -1].astype(int)



# splitting X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)
 
# create linear regression object
reg = linear_model.LinearRegression()
 
# train the model using the training sets
reg.fit(X_train, y_train)
 
# variance score: 1 means perfect prediction
parent_score = reg.score(X_test, y_test)
pltscore.append(parent_score)

## setting plot style
plt.style.use('fivethirtyeight')
 
## plotting residual errors in training data
plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color = "green", s = 10, label = 'Train data')
 
## plotting residual errors in test data
plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test, color = "blue", s = 10, label = 'Test data')
 
## plotting line for zero residual error
plt.hlines(y = 0, xmin = -50, xmax = 20, linewidth = 2)
 
## plotting legend
plt.legend(loc = 'upper right')
 
## plot title
plt.title("Residual errors")
 
## function to show plot
plt.show()

# Hill Climbing Approach
# Worst Case Running Time = N+N-1+N-2+....+1 = O(N^2)

while 1:

	i = 0
	limit = X.shape[1]
	score = -1000000.0
	print("New shape.......")
	print(X.shape[1])
	while i < limit:

		X_new = X;
		X_new = np.delete(X_new,i,1);
		# print(X_new)


		# splitting X and y into training and testing sets
		X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.4,random_state=1)
		 
		# create linear regression object
		#reg = linear_model.LinearRegression()
		 
		# train the model using the training sets
		reg.fit(X_train, y_train)
		
		# variance score: 1 means perfect prediction
		temp = reg.score(X_test, y_test)
		print("New score : ")
		print(temp)

		if temp > score:
			score = temp
			j = i

		i = i + 1;

	if parent_score < score:
		parent_score = score
		pltscore.append(score)
		X = np.delete(X,j,1)
	else:
		break

	print("Parent Score")
	print(parent_score)

# print("Feature subset: ")
# print(X.shape[1])
# print("Required feature matrix: ")
print(X)

X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.4,random_state=1)

# create linear regression object
reg = linear_model.LinearRegression()
 
# train the model using the training sets
reg.fit(X_train, y_train)

# plot for residual error
 
## setting plot style
plt.style.use('fivethirtyeight')
 
## plotting residual errors in training data
plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color = "green", s = 10, label = 'Train data')
 
## plotting residual errors in test data
plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test, color = "blue", s = 10, label = 'Test data')
 
## plotting line for zero residual error
plt.hlines(y = 0, xmin = -50, xmax = 20, linewidth = 2)
 
## plotting legend
plt.legend(loc = 'upper right')
 
## plot title
plt.title("Residual errors")
 
## function to show plot
plt.show()
# plt.ylim(0,1)
plt.plot(pltscore)
plt.ylabel('Score plot')
plt.show()