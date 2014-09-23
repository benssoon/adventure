#!/usr/bin/python3

import gameItems
import gameMap
import inventory
import os
import shutil



LOCKED = True
UNLOCKED = False



################################################################################
#		Person class
################################################################################
class Person():
	def __init__(self, usrName, stRoom, gameName):	# Initialize with an input user name
		self.name = usrName
		self.health = 100
		self.strength = 10
		self.bag = inventory.Inventory()
		self.position = stRoom	# Start a new player at home
		self.game = gameName	# For recovery purposes
	
	#-------------------------------------------------------------------------------
	#		Print location
	#-------------------------------------------------------------------------------
	def locate(self):
		print("You are in the %s."%self.position.name)

	#-------------------------------------------------------------------------------
	#		Print description
	#-------------------------------------------------------------------------------
	def hint(self):
		print(self.position.description)

	#-------------------------------------------------------------------------------
	#		Look around
	#-------------------------------------------------------------------------------
	def look(self):
		if self.position.objects.items[0] == 0:
			print(self.position.objects.items[1])
		else:
			print("\nContents of the room:")
			print()
			for item in self.position.objects.items:
				print(item.name)
			print()

	#-------------------------------------------------------------------------------
	#		Take inventory
	#-------------------------------------------------------------------------------
	def takeInventory(self):
		if self.bag.items[0] == 0:
			print("There is nothing in your bag.")
		else:
			print("\nContents of your bag:")
			print()
			for item in self.bag.items:
				print(item.name)
			print()

	#-------------------------------------------------------------------------------
	#		Move
	#-------------------------------------------------------------------------------
	def move(self, direction):
		for d in ['north', 'south', 'east', 'west']:
			if direction == d[0]:
				direction = d
		if eval("self.position.%s"%direction) != None:
			if self.position.locks[direction] == UNLOCKED:				# If the specified door is unlocked, move that direction.
				self.position = eval("self.position.%s"%direction)
				self.hint()
			elif 'coffee' not in self.position.objects.items and 'coffee' not in self.bag.items:
				print("The door is locked. Look for a key somewhere.")
			else:
				print("That door is locked.")
		else:
			print("There is nothing in that direction.")

	#-------------------------------------------------------------------------------
	#		Pick up object
	#-------------------------------------------------------------------------------
	def pickUp(self, item):
		for thing in self.position.objects.items:
			if item.name == thing.name:
				if item.weight <= self.strength:
					self.bag.add(item)
					self.position.kill(item)
					if item.name == 'desk':
						print("You pick up a tiny %s"%item.name)
					else:
						print("You pick up a %s"%item.name)
					return
				else:
					print("The %s is too heavy to carry. But maybe there is a way you could make it lighter......"%item.name)
					for thing in self.position.objects.items:			# Since someone could try to pick up a heavy object multiple times
						if self.position.objects.items[0] != 0:			# with no success, test to make sure there isn't already a
							if 'shrinker' == thing.name:			# shrinker in the room.
								return
					for thing in self.bag.items:					# Do the same with the bag, to make sure it doesn't exist at all.
						if self.bag.items[0] != 0:
							if thing == 0 or 'shrinker' == thing.name:
								return
					shrinker = gameItems.Shrinker()
					self.position.add(shrinker)
					return
		print("That item is not here.")

	#-------------------------------------------------------------------------------
	#		Use an item
	#-------------------------------------------------------------------------------
	def use(self, item):
		for thing in self.bag.items:
			if item.name == thing.name:
				if item.name == 'coffee':
					self.health += item.use()
					if self.position.name == 'bedroom':
						print("You feel a great burst of energy! Your mind clears and you look around. You are indeed in your own room, but you notice that all of your furniture is missing! Try to find it.\nYou now have an empty coffee mug.")
						self.position.description = "Try to find all of your furniture."
					else:
						print("You feel invigorated.")
					self.bag.kill(item)
					mug = gameItems.Mug()
					self.bag.add(mug)
					break
				elif item.name == 'mug':
					key = item.use()
					self.bag.add(key)
					self.bag.kill(item)
					break
				elif item.name == 'key':
					door = input("Which door would you like to unlock (north, south, east, or west)? ")
					for d in ['north', 'south', 'east', 'west']:
						if door == d[0]:
							door = d
					door = [self.position.name, door]
					doorState = item.use(self.position, door)
					if doorState == UNLOCKED:
						self.bag.kill(item)
					break
				elif item.name == 'shrinker':
					shrinkee = input("What would you like to shrink? ")
					none = 0
					for thing in self.bag.items:
						if shrinkee == thing.name:
							shrinkee = thing
							none = 0
						else:
							none = 1
					for thing in self.position.objects.items:
						if shrinkee == thing.name:
							shrinkee = thing
							none = 0
						else:
							none = 1
					if none == 1:
						print("You do not have that item and it is not nearby.")
					else:
						item.use(shrinkee, self.strength)
					break
				elif item.name == 'desk':
					if item.inside.items[0] == 0:
						print("You cannot use that right now.")
					else:
						key = item.use()
						self.bag.add(key)
						item.kill(key)	# Remove the key from the desk but don't get rid of the desk. You need it to win!
					break
				else:
					print("There is not yet a way to use this item.")



