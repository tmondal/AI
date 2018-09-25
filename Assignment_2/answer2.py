import numpy as np
import matplotlib.pyplot as plt

arena = np.zeros((4,16))
arena.fill(1)
arena[0][4] = 0
arena[0][10] = 0
arena[0][14] = 0
arena[1][0] = 0
arena[1][1] = 0
arena[1][4] = 0
arena[1][6] = 0
arena[1][7] = 0
arena[1][9] = 0
arena[1][11] = 0
arena[1][13] = 0
arena[1][14] = 0
arena[1][15] = 0
arena[2][0] = 0
arena[2][4] = 0
arena[2][6] = 0
arena[2][13] = 0
arena[2][14] = 0
arena[3][2] = 0
arena[3][6] = 0
arena[3][11] = 0

get_state = {}
k = 1
for i in range(0,4):
	for j in range(0,16):
		if arena[i][j] == 1:
			get_state[i,j] = k
			k += 1
get_coord = {}
for i in range(1,44):
	for key,val in get_state.items():
		get_coord[val] = key

# generate neighbour list
neighbour_list = []
# bit_list has ground truth value for sensors at every stage
bit_list = []

neighbour_list.append(-1)
bit_list.append(-1)
for i in range(1,44):
	t_list = []
	bits = []
	x,y = get_coord[i]

	if( get_state.has_key((x-1,y)) == True ):
		t_list.append( get_state[x-1,y] )
		bits.append(1)
	else:
		bits.append(0)

	if( get_state.has_key((x+1,y)) == True ):
		t_list.append( get_state[x+1,y] )
		bits.append(1)
	else:
		bits.append(0)

	if( get_state.has_key((x,y+1)) == True ):
		t_list.append( get_state[x,y+1] )
		bits.append(1)
	else:
		bits.append(0)

	if( get_state.has_key((x,y-1)) == True ):
		t_list.append( get_state[x,y-1] )
		bits.append(1)
	else:
		bits.append(0)

	bit_list.append(bits)
	neighbour_list.append( t_list )

# generate a random walk of t_max steps
def walker(t_max):
	state = np.random.randint(1,44)
	walk_list = []
	i = 1
	while(i <= t_max):
		walk_list.append(state)
		if(len(neighbour_list[state]) == 0):
			continue
		state = neighbour_list[ state ][ np.random.randint(0,len(neighbour_list[state]) ) ]
		i += 1
	return walk_list

# walk contains the actual robot walk
print "Enter the steps:"
t_max = int( input() )
walk = walker(t_max)

def induce_error(walk, epsilon):
	ret_list = []
	for i in range(0, len(walk)):
		# bits = bit_list[ walk[i] ]
		bits = []
		for j in range(0,4):
			u = np.random.random_sample(None)
			if( u <= epsilon ):
				bits.append(int(1- bit_list[walk[i]][j] ))
				# print "SWITCH " + str(i) + "_" + str(j)
			else:
				bits.append(int( bit_list[walk[i]][j] ))
		ret_list.append(bits)
	return ret_list

# epsilon has error prob.
print "Enter epsilon:"
epsilon = float(input())
sensor_reading = induce_error(walk, epsilon)

T_ = np.zeros((43,43))

def fill_entries():
	for i in range(1,44):
		list1 = neighbour_list[i]
		if(len(list1) == 0):
			T_[i-1][i-1] = 1
			continue
		for j in list1:
			T_[i-1][j-1] = 1.0/float(len(list1))
			# print T_[i-1][j-1]


def print_T():
	for i in range(0,43):
		for j in range(0,43):
			print (T_[i][j]),
		print "\n\n"



# function to fill T_ matrix
fill_entries()


# matrix O
O = np.zeros((t_max,43,43))

for t in range(0,t_max):
	obs = sensor_reading[t]
	for i in range(0,43):
		dit = 0
		for j in range(0,4):
			if(obs[j] != bit_list[i+1][j]):
				dit += 1
		# print dit
		O[t][i][i] = ((1.0 - epsilon)**(4.0 - dit))*((epsilon)**(dit))
		# print O[t][i][i]



# for i in range(0,43):
# 	for j in range(0,43):
# 		print (O[0][i][j]),
# 	print "\n\n"

# vector f
f = np.zeros(43)
f.fill(1.0/43.0)
# print f

f_list = []
f_list.append(f)
for t in range(0,t_max-1):
	f_ = np.matmul( O[t+1] , np.matmul(T_.T , f_list[t] ) )
	summ = 0.0
	for j in range(0,43):
		summ += f_[j]
	for j in range(0,43):
		f_[j] = f_[j] / summ
	f_list.append(f_)

# for t in range(0,t_max):
# 	for j in range(0,43):
# 		print (str(f_list[t][j])+"\t"),
# 	print "\n"

predicted_state = []
for i in range(0,len(f_list)):
	if(i == 0):
		predicted_state.append( np.random.randint(1,44) )
	else:
		predicted_state.append( 1 + np.argmax(f_list[i]) )



# viterbi algorithm

T1 = np.zeros((43,t_max))
T2 = np.zeros((43,t_max))

for i in range(0,43):
	T1[i,0] = (1.0/43.0)*O[0][i][i]

Z = np.zeros(t_max)
X = np.zeros(t_max)

for t in range(1,t_max):
	for j in range(0,43):
		maxi = 0
		max_k = 0
		for k in range(0,43):
			if( T1[k,t-1]*T_[k][j]*O[t][j][j] > maxi ):
				maxi = T1[k,t-1]*T_[k][j]*O[t][j][j]
				max_k = k
		T1[j,t] = maxi
		T2[j,t] = max_k

maxi = 0
max_k = 0
for k in range(0,43):
	if( T1[k][t_max-1] >= maxi ):
		maxi = T1[k][t_max-1]
		max_k = k

Z[t_max-1] = max_k
X[t_max-1] = max_k

for i in list(reversed(range(1, t_max))):
	Z[i-1] = T2[ int(Z[i]) ][i]
	X[i-1] = Z[i-1]

viterbi_list = []
for i in range(0,len(X)):
	viterbi_list.append( int(X[i]+1) )

# comparision of prediction at every step vs actual location
print "The random generated walk was:"
print walk
print "The location estimate at particular times:"
print predicted_state
print "Most likely"
print viterbi_list

def manhattan_distance(state1,state2):
	x1,y1 = get_coord[state1]
	x2,y2 = get_coord[state2]
	return abs(x2-x1) + abs(y2-y1)

# get error list
man_error_list = []
for i in range(0,len(walk)):
	man_error_list.append( int(manhattan_distance(walk[i],predicted_state[i])) )

plt.plot(man_error_list,'-')
plt.savefig('local_error_'+str(t_max)+'_'+str(epsilon)+'.png')
# plt.show()
plt.close()


accuracy = 0.0
for i in range(0,len(walk)):
	if(walk[i] == viterbi_list[i]):
		accuracy += 1.0
accuracy = accuracy / float(len(walk))
print "Accuracy is: "+str(accuracy*100)+"%"



# for i in range(0, len(walk)):
# 	print str( bit_list[walk[i]]) + "_" + str(sensor_reading[i])