#!/usr/bin/python3

import os
import gameMap
import gameItems


LOCKED = True
UNLOCKED = False



###################################################################################################################
#=====================================================
#		Main menu
#=====================================================
def mainMenu():
	menu = """
  (1) New map
  (2) Change a map
  (3) Quit
"""
	print(menu)
	option = int(input("Choose an option from the menu: "))
	return option



#=====================================================
#		Edit menu
#=====================================================
def editMenu():
	menu = """
  (1) Map name
  (2) Room attributes
  (3) Add a room
  (0) Type 0 at any time during the program to return to the previous menu
"""
	print(menu)
	choice = int(input("What would you like to change?(select a number) "))
	return choice



#=====================================================
#		Room menu
#=====================================================
def roomMenu():
	menu = """
  (1) Name
  (2) Description
  (3) Objects
  (4) Connection
"""
	print(menu)
	attribute = int(input("Which attribute would you like to edit?(enter number form list) "))
	return attribute



###################################################################################################################
#=====================================================
#		Print list of all rooms
#=====================================================
def roomsList(amap, operation):					# Operation list should be [operation, direction, room name], where direction and room name are optional. Depends on operation.
	j = 1
	print()
	for room in amap.rooms:
		print("  (%d) %s"%(j,room.name))
		j += 1
	print()
	if operation[0] == 'connect':
		direction = operation[1]
		name = operation[2]
		connection = int(input("Which room would you like to be to the %s of %s?(enter number from list) "%(direction, name)))			# Specify the room to connect to.
		return connection															# Return the room.
	elif operation[0] == 'edit':
		index = int(input("Which room would you like to edit?(enter number from list) "))
		return index																# Return the index.



#=====================================================			This method gives the user the option to connect rooms to each									^
#		Connect rooms together					of the rooms in the map.												       /|\
#=====================================================																			|
def connectRooms(amap, room):											#											|
	nsew = ['north', 'south', 'east', 'west']									# Variable for checking that the user input an actual direction.		|
	answer = input("Would you like to connect %s to another room?(y/n) "%room.name)					# Connect a room to the currently selected one?					|
	while answer != 'n':												# Loop until the user decides not to connect to another room.			|
		if answer == 'y':												# The user would like to connect a room to the selected room.		|
			direction = input("Which direction would you like to connect to?(north, south, east, west) ").lower()		# Standardize the input to work with connect().			|
			while direction not in nsew:											# Loop until the user enters an actual direction.		|
				direction = input("That is an invalid direction. Please choose from north, south, east or west: ")		# Select north, south, east or west.			|
			connection = roomsList(amap, ['connect', direction, room.name])							# List all the rooms in the map. See method above_______________|
			room.connect(direction, amap.rooms[connection-1])								# Connect the rooms.
			lock = input("Would you like to lock the door to the %s of %s?(y/n)"%(direction, room.name))
			if lock == 'y':
				room.locks[direction] = LOCKED
			elif lock == 'n':
				room.locks[direction] = UNLOCKED
			else:
				print("Invalid option.")
			answer = input("Would you like to connect %s to another room?(y/n) "%room.name)					# Connect a room to the currently selected one?
		else:														# The user selected something other than 'y' or 'n'.
			answer = input("Invalid option. Please select 'y' or 'n': ")						# Select 'y' or 'n'.
	return(room)



#=====================================================
#		Make a new map
#=====================================================
def new():
	name = input("What would you like to call your map? ")
	size = int(input("How many rooms are there? "))
	themap = gameMap.Map(name, size)

	i = 1
	for room in themap.rooms:
		rmName = input("What would you like to call room %d? "%i)
		room.name = rmName
		i += 1
	for room in themap.rooms:
		room = connectRooms(themap, room)
	return(themap)



#=====================================================
#		Change map name
#=====================================================
def changeName(amap):
	name = input("The map name is currently %s. What would you like to change it to? "%amap.name)
	amap.name = name
	return amap