################################################################################
#		Game class
################################################################################
class Game():
	def __init__(self, character):
		self.game_over = False
		self.name = "AdventureGame"
		self.theMap = gameMap.Map(self.name, 1)
		self.theMap.load("characters/%s"%character)
		self.char = Person(character, self.theMap.rooms[0], self.name) # Hero is a person with the name given in the prompt
		self.commands = {
			'save':0,
			's':0,
			'inventory':1,
			'inv':1,
			'bag':1,
			'location':2,
			'loc':2,
			'where':2,
			'hint':3,
			'look':4,
			'move':5,
			'take':6,
			'use':7,
			'help':8,
			'h':8,
			'quit':9,
			'q':9
		}

	#-------------------------------------------------------------------------------
	#		Run logic
	#-------------------------------------------------------------------------------
	def run_logic(self):
		end = False
		if not self.game_over:
			self.command = -1
			self.prompt = input("What would you like to do? (Type 'help' for a list of commands) ")
			self.prompt = self.prompt.split(' ')
			try:
				self.command = self.doCommand(self.prompt[0].lower())	# Translate command into an int for easier processing. The 'lower()' makes the string comparing significantly easier and allows for many versions of one command.
			except KeyError:
				print("Invalid command.")
			del self.prompt[0]
			self.prompt = ' '.join(item for item in self.prompt).strip()
			if self.command == 0:				# Save progress
				self.save()
			elif self.command == 1:				# Take inventory
				self.char.takeInventory()
			elif self.command == 2:				# Check location
				self.char.locate()
			elif self.command == 3:				# Hint
				self.char.hint()
			elif self.command == 4:				# Look around
				self.char.look()
			elif self.command == 5:				# Move
				if self.prompt.strip() == "":
					print("Please type 'move' and an direction, separated by a space.")
					return end
				self.char.move(self.prompt)
			elif self.command == 6:				# Pick up
				item = None
				if self.prompt.strip() == "":
					print("Please type 'take' and an item name, separated by a space.")
					return end
				if self.char.position.objects.items[0] != 0:
					for thing in self.char.position.objects.items:
						if self.prompt == thing.name:
							item = thing
					if item == None:
						print("That item is not here.")
					else:
						self.char.pickUp(item)
				else:
					print(self.char.position.objects.items[1])
			elif self.command == 7:				# Use
				item = None
				if self.prompt.strip() == "":
					print("Please type 'use' and an item name, separated by a space.")
					return end
				if self.char.bag.items[0] != 0:
					for thing in self.char.bag.items:
						if self.prompt == thing.name:
							item = thing
					if item == None:
						print("You do not have that item.")
					else:
						self.char.use(item)
				else:
					print("There is nothing in your bag.")
			elif self.command == 8:				# Help
				print("""
help/h: Print the list of possible commands.
inventory/inv/bag: Check the contents of your bag.
look: Check your surroundings for items that may be useful.
location/loc/where: Check where you are.
hint: Get any information or hints regarding your location.
move [direction]: Where [direction] is north/n, south/s, east/e, or west/w. Moves you in that direction if possible.
take [item]: Where [item] is an item from your surroundings. Adds it to your inventory.
use [item]: Where [item] is an item in your bag. May use up the item, depending on what it is.
save/s: Save your progress.
quit/q: Exit to the main menu.
""")
			elif self.command == 9:				# Quit
				end = True
		return(end)	# Used for ending the loop occuring in the main method.

	#-------------------------------------------------------------------------------
	#		Commands switch
	#-------------------------------------------------------------------------------
	def doCommand(self, x):
		return self.commands[x]

	#-------------------------------------------------------------------------------
	#		Save progress
	#-------------------------------------------------------------------------------
	def save(self):
		if not os.path.exists("data/characters/%s"%(self.char.name)):
			os.mkdir("data/characters/%s"%(self.char.name))
			shutil.copytree("data/items", "data/characters/%s/items"%self.char.name)
		gfile = open("data/characters/%s/%s.game"%(self.char.name, self.char.name), "w")

		# Save game attributes
		gfile.write(str(self.game_over)+'\n')							# Game over?
		gfile.write(self.name+'\n')								# Game name

		#Save character attributes
		gfile.write(self.char.name+'\n')							# Character name
		gfile.write(str(self.char.health)+'\n')							# Character health
		if self.char.bag.items[0] == 0:
			gfile.write(','.join(str(item) for item in self.char.bag.items)+'\n')		# Converts all items in list to strings and combines them into one string with commas.
		else:
			gfile.write(','.join(str(item.name) for item in self.char.bag.items)+'\n')	# Converts all items in list to strings and combines them into one string with commas.
		gfile.write(self.char.position.name+'\n')						# Character position
		gfile.close()
		if self.char.bag.items[0] != 0:
			for item in self.char.bag.items:
				item.save("characters/%s/items"%self.char.name)
		self.theMap.save("characters/%s"%self.char.name)								# Map as it is in current game
		print("Your progress has been saved.")

	#-------------------------------------------------------------------------------
	#		Load progress
	#-------------------------------------------------------------------------------
	def load(self):
		gfile = open("data/characters/%s/%s.game"%(self.char.name, self.char.name))
		self.game_over = gfile.readline().rstrip()				# Game over?
		if self.game_over == 'False':
			self.game_over = False
		elif self.game_over == 'True':
			self.game_over = True
		self.name = gfile.readline().rstrip()					# Game name

		self.char.name = gfile.readline().rstrip()				# Character name
		self.char.health = int(gfile.readline().rstrip())			# Character health
		items = gfile.readline().rstrip().split(',')				# Character inventory items
		if items[0] == '0':
			self.char.bag.__init__()
		else:
			for item in items:
				item = gameItems.makeItem(item)
				item.load("characters/%s/items"%self.char.name)
				self.char.bag.add(item)
		self.char.position.name = gfile.readline().rstrip()			# Character position

		for room in self.theMap.rooms:				# Set the actual position of the character, rather than just the name of the position, as in the previous line.
			if room.name == self.char.position.name:
				self.char.position = room

		gfile.close()



