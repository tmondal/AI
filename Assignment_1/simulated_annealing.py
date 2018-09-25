import matplotlib.pyplot as plt
import math
from random import uniform,randint
import numpy as np
from sklearn import datasets, linear_model, metrics, preprocessing
from sklearn.model_selection import train_test_split

# load dataset which should not contain missing feature as '?'
input_file = 'demo.txt'

X = []  # Feature matrix
y = []  # Output column
X_new = []
X_subset = []
pltscore = []
count = 0
# Read each row from the dataset except the last column 
with open(input_file, 'r') as f:
    for line in f.readlines():
    	data = line[:-1].split(',')
    	print("[Row no]----[Column no]: {}----{}".format(count,len(data)))
    	X.append(data)
    	count = count + 1
# Convert to numpy array to do operation efficiently
X = np.array(X)

"""
Preprocessing of loaded dataset: 

Convert string data to numerical data with label encoder 
which uses One Hot encoding to represent a string from a set of string
e.g Let string set is ["black", "yellow", "white","red","blue","green","pink","gray"]
then black will be One Hot encoded as [1 0 0 0 0 0 0 0]
"""
label_encoder = [] 
X_encoded = np.empty(X.shape)
for i,item in enumerate(X[0]):
    if item.isdigit(): 
        X_encoded[:, i] = X[:, i]
    else:
        label_encoder.append(preprocessing.LabelEncoder())
        X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])

""" 
X contains all rows and all columns of X_encoded except last column
Y contains last column
"""
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
print("Initial score : {}".format(parent_score))

## setting plot style

# plt.style.use('fivethirtyeight')
 
# ## plotting residual errors in training data
# plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color = "green", s = 10, label = 'Train data')
 
# ## plotting residual errors in test data
# plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test, color = "blue", s = 10, label = 'Test data')
 
# ## plotting line for zero residual error
# plt.hlines(y = 0, xmin = -50, xmax = 20, linewidth = 2)
 
# ## plotting legend
# plt.legend(loc = 'upper right')
 
# ## plot title
# plt.title("Residual errors")
 
# ## function to show plot
# plt.show()

# Setting initial temperature which should be tuned properly for better subset
T = 100000


limit = X.shape[1] # No of columns 
print("Initial shape: {}".format(X.shape[1]))

while T > 10:
	# Select a random column to remove and check score
	r = randint(0,limit-1)
	print("Column removed: {}".format(r))
	X_new = X;
	X_new = np.delete(X_new,r,1);

	# splitting X and y into training and testing sets
	X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.4,random_state=1)
	 
	# train the model using the training sets
	reg.fit(X_train, y_train)

	# variance score: 1 means perfect prediction
	child_score = reg.score(X_test, y_test)
	delta_E = child_score - parent_score

	if delta_E > 0:
		parent_score = child_score
		# print("score: {}".format(child_score))
		pltscore.append(child_score)
		X = X_new
		j = i
	else:
		# Accept bad move if the probability is higher than a randon number between 0 and 1
		nr = uniform(0,1)
		if nr < math.exp(delta_E/T):
			# accept new child
			X = X_new
			parent_score = child_score
			# print("score: {}".format(child_score))
			pltscore.append(child_score)
		else:
			print("Parent not changed.")
	# Change limit according to new feature matrix
	limit = X.shape[1]

	"""
	Temparature decreases which indicates take bad move with low probability
	as you go towards solution. This decrease rate is tuneable
	"""
	T = T/10				

print("\nFinal shape: {}\n".format(limit))
print(X)

X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.4,random_state=1)

# create linear regression object
reg = linear_model.LinearRegression()
 
# train the model using the training sets
reg.fit(X_train, y_train)

# plot for residual error
 
## setting plot style
# plt.style.use('fivethirtyeight')
 
# ## plotting residual errors in training data
# plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color = "green", s = 10, label = 'Train data')
 
# ## plotting residual errors in test data
# plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test, color = "blue", s = 10, label = 'Test data')
 
# ## plotting line for zero residual error
# plt.hlines(y = 0, xmin = -50, xmax = 20, linewidth = 2)
 
# ## plotting legend
# plt.legend(loc = 'upper right')
 
# ## plot title
# plt.title("Residual errors")
 
# ## function to show plot
# plt.show()

# val = []
pltscore.reverse()
plt.plot(pltscore)
plt.ylabel('')
plt.show()