#=====================================================
#		Add or remove an item
#=====================================================
def addRemove(room, action):
	if action == 1:
		item = input("What is the item you would like to add? ")
		if item == '0':
			return
		else:
			item = gameItems.makeItem(item)
			item.load('items')
			room.add(item)
		action = int(input("Would you like to 1. add an item to or 2. remove an item from the room? "))
	elif action == 2:
		if room.objects.items[0] == 0:
			print("\n%s\n"%room.objects.items[1])
		else:
			print()
			for item in room.objects.items:
				print(item.name)
			print()
			item = input("What is the item you would like to remove? ")
			if item == '0':
				return
			room.kill(item)
		action = int(input("Would you like to 1. add an item to or 2. remove an item from the room? "))
	else:
		print("Invalid selection.")
		action = int(input("Would you like to 1. add an item to or 2. remove an item from the room? "))
	return action



#=====================================================
#		Change attributes
#=====================================================
def attributeChange(amap):
	index = roomsList(amap, ['edit'])			# Get the index of the room the user wants to edit.
	while index != 0:					# 0 should quit to the previous menu (edit menu).
		if index  <= amap.size and index >= 0:			# Room is in map.
			room = amap.rooms[index-1]				# Set the room to a variable.
			attribute = roomMenu()					# Ask the user to select which attribute they want to change.
			while attribute != 0:					# 0 should quit up to the previous menu (rooms list).

		############### Name ###############
				if attribute == 1:
					name = input("The name is currently %s. What would you like to change the name to? "%room.name)
					if name == '0':
						break
					room.name = name
					attribute = roomMenu()

		############### Description ###############
				elif attribute == 2:
					description = input("The description is currently as follows:\n\n%s\n\nWhat would you like to change it to? "%room.description)
					if description == '0':
						break
					room.description = description
					attribute = roomMenu()

		############### Objects ###############
				elif attribute == 3:
					action = int(input("Would you like to 1. add an item to or 2. remove an item from the room? "))
					while action != 0:	# Quit to previous menu (room menu)
						action = addRemove(room, action)
					attribute = roomMenu()

		############### Connection ###############
				elif attribute == 4:
					room = connectRooms(amap, room)
					attribute = roomMenu()
				else:
					print("Invalid selection.")
					attribute = roomMenu()
			index = roomsList(amap, ['edit'])
		else:
			print("Invalid selection.")
			index = roomsList(amap, ['edit'])
	return amap



#=====================================================
#		Change elements of a map
#=====================================================
def change(amap):
	choice = editMenu()
	while choice != 0:

	########### Change map name ###########
		if choice == 1:
			amap = changeName(amap)
			choice = editMenu()

	########### Change room attributes ###########
		elif choice == 2:
			amap = attributeChange(amap)
			choice = editMenu()

	########### Add a room ###########
		elif choice == 3:
			name = input("What would you like the room to be called? ")
			index = amap.size
			room = Room(name, index)
			amap.rooms.append(room)
			amap.size += 1
			room = connectRooms(amap, room)
			choice = editMenu()
		else:
			print("Invalid option.")
			choice = editMenu()
	return(amap)



#=====================================================
#		Draw the map
#=====================================================
def draw(amap):
	for i in range(0,amap.size*2):
		for j in range(0,amap.size*2):
			print(0,end=" ")
		print()



#=====================================================
#		Main
#=====================================================
def main():
	option = mainMenu()
	while option != 3:
		if option == 1:
			themap = new()
			themap.save('maps')	# Save in the maps directory
			option = mainMenu()
		elif option == 2:
			print()
			for item in os.listdir("data/maps"):
				print(item)
			print()
			filename = input("Which map would you like to change? ")
			while "%s.map"%filename not in os.listdir("data/maps"):
				filename = input("The specified .map file does not exist. Please try another: ")
			themap = gameMap.Map(filename, 0)
			themap.load('maps')
			themap = change(themap)
			themap.save('maps')
			option = mainMenu()
		else:
			print("Invalid selection.")
			option = mainMenu()

if __name__ == "__main__":
	main()
