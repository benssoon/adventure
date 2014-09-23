#!/usr/bin/python3

################################################################################
#		Inventory class
################################################################################
class Inventory():
	def __init__(self):
		self.size = 0
		self.items = []
		self.items.append(0)
		self.items.append("There is nothing here.")

	#-------------------------------------------------------------------------------
	#		Add an item
	#-------------------------------------------------------------------------------
	def add(self, item):
		if self.items[0] == 0:
			self.items[0] = item
			del self.items[1]
		else:
			self.items.append(item)
		self.size += 1

	#-------------------------------------------------------------------------------
	#		Remove an item
	#-------------------------------------------------------------------------------
	def kill(self, item):
		for thing in self.items:
			if item.name == thing.name:
				self.items.remove(thing)
				self.size -= 1
				if self.size == 0:
					self.items.append(0)
					self.items.append("There is nothing here.")
				break
		else:
			print("The specified item is not here.")
