#!/usr/bin/env python2
import math
import pygame
import random
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


#diferent types of nodes and their locations
# depot = [[100,400]]
# disposal = [[700,400]]
# customer = [[350, 400],[450, 100],[450, 600],[650, 200],[650, 500]]

# speed = 300
# garbage range rand(1,80)

class AntColony(object):
		
	pygame.init()

	BLACK = (  0,   0,   0)
	WHITE = (255, 255, 255)
	BLUE =  (  0,   0, 255)
	GREEN = (  0, 255,   0)
	RED =   (255,   0,   0)
	BACKGROUND = (0,   0,   0)
	CUSTOMER = (156,39,176)
	DISPOSAL = (0,150,136)
	DEPOT = (183,28,28)
	BASIC_LINE = (33,150,243)
	TOUR_LINE = (255,152,0)
	BEST_LINE = (244,67,54)
	TEXT = (255, 255, 255)

	color = [BLACK, BLUE, GREEN, RED]
	myFont = pygame.font.SysFont("Roboto", 18)

	# Set the height and width of the screen
	size = [1000, 1000]
	

	# global constants
	alpha = 1
	beta = 2
	ro = .9

	#capacity of each vehicle
	capacity = 0

	#diferent types of nodes and their locations
	depot = []
	disposal = []
	customer = []
	nodes = []
	network = []
	time_window = []
	node_type = []

	speed = 300
	visited = [] # depot initially visited
	service_time = 2.0
	garbage = []
	travel_time = []
	pheromones = []
	eta = []
	screen = any
	def __init__(self, vehicle_capacity,node,node_ty,time_window):
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Vehicular routing")
		super(AntColony, self).__init__()
		self.time_window = time_window
		self.capacity = vehicle_capacity
		self.node_type = node_ty
		print "node and type: "
		for x in xrange(0,len(node)):
			print node[x], node_type[x],

		for x in xrange(0,len(node)):
			if self.node_type[x] == 1:
				self.customer.append(node[x])
			if self.node_type[x] == 2:
				self.disposal.append(node[x])
			if self.node_type[x] == 3:
				self.depot.append(node[x])

		self.network.append(self.depot[0])
		for x in xrange(0,len(self.customer)):
			self.network.append(self.customer[x])

		self.nodes.append(self.depot[0])
		for x in xrange(0,len(self.customer)):
			self.nodes.append(self.customer[x])
		for x in xrange(0,len(self.disposal)):
			self.nodes.append(self.disposal[x])

		for x in xrange(0,len(self.network)):
			self.visited.append(0)


	def Initialize(self):
		#customer time window
		self.travel_time = [[0.0 for i in range(len(self.nodes))] for i in range(len(self.nodes))]
		# service time at each node
		self.pheromones = [[1.0 for i in range(len(self.nodes))] for i in range(len(self.nodes))]
		# initializing eta values (1/dist) for each pair of nodes in network
		self.eta = [[0.0 for i in range(len(self.network))] for i in range(len(self.network))]
		for x in xrange(0,len(self.nodes)):
			for y in xrange(0,len(self.nodes)):
				self.travel_time[x][y] = self.distance(self.nodes[x][0],self.nodes[x][1],self.nodes[y][0],self.nodes[y][1])/self.speed
				print self.travel_time[x][y],
			print ""

		#garbage amount initialization
		self.garbage.append(0) # for depot
		for x in xrange(1,len(self.network)):
			self.garbage.append(random.randint(1,self.capacity/2))

		# pheromone for all 
		for x in xrange(0,len(self.nodes)):
			for y in xrange(0,len(self.nodes)):
				if x == y:
					self.pheromones[x][y] = -1.0
		# attractive variable 
		for i in range(0,len(self.network)):
			for j in range(0,len(self.network)):
				if self.distance(self.network[i][0],self.network[i][1],self.network[j][0],self.network[j][1]):
					self.eta[i][j] = 1.0/self.distance(self.network[i][0],self.network[i][1],self.network[j][0],self.network[j][1])
	 
	def create_node(self):
		for x in xrange(0,len(self.nodes)):
			if self.node_type[x] == 1:
				pygame.draw.rect(self.screen, self.CUSTOMER , [self.nodes[x][0], self.nodes[x][1], 30,30])
				pos = self.myFont.render(str(x), 3, self.TEXT)
			if self.node_type[x] == 2:
				pygame.draw.rect(self.screen, self.DISPOSAL , [self.nodes[x][0], self.nodes[x][1], 30,30])
				pos = self.myFont.render(str(x), 3, self.TEXT)
			if self.node_type[x] == 3:
				pygame.draw.rect(self.screen, self.DEPOT , [self.nodes[x][0], self.nodes[x][1], 30,30])
				pos = self.myFont.render(str(x), 3, self.TEXT)
			self.screen.blit(pos, (self.nodes[x][0], self.nodes[x][1]))
		pygame.display.flip()		

	def reset_color(self):
		for x in xrange(0,len(self.nodes)):
			for y in xrange(0,len(self.nodes)):
				pygame.draw.line(self.screen, self.BASIC_LINE, [self.nodes[x][0], self.nodes[x][1]], [self.nodes[y][0],self.nodes[y][1]], 2)
		pygame.display.flip()

	def reset_text(self,tour):
		prev = tour[0]
		index = 0
		for x in xrange(1,len(tour)):
			pos = self.myFont.render(str(self.pheromones[index][x]), 3, self.BLACK)
			if abs(prev[1] - tour[x][1])/2 > 400:
				self.screen.blit(pos, ((prev[0] + tour[x][0])/2, (prev[1] + tour[x][1])/2 + 2))
			else:
				self.screen.blit(pos, ((prev[0] + tour[x][0])/2, (prev[1] + tour[x][1])/2 - 2))
			index = x
			prev = tour[x]
			pygame.display.flip()		

	def distance(self,x1, y1, x2, y2):
	    # Manhattan distance
	    dist = abs(x1 - x2) + abs(y1 - y2)
	    return dist

	def isDepot(self,node):
		for x in xrange(0,len(self.depot)):
			if node[0] == self.depot[x][0] and node[1] == self.depot[x][1]:
				return 1
		return 0
	def isDisposal(self,node):
		for x in xrange(0,len(self.disposal)):
			if node[0] == self.disposal[x][0] and node[1] == self.disposal[x][1]:
				return 1
		return 0

	def isPerfectNeighbour(self,start_time,remaining,i,j):
		if i != j:
			total_time = start_time + self.travel_time[i][j]
			if total_time >= self.time_window[j][0] and total_time <= self.time_window[j][1] and remaining >= self.garbage[j]:
				return 1
			else:
				return 0
		else:
			return 0

	def isNeighbour(self,start_time,remaining,i,j):
		if i != j:
			total_time = start_time + self.travel_time[i][j]
			if total_time <= self.time_window[j][1] and remaining >= self.garbage[j]:
				return 1
			else:
				return 0
		else:
			return 0

	def allNotVisited(self):
		for col in range(0,len(self.visited)):
			if (not self.visited[col]):
				return 1
		return 0

	def attract_coeff(self,x,y):
		return self.eta[x][y]

	def calculate_prob(self,neighbour_set,x,y):
		numerator = self.pheromones[x][neighbour_set[y]]**self.alpha * self.eta[x][neighbour_set[y]]**self.beta
		denominator = 0.0
		for n in range(0,len(neighbour_set)):
			if x != neighbour_set[n]:
				denominator = denominator + self.pheromones[x][neighbour_set[n]]**self.alpha * self.eta[x][neighbour_set[n]]**self.beta
		if denominator != 0.0:
			return numerator / denominator
		else:
			print "Exception!! division by zero"

	def isNotEmpty(self,x):
		if(len(x)):
			return 1
		else:
			return 0

	def  nearest_disposal(self,curr):
		mini = self.distance(self.network[curr][0], self.network[curr][1] , self.disposal[0][0], self.disposal[0][1])
		index = 0
		for x in xrange(1,len(self.disposal)):
			temp = self.distance(self.network[curr][0], self.network[curr][1] , self.disposal[x][0], self.disposal[x][1])
			if mini > temp:
				mini = temp
				index = x
		return index

	# get positon of tour node
	def getpos(self,t):
		for x in xrange(0,len(self.nodes)):
			if self.nodes[x][0] == t[0] and self.nodes[x][1] == t[1]:
				return x

	def tour_const(self):
		self.Initialize()
		epoch = 3
		min_dist = 10000
		# keeps best tour calculated after each epoch
		best_tour = []
		clock = pygame.time.Clock()
		self.screen.fill(self.BACKGROUND)
		self.create_node()
		self.reset_color()
		pygame.draw.rect(self.screen, self.CUSTOMER , [50, 50, 30,30])
		cus = self.myFont.render("Customer Node",1, self.CUSTOMER)
		self.screen.blit(cus,(100,60))
		pygame.draw.rect(self.screen, self.DISPOSAL , [50, 90, 30,30])
		dis = self.myFont.render("Disposal Node",1, self.DISPOSAL)
		self.screen.blit(dis,(100,100))
		pygame.draw.rect(self.screen, self.DEPOT , [50, 130, 30,30])
		depo = self.myFont.render("Depot Node",1, self.DEPOT)
		self.screen.blit(depo,(100,140))
		pygame.display.flip()

		distance_per_epoch = []
		while epoch:
			flag = 0
			start_time = 0.0
			curr = 0 # initially depot
			self.visited[curr] = 1
			next_node = 0
			remaining = self.capacity
			tour = []
			tour.append(self.depot[0])
			new_dist = 0
			while self.allNotVisited():
				perfect_neighbour_set = []
				neighbour_set = []
				# print "start_time: {}".format(start_time)
				# print "remaining : {}".format(remaining)
				for x in xrange(0,len(self.network)):
					# find all neighbour of x
					if self.isPerfectNeighbour(start_time,remaining,curr,x) and self.visited[x] == 0:
						perfect_neighbour_set.append(x)
				# if neighbour set not empty select next node
				if self.isNotEmpty(perfect_neighbour_set):
					print "Perfect neighbours: "
					for x in xrange(0,len(perfect_neighbour_set)):
						print "{} --> {}".format(curr,perfect_neighbour_set[x])
					q = random.uniform(0,1)
					maxi = 0.0
					if q > 0.5:
						for j in range(0,len(perfect_neighbour_set)):
							prob = self.calculate_prob(perfect_neighbour_set,curr,j)
							print "perfect node: {} prob : {}".format(perfect_neighbour_set[j],prob)
							if maxi < prob:
								maxi = prob
								next_node = perfect_neighbour_set[j]

					# randomly choosing for exploration
					else:
						for j in range(0,len(perfect_neighbour_set)):
							prob = self.attract_coeff(curr,perfect_neighbour_set[j])
							print "perfect node: {} prob : {}".format(perfect_neighbour_set[j],prob)
							if maxi < prob:
								maxi = prob
								next_node = perfect_neighbour_set[j]

					print "next node perfect nei: {}".format(next_node)
					# update next neighbour
					start_time = start_time + self.travel_time[curr][next_node] + self.service_time
					remaining = remaining - self.garbage[next_node]
					curr = next_node
					self.visited[curr] = 1
					# keep path
					tour.append(self.network[curr])

				else:
					for x in xrange(0,len(self.network)):
						if self.isNeighbour(start_time,remaining,curr,x) and self.visited[x] == 0:
							neighbour_set.append(x)

					if self.isNotEmpty(neighbour_set):
						print "Simple neighbours: "
						for x in xrange(0,len(neighbour_set)):
							print "{} --> {}".format(curr,neighbour_set[x])
						q = random.uniform(0,1)
						maxi = 0.0
						if q > 0.5:
							for j in range(0,len(neighbour_set)):
								prob = self.calculate_prob(neighbour_set,curr,j)
								print "simple node: {} prob : {}".format(neighbour_set[j],prob)
								if maxi < prob:
									maxi = prob
									next_node = neighbour_set[j]
						
						# randomly choosing for exploration
						else:
							for j in range(0,len(neighbour_set)):
								prob = self.attract_coeff(curr,neighbour_set[j])
								print "simple node: {} prob : {}".format(neighbour_set[j],prob)
								if maxi < prob:
									maxi = prob
									next_node = neighbour_set[j]

						# update next neighbour
						print "next node simple nei: {}".format(next_node)
						start_time = self.time_window[next_node][0] + self.service_time
						remaining = remaining - self.garbage[next_node]
						curr = next_node
						self.visited[curr] = 1
						# keep path
						tour.append(self.network[curr])
					else:
						for x in xrange(1,len(self.network)):
							if remaining >= self.garbage[x]:
								break
						if x == len(self.customer):
							# goto disposal
							remaining = self.capacity
							# find nearest disposal
							disp = self.nearest_disposal(curr)
							tour.append(self.disposal[disp])
							pos = self.getpos(self.disposal[disp])
							start_time = start_time + self.travel_time[curr][pos]*2 + self.service_time
						else:
							# print "[curr] : before comimg to depot : {}".format(curr)
							# Use another vehicle to satisfy other customers
							start_time = 0.0
							curr = 0
							remaining = self.capacity
							tour.append(self.depot[0])
							
				for x in xrange(0,len(tour)):
					if self.isDepot(tour[x]) and not(x == 0):
						print "Car change --> ",
					if self.isDisposal(tour[x]):
						print "Going to disposal --> ",
					print "{} --> ".format(tour[x]),
				print ""

				# prev = tour[0]
				# index = 0
				# for x in xrange(1,len(tour)):
				# 	pos = getpos(tour[x])
				# 	pygame.draw.line(self.screen, self.TOUR_LINE, [prev[0], prev[1]],[tour[x][0],tour[x][1]], 2)
				# 	pos = self.myFont.render(str(self.pheromones[index][x]), 3, self.TEXT)
				# 	if abs(prev[1] - tour[x][1])/2 > 400:
				# 		self.screen.blit(pos, ((prev[0] + tour[x][0])/2, (prev[1] + tour[x][1])/2 + 2))
				# 	else:
				# 		self.screen.blit(pos, ((prev[0] + tour[x][0])/2, (prev[1] + tour[x][1])/2 - 2))
				# 	index = x
				# 	prev = tour[x]
				# 	pygame.display.flip()
				# 	pygame.time.wait(1000) # Wait one second between frames.
				# self.reset_text(tour)
			# reset self.visited for next epoch
			for x in xrange(0,len(self.visited)):
				self.visited[x] = 0
			# Update pheromone (decay) to all path
			for x in range(0,len(self.nodes)):
				for y in range(0,len(self.nodes)):
					self.pheromones[x][y] = (1 - self.ro)*self.pheromones[x][y]

			# Add pheromone to the tour
			dist = 0
			prev_node = self.nodes[0]
			for x in range(0,len(tour)):
				dist = dist + self.distance(prev_node[0],prev_node[1],tour[x][0],tour[x][1])
				prev_node = tour[x]

			prev_pos = 0
			for y in range(0,len(tour)):
				pos = self.getpos(tour[y])
				if not self.isDepot(tour[y]):	
					self.pheromones[prev_pos][pos] = self.pheromones[prev_pos][pos] + 1.0/dist
				prev_pos = pos 

			# compute best tour
			new_dist = 0
			prev_node = self.nodes[0]
			for x in range(0,len(tour)):
				if not self.isDepot(tour[x]):
					new_dist = new_dist + self.distance(prev_node[0],prev_node[1],tour[x][0],tour[x][1])
				prev_node = tour[x]
			if min_dist > new_dist:
				min_dist = new_dist
				best_tour = tour

			# keep epoch and corresponding minimum distance 
			distance_per_epoch.append([epoch,new_dist])

			print"----------------------------------------------------------------------------------------------------"
			epoch = epoch - 1
			self.reset_color()					
		
		# print best tour 
		for x in xrange(0,len(best_tour)):
			if self.isDepot(best_tour[x]) and not(x == 0):
				print "Car change --> ",
			if self.isDisposal(best_tour[x]):
				print "Going to disposal --> ",
			print "{} --> ".format(best_tour[x]),
		print ""

		print "Changes in path dist: "
		for x in xrange(0,len(distance_per_epoch)):
			print distance_per_epoch[x] ,

		prev = best_tour[0]
		index = 0
		for x in xrange(1,len(best_tour)):
			pygame.draw.line(self.screen, self.BEST_LINE, [prev[0], prev[1]],[best_tour[x][0],best_tour[x][1]], 3)
			# pos = self.myFont.render(str(self.pheromones[index][x]), 3, self.TEXT)
			# if abs(prev[1] - tour[x][1])/2 > 400:
			# 	self.screen.blit(pos, ((prev[0] + best_tour[x][0])/2, (prev[1] + best_tour[x][1])/2 + 2))
			# else:
			# 	self.screen.blit(pos, ((prev[0] + best_tour[x][0])/2, (prev[1] + best_tour[x][1])/2 - 2))
			# index = x
			prev = best_tour[x]
			pygame.display.flip()
			pygame.time.wait(1000) # Wait one second between frames.