################################################################################
#		Main
################################################################################
def main():
	theMap = gameMap.Map("Game Name", 10)
	menu = """
  (1) Create a new character
  (2) Play an existing character
  (3) Delete an existing character
  (4) Quit
"""
	done = False
	print(menu)
	choice = int(input("Select a choice from the menu: "))
	while choice != 4:
		if choice == 1:
			name = input("What name would you like? ")
			go = True
			if os.path.exists("data/characters/%s"%name):
				sure = input("This character already exists. Are you sure you'd like to overwite it? ")
				if sure in ['y','yes','Y','Yes']:
					shutil.rmtree("data/characters/%s"%name)
				else:
					go = False
			if go == True:
				os.mkdir("data/characters/%s"%name)
				shutil.copytree("data/items", "data/characters/%s/items"%name)
				shutil.copy("data/maps/AdventureGame.map", "data/characters/%s"%name)
				newGame = Game(name)
				newGame.char.hint()
				newGame.char.position.description = "Do something to clear your thoughts."
				while not done:
					done = newGame.run_logic()	# run_logic() returns a boolean value that is true when the user has typed the quit command (see switch method for details).
			else:
				print("Character not created.")
		elif choice == 2:
			name = input("What is your name? ")
			if os.path.exists("data/characters/%s"%name):
				loadGame = Game(name)
				loadGame.load()
				loadGame.char.hint()
				while not done:
					done = loadGame.run_logic()	# run_logic() returns a boolean value that is true when the user has typed the quit command (see switch method for details).
			else:
				print("Sorry, that character does not exist.")
		elif choice == 3:
			name = input("Which character would you like to delete? ")
			if os.path.exists("data/characters/%s"%name):
				sure = input("Are you sure? ")
				if sure in ['y','yes','Y','Yes']:
					shutil.rmtree("data/characters/%s"%name)
				else:
					print("Character %s not deleted."%name)
			else:
				print("Sorry, that character does not exist.")
		done = False
		print(menu)
		choice = int(input("Select a choice from the menu: "))

if __name__ == "__main__":
	main()
