import math



alpha = 1
beta = 2
ro = .5
eta = [[0.0 for i in range(14)] for i in range(14)]

def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist


pheromones = [[-1.0, 20.0, 14.0, 10.0, 2.0, 7.0, 3.0, 20.0, 3.0, 40.0, 1.0, 22.0, 6.0, 20.0],[20.0, -1.0, 2.0, 5.0, 4.0, 33.0, 10.0, 30.0, 3.0, 12.0, 42.0,
19.0, 8.0, 21.0],[14.0, 2.0, -1.0, 10.0, 3.0, 22.0, 10.0, 3.0, 2.0, 33.0, 23.0, 7.0, 27.0, 5.0],[10.0, 5.0, 10.0, -1.0, 6.0, 20.0, 20.0, 11.0, 21.0, 21.0,
73.0, 6.0, 14.0, 20.0],[2.0, 4.0, 3.0, 6.0, -1.0, 1.0, 2.0, 40.0, 12.0, 18.0, 17.0, 25.0, 30.0, 7.0],[7.0, 33.0, 22.0, 20.0, 1.0, -1.0, 40.0, 5.0, 3.0, 2.0,
3.0, 11.0, 10.0, 33.0],[3.0, 10.0, 10.0, 20.0, 2.0, 40.0, -1.0, 8.0, 4.0, 7.0, 8.0, 24.0, 5.0, 13.0],[20.0, 30.0, 3.0, 11.0, 40.0, 5.0, 8.0, -1.0, 9.0, 11.0,
4.0, 12.0, 3.0, 19.0],[3.0, 3.0, 2.0, 21.0, 12.0, 3.0, 4.0, 9.0, -1.0, 12.0, 42.0, 33.0, 21.0, 18.0],[40.0, 12.0, 33.0, 21.0, 18.0, 2.0, 7.0, 11.0, 12.0,
-1.0, 6.0, 3.0, 17.0, 4.0],[1.0, 42.0, 23.0, 73.0, 17.0, 3.0, 8.0, 4.0, 42.0, 6.0, -1.0, 6.0, 26.0, 8.0],[22.0, 19.0, 7.0, 6.0, 25.0, 11.0, 24.0, 12.0, 33.0,
1.0, 6.0, -1.0, 20.0, 15.0],[6.0, 8.0, 27.0, 14.0, 30.0, 10.0, 5.0, 3.0, 21.0, 17.0, 26.0, 20.0, -1.0, 18.0],[20.0, 21.0, 5.0, 20.0, 7.0, 33.0, 13.0, 19.0,
18.0, 4.0, 8.0, 15.0, 18.0, -1.0]] 

tour = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]] 

visited = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

nodes = [[82, 76], [96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39],
               [14, 24], [12, 39], [3, 82], [5, 10], [98, 52], [84, 25]]


for i in range(0,len(nodes)):
	for j in range(0,len(nodes)):
		if distance(nodes[i][0],nodes[i][1],nodes[j][0],nodes[j][1]):
			eta[i][j] = 1.0/distance(nodes[i][0],nodes[i][1],nodes[j][0],nodes[j][1])
			# print eta[i][j]


def isNeighbour(i,j):
	if pheromones[i][j] < 0:
		return 0
	else:
		return 1

def allNotVisited():
	for col in range(0,len(visited)):
		if not visited[col]:
			return 1
	return 0

def calculate_prob(x,y):
	numerator = pheromones[x][y]**alpha * eta[x][y]**beta
	denominator = 0.0
	for n in range(0,len(nodes)):
		if x != n:
			# print pheromones[x][n]
			# print eta[x][n]
			denominator = denominator + pheromones[x][n]**alpha * eta[x][n]**beta
	# print denominator
	if denominator != 0.0:
		return numerator / denominator
	else:
		print "Exception!! division by zero"

def tour_const():
	epoch = 3
	index = 0
	while epoch:
		# for each ant do following
		for k in range(0,len(nodes)):
			curr = k
			visited[curr] = 1  
			iteration = 0
			while allNotVisited():
				maxi = 0
				for j in range(0,len(nodes)):
					if isNeighbour(curr,j) and visited[j] == 0:
						# print curr,j
						prob = calculate_prob(curr,j)
						if maxi < prob:
							maxi = prob
							next_node = j
				# update next neighbour
				curr = next_node
				visited[curr] = 1
				# keep path
				tour[k][iteration] = curr
				iteration = iteration + 1
			# print tour[k][len(nodes)-1]
			tour[k][len(nodes)-1] = k  # source added at last pos
			# reset visited for next ant
			for x in range(0,len(visited)):
			 	visited[x] = 0
		# Update pheromone (decay) to all path
		for x in range(0,len(nodes)):
			for y in range(0,len(nodes)):
				pheromones[x][y] = (1 - ro)*pheromones[x][y]

		# Add pheromone to the tour
		for x in range(0,len(nodes)):
			curr = x
			dist = 0
			for y in xrange(0,len(nodes)):
				dist = dist + distance(nodes[curr][0],nodes[curr][1],nodes[tour[x][y]][0],nodes[tour[x][y]][1])
				curr = tour[x][y]
				# print 1.0/dist
			for y in range(0,len(nodes)):
				pheromones[curr][tour[x][y]] = pheromones[curr][tour[x][y]] + 1.0/dist
		# break
		# compute best path from tour matrix
		best = float("inf")
		# index = 0
		for x in xrange(0,len(nodes)):
			curr = x
			cost = 0
			for y in xrange(0,len(nodes)):
				cost = cost + distance(nodes[curr][0],nodes[curr][1],nodes[tour[x][y]][0],nodes[tour[x][y]][1])
				curr = tour[x][y]
			if cost < best :
				best = cost
				index = x
		# print the best path
		# for x in xrange(0,len(nodes)):
		#  	print tour[index][x],

		# print ""
		epoch = epoch - 1
		#break
	for x in xrange(0,len(nodes)):
		print tour[index][x],


tour_const()