class LabelWindow(Gtk.Window):

	vehicle_capacity = 80
	node = []
	node_type = []
	ntype = 1
	time_window = []
	depot_set = 0
	cust_count = 0
	disp_count = 0
	depo_count = 0

	def __init__(self):
	    Gtk.Window.__init__(self, title="Create Graph")
	    hbox = Gtk.Box(spacing=10)
	    hbox.set_homogeneous(False)

	    hboxTop = Gtk.Box(spacing=1)
	    hboxSecondTop = Gtk.Box(spacing=1)
	    hboxMiddle = Gtk.Box(spacing=1)
	    hboxSecondBottom = Gtk.Box(spacing=1)
	    hboxBottom = Gtk.Box(spacing=1)

	    container_vbox_inside_hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    container_vbox_inside_hbox.set_homogeneous(False)

	    hbox.pack_start(container_vbox_inside_hbox,True,True,0)

	    container_vbox_inside_hbox.pack_start(hboxTop, True, True, 0)
	    container_vbox_inside_hbox.pack_start(hboxSecondTop, True, True, 0)
	    container_vbox_inside_hbox.pack_start(hboxMiddle, True, True, 0)
	    container_vbox_inside_hbox.pack_start(hboxSecondBottom, True, True, 0)
	    container_vbox_inside_hbox.pack_start(hboxBottom, True, True, 0)

	    # add capacity in the second top horizontal box
	    capacity_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    capacity_left.set_homogeneous(False)
	    capacity_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    capacity_right.set_homogeneous(False)
	    
	    hboxTop.pack_start(capacity_left, True, True, 0)
	    hboxTop.pack_start(capacity_right, True, True, 0)

	    # add vehicle capacity
	    label = Gtk.Label("Vehicle capacity")
	    label.set_justify(Gtk.Justification.LEFT)
	    capacity_left.pack_start(label, True, True, 0)

	    # add entry for x-cordinate
	    self.capacity = Gtk.Entry()
	    self.capacity.set_text("80")
	    capacity_right.pack_start(self.capacity,True,True,0)

	    # add coordinates in the middle horizontal box

	    vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    vbox_left.set_homogeneous(False)
	    vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    vbox_right.set_homogeneous(False)
	    
	    hboxMiddle.pack_start(vbox_left, True, True, 0)
	    hboxMiddle.pack_start(vbox_right, True, True, 0)

	    hboxInvbox_left = Gtk.Box(spacing=10)
	    hboxInvbox_left.set_homogeneous(False)

	    vbox_left.pack_start(hboxInvbox_left,True,True,0)

	    corodinate_label = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    corodinate_label.set_homogeneous(False)
	    cordinate_entry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    cordinate_entry.set_homogeneous(False)
	    
	    hboxInvbox_left.pack_start(corodinate_label, True, True, 0)
	    hboxInvbox_left.pack_start(cordinate_entry, True, True, 0)

	    label = Gtk.Label("X-coordinate")
	    label.set_justify(Gtk.Justification.LEFT)
	    corodinate_label.pack_start(label, True, True, 0)

	    # add entry for x-cordinate
	    self.xentry = Gtk.Entry()
	    self.xentry.set_text("0")
	    cordinate_entry.pack_start(self.xentry,True,True,0)
	    
	    label = Gtk.Label("Y-coordinate")
	    label.set_justify(Gtk.Justification.LEFT)
	    corodinate_label.pack_start(label, True, True, 0)
	    
	    # add entry for y-cordinate
	    self.yentry = Gtk.Entry()
	    self.yentry.set_text("0")
	    cordinate_entry.pack_start(self.yentry,True,True,0)

	    # add radio button in vbox right of middle horizontal box
	    self.radio_customer = Gtk.RadioButton.new_with_label_from_widget(None,"Customer")
	    self.radio_customer.connect("toggled", self.on_customer_toggled)
	    vbox_right.pack_start(self.radio_customer, True, True, 0)

	    self.radio_disposal = Gtk.RadioButton.new_with_label_from_widget(self.radio_customer,"Disposal")
	    self.radio_disposal.connect("toggled", self.on_disposal_toggled)
	    vbox_right.pack_start(self.radio_disposal, True, True, 0)

	    self.radio_depot = Gtk.RadioButton.new_with_label_from_widget(self.radio_customer,"Depot")
	    self.radio_depot.connect("toggled", self.on_depot_toggled)
	    vbox_right.pack_start(self.radio_depot, True, True, 0)


	    # add time window 
	    time_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    time_left.set_homogeneous(False)
	    time_middle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    time_middle.set_homogeneous(False)
	    time_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    time_right.set_homogeneous(False)
	    
	    hboxSecondBottom.pack_start(time_left, True, True, 0)
	    hboxSecondBottom.pack_start(time_middle, True, True, 0)
	    hboxSecondBottom.pack_start(time_right, True, True, 0)
	   
	    
	    window_label = Gtk.Label("Time window")
	    window_label.set_justify(Gtk.Justification.LEFT)
	    time_left.pack_start(window_label, True, True, 0)

	    # add entry for start time
	    self.start_time = Gtk.Entry()
	    self.start_time.set_text("0")
	    time_middle.pack_start(self.start_time,True,True,0)
	    
	    # add entry for end time
	    self.end_time = Gtk.Entry()
	    self.end_time.set_text("0")
	    time_right.pack_start(self.end_time,True,True,0)

	    # add buttons 
	    node_button = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    node_button.set_homogeneous(False)
	    animate_button = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	    animate_button.set_homogeneous(False)
	    
	    hboxBottom.pack_start(node_button, True, True, 0)
	    hboxBottom.pack_start(animate_button, True, True, 0)
	   
	    
	    self.bnode = Gtk.Button.new_with_mnemonic("Add the Node")
	    self.bnode.connect("clicked", self.on_add_node_clicked)
	    node_button.pack_start(self.bnode,True,True,0)

	    self.animate = Gtk.Button.new_with_mnemonic("Call Animator")
	    self.animate.connect("clicked", self.on_animator_clicked)
	    animate_button.pack_start(self.animate,True,True,0)

	    self.add(hbox)

	def on_customer_toggled(self,radio_customer):
		self.ntype = 1
		self.bnode.set_sensitive(True)
		self.animate.set_sensitive(True)
		
	def on_disposal_toggled(self,radio_disposal):
		self.ntype = 2
		self.bnode.set_sensitive(True)
		self.animate.set_sensitive(True)

	def on_depot_toggled(self,radio_depot):
		self.ntype = 3
		self.bnode.set_sensitive(True)
		self.animate.set_sensitive(True)

	def on_add_node_clicked(self,bnode):
		if self.ntype > 0:
			# self.animate.set_sensitive(False)
			self.vehicle_capacity = int(self.capacity.get_text())
			self.node.append([int(self.xentry.get_text()),int(self.yentry.get_text())])
			self.node_type.append(self.ntype)
			self.time_window.append([float(self.start_time.get_text()),float(self.end_time.get_text())])
			print "start: {}".format(float(self.start_time.get_text()))
			print "node type : {}".format(self.ntype)
			if self.ntype == 1:
				self.cust_count = self.cust_count + 1
			if self.ntype == 2:
				self.disp_count = self.disp_count + 1
			if self.ntype == 3:
				self.depo_count = self.depo_count + 1
				self.radio_depot.set_sensitive(False)
				self.ntype = 0
			self.capacity.set_sensitive(False)			
		else:
			bnode.set_sensitive(False)

	def on_animator_clicked(self,ani):
		print self.cust_count, self.disp_count, self.depo_count
		if 	self.cust_count > 0 and self.disp_count > 0 and self.depo_count > 0:
			testObj = AntColony(self.vehicle_capacity, self.node, self.node_type,self.time_window)
			testObj.tour_const()
			ani.set_sensitive(False)
		else:
			ani.set_sensitive(False)

window = LabelWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
pygame.quit()