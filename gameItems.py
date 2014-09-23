#!/usr/bin/python3

import inventory

LOCKED = True
UNLOCKED = False

def makeItem(x):
	return{"coffee":Coffee(), "mug":Mug(), "key":Key('none'), "desk":Desk(), "chair":Chair(), "shrinker":Shrinker()}[x]


################################################################################
#		Item class
################################################################################
class Item():
	def __init__(self):
		self.weight = 0
		self.inside = inventory.Inventory()
		self.name = None

	def add(self, item):
		self.inside.add(item)

	def kill(self, item):
		self.inside.kill(item)

	def save(self, directory):
		ifile = open("data/%s/%s.item"%(directory, self.name), "w")

		ifile.write(str(self.weight)+'\n')						# Item weight
		if self.inside.items[0] == 0:
			ifile.write(','.join(str(item) for item in self.inside.items)+'\n')	# List of objects in item, separated by commas
		else:
			ifile.write(','.join(item.name for item in self.inside.items)+'\n')	# List of objects in item, separated by commas
		ifile.close()

	def load(self, directory):
		ifile = open("data/%s/%s.item"%(directory, self.name))

		self.weight = int(ifile.readline().rstrip())
		items = ifile.readline().rstrip().split(',')					# Item inventory items
		if items[0] == '0':
			self.inside.items[0] = 0
			self.inside.items[1] = items[1]
		else:
			self.inside.__init__()
			for item in items:
				item = makeItem(item)
				self.add(item)
		ifile.close()



################################################################################
#		Coffee class
################################################################################
class Coffee(Item):
	def __init__(self):
		Item.__init__(self)
		self.name = "coffee"
		self.addictive = True
		self.speed = True
		self.weight = 2

	def use(self):
		healthBoost = 17
		return healthBoost



################################################################################
#		Mug class
################################################################################
class Mug(Item):
	def __init__(self):
		Item.__init__(self)
		key = Key(['bedroom','north'])
		self.inside.add(key)
		self.name = 'mug'
		self.weight = 2

	def use(self):
		print("You find a small key in the mug! Maybe you can use it to unlock a door.")
		return self.inside.items[0]


################################################################################
#		Key class
################################################################################
class Key(Item):
	def __init__(self, door):
		Item.__init__(self)
		self.name = 'key'
		self.weight = 1
		self.door = door

	def use(self, room, door):
		print(self.door, door)
		if self.door == door:
			room.locks[door[1]] = UNLOCKED
			print("The %s door is now unlocked."%door[1])
			return UNLOCKED
		else:
			print("The key does not unlock that door.")
			return LOCKED

	def save(self, directory):
		kfile = open("data/%s/%s.item"%(directory, self.name), "w")
		kfile.write(str(self.weight)+'\n')
		if self.door != None:
			kfile.write(','.join(str(item) for item in self.door)+'\n')	# List of objects in item, separated by commas
		else:
			kfile.write("None\n")
		kfile.close()

	def load(self, directory):
		kfile = open("data/%s/%s.item"%(directory, self.name))
		self.weight = int(kfile.readline().rstrip())
		door = kfile.readline()					# Item inventory items
		if door != "None":
			door = door.rstrip().split(',')
			self.door[0] = door[0]
			self.door[1] = door[1]
		kfile.close()


################################################################################
#		Desk class
################################################################################
class Desk(Item):
	def __init__(self):
		Item.__init__(self)
		self.weight = 18
		self.name = 'desk'
		key = Key(['bedroom','west'])
		self.inside.add(key)

	def use(self):
		print("You find a small key in the desk! Maybe you can use it to unlock a door.")
		print(self.inside.items[0].door)
		return self.inside.items[0]

	def save(self, directory):
		Item.save(self, directory)
		with open("data/%s/%s.item"%(directory, self.name), "a") as iFile:
			iFile.write(','.join(str(item) for item in self.inside.items[0].door))

	'''def load(self, directory):
		Item.load(self, directory)
		self.inside.items[0].door = line'''


################################################################################
#		Chair class
################################################################################
class Chair(Item):
	def __init__(self):
		Item.__init__(self)
		self.weight = 9
		self.name = 'chair'


################################################################################
#		Shrinker class
################################################################################
class Shrinker(Item):
	def __init__(self):
		Item.__init__(self)
		self.weight = 5
		self.name = 'shrinker'

	def use(self, item, strength):
		item.weight /= 2
		item.weight = int(item.weight)
		if item.weight <= strength:
			print("The %s is now half its original size. It is now light enough to carry!"%item.name)
		else:
			print("Although the %s is now half its original size, it is still to heavy to carry."%item.name)



coffee = Coffee()
mug = Mug()
key = Key(None)
desk = Desk()
shrinker = Shrinker()

coffee.save('items')
mug.save('items')
key.save('items')
desk.save('items')
shrinker.save('items')
