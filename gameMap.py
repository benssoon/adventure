#!/usr/bin/python3

import inventory
import gameItems

LOCKED = True
UNLOCKED = False

################################################################################
#		Room class
################################################################################
class Room():
	def __init__(self, rmName, index):	# Initialize with a given room name and all connecting rooms
		self.name = rmName
		self.description = "The sun is shining."
		self.objects = inventory.Inventory()
		self.connections = []
		self.north = None
		self.south = None
		self.east = None
		self.west = None
		self.locks = {'north':UNLOCKED, 'south':UNLOCKED, 'east':UNLOCKED, 'west':UNLOCKED}
		self.index = index


	#-------------------------------------------------------------------------------
	#		Connect rooms
	#-------------------------------------------------------------------------------

	def connect(self, direction, room):
		if direction == 'north':
			self.north = room
			room.south = self
			self.connections.append(room.index)
			room.connections.append(self.index)
		elif direction == 'south':
			self.south = room
			room.north = self
			self.connections.append(room.index)
			room.connections.append(self.index)
		elif direction == 'east':
			self.east = room
			room.west = self
			self.connections.append(room.index)
			room.connections.append(self.index)
		elif direction == 'west':
			self.west = room
			room.east = self
			self.connections.append(room.index)
			room.connections.append(self.index)

	#-------------------------------------------------------------------------------
	#		Add item
	#-------------------------------------------------------------------------------
	def add(self, item):
		self.objects.add(item)

	#-------------------------------------------------------------------------------
	#		Remove item
	#-------------------------------------------------------------------------------
	def kill(self, item):
		self.objects.kill(item)



################################################################################
#		Map class
################################################################################
class Map():
	def __init__(self, mapName, numRooms):	# Initialize with a given map name, start room, and map size
		self.name = mapName
		self.size = numRooms	# of rooms
		### Initialize the map with rooms ###
		self.rooms = []
		for i in range(0,self.size):
			name = "Room %d"%i
			index = i
			self.rooms.append(Room(name, index))

	#-------------------------------------------------------------------------------
	#		Save map
	#-------------------------------------------------------------------------------
	def save(self, directory):
		mfile = open("data/%s/%s.map"%(directory, self.name),"w")
		mfile.write(self.name+'\n')
		mfile.write(str(self.size)+'\n')
		for room in self.rooms:
			mfile.write(room.name+'\n')							# Room name
			mfile.write(str(room.index)+'\n')						# Room index number
			mfile.write(room.description+'\n')						# Room description
			if room.objects.items[0] == 0:
				mfile.write(','.join(str(item) for item in room.objects.items)+'\n')	# List of objects in room, separated by commas
			else:
				mfile.write(','.join(item.name for item in room.objects.items)+'\n')	# List of objects in room, separated by commas
			mfile.write(','.join(str(index) for index in room.connections)+'\n')		# List of room connections, separated by commas
			if room.north != None:								# Connection to the north
				mfile.write(str(room.north.index)+'\n')
			else:
				mfile.write('None\n')
			if room.south != None:								# Connection to the south
				mfile.write(str(room.south.index)+'\n')
			else:
				mfile.write('None\n')
			if room.east != None:								# Connection to the east
				mfile.write(str(room.east.index)+'\n')
			else:
				mfile.write('None\n')
			if room.west != None:								# Connection to the west
				mfile.write(str(room.west.index)+'\n')
			else:
				mfile.write('None\n')
			mfile.write(str(room.locks['north']))						# Lock on north door
			mfile.write('\n')
			mfile.write(str(room.locks['south']))						# Lock on south door
			mfile.write('\n')
			mfile.write(str(room.locks['east']))						# Lock on east door
			mfile.write('\n')
			mfile.write(str(room.locks['west']))						# Lock on west door
			mfile.write('\n')
		mfile.close()

	#-------------------------------------------------------------------------------
	#		Load map
	#-------------------------------------------------------------------------------
	def load(self, directory):
		mfile = open("data/%s/%s.map"%(directory, self.name))				#file is stored in the data/maps directory and is named after the game with which it is associated
		self.name = mfile.readline().rstrip()
		self.size = int(mfile.readline().rstrip())
		self.__init__(self.name, self.size)
		for room in self.rooms:
			room.name = mfile.readline().rstrip()
			room.index = int(mfile.readline().rstrip())
			room.description = mfile.readline().rstrip()
			items = mfile.readline().rstrip().split(',')
			if items[0] == '0':
				room.objects.__init__()
			else:
				for item in items:
					item = gameItems.makeItem(item)
					item.load("items")
					room.add(item)
			for index in mfile.readline().rstrip().split(','):
				if index == '':		#i.e. there are no rooms connected to the current one.
					break
				else:
					room.connections.append(int(index))
			north = mfile.readline().rstrip()
			if north != 'None':
				room.north = self.rooms[int(north)]
			south = mfile.readline().rstrip()
			if south != 'None':
				room.south = self.rooms[int(south)]
			east = mfile.readline().rstrip()
			if east != 'None':
				room.east = self.rooms[int(east)]
			west = mfile.readline().rstrip()
			if west != 'None':
				room.west = self.rooms[int(west)]
			for door in ['north', 'south', 'east', 'west']:
				lock = mfile.readline().rstrip()
				if lock == 'True':
					room.locks[door] = LOCKED
				elif lock == 'False':
					room.locks[door] = UNLOCKED
		mfile.close()
