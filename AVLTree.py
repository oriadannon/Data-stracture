#id1:
#name1:oria dannon
#username1:
#id2:
#name2:shira romi
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key!=None
	
	def UpdateHeight(self): # O(1) complexity
		self.height=max(self.right.height,self.left.height)+1

	def getHeightDistanceRight(self): # O(1) complexity
		return self.height-self.right.height

	def getHeightDistanceLeft(self): # O(1) complexity
		return self.height-self.left.height

	def getHeightDistance(self,other):
		if (other==None):
			return None
		return self.height-self.other.height	
	
	def fix(self,promotions): # O(logn) complexity, (worst case is when promotion goes all the way to tree root)
		if((self.getHeightDistanceLeft()==1 and self.getHeightDistanceRight()==1)): #done with promotions
			return promotions
		if(self.getHeightDistanceLeft()==1 or self.getHeightDistanceRight()==1):
			self.UpdateHeight()#promote!
			if(self.parent==None):
				return 1
			promotions=self.parent.fix(promotions)+1 
		elif(self.getHeightDistanceLeft()==2):
			self.rotateLeft() #rotation and done
		elif(self.getHeightDistanceRight()==2):
			self.rotateRight() #rotation and done
		return promotions
	
	def rotateRight(self): # O(1) complexity
		newfather=self.left
		if(newfather.getHeightDistanceLeft()==2):#in case of double-rotation
			newfather.rotateLeft()
			newfather=newfather.parent
		self.left=newfather.right
		newfather.right=self
		newfather.parent=self.parent
		if(self.parent!=None):
			if(self.parent.right==self):
				self.parent.right=newfather
			else:
				self.parent.left=newfather
		self.parent=newfather
		self.UpdateHeight()
		newfather.UpdateHeight()


	def rotateLeft(self): # O(1) complexity
		newfather=self.right
		if(newfather.getHeightDistanceRight()==2):#in case of double-rotation
			newfather.rotateRight()
			newfather=newfather.parent
		self.right=newfather.left
		newfather.left=self
		newfather.parent=self.parent
		if(self.parent!=None):
			if(self.parent.right==self):
				self.parent.right=newfather
			else:
				self.parent.left=newfather
		self.parent=newfather
		self.UpdateHeight()
		newfather.UpdateHeight()

	def Predecessor(self):
		if(self.left.is_real_node()):
			return self.left
		traveler=self
		while(traveler.parent.right!=traveler):
			traveler=traveler.parent
		traveler=traveler.parent.left
		while(traveler.right!=None):
			traveler=traveler.right
		return traveler
		
		
		

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		return None, -1

	
	def insertion(self,key,val,newnodeplace,track):
		if(newnodeplace.key<key):
				newnodeplace.right=AVLNode(key,val)
				newnode=newnodeplace.right
		else:
				newnodeplace.left=AVLNode(key,val)
				newnode=newnodeplace.left
		newnode.left=AVLNode(None,None)
		newnode.right=AVLNode(None,None)
		newnode.UpdateHeight()
		newnode.parent=newnodeplace
		promotions=newnode.parent.fix(0) #fix the tree if needed, in wc: O(logn) complexity
		if(self.root.parent!=None): #update the tree root, in case we did rotation with tree root 
			self.root=self.root.parent
		return newnode, track, promotions


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val): # O(logn) complexity
		traveler=self.root
		prev=None # will be the father of the new node
		track=1 #counts the track
		if(traveler==None):
			newnode=AVLNode(key,val)
			newnode.left=AVLNode(None,None)
			newnode.right=AVLNode(None,None)
			newnode.UpdateHeight()
			self.root=newnode
			return newnode, track, 0
		while(traveler.is_real_node()):# search for key (O(logn) complexity)
			prev=traveler
			if(traveler.key<key):
				traveler=traveler.right
			else:
				traveler=traveler.left
			track+=1 
		return self.insertion(key,val,prev,track)


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		traveler=self.max_node()
		track=1
		while((traveler.is_real_node())and(traveler.key>key)):
			if(traveler==self.root):# if we made it to the root its the same as normal insertion
				node, partialtrack, promotions = self.insert(key,val)
				return node, partialtrack+track, promotions
			traveler=traveler.parent
			track+=1
		prev=traveler
		traveler=traveler.left
		while(traveler.is_real_node()):
			prev=traveler
			if(traveler.key>key):
				traveler=traveler.left
			else:
				traveler=traveler.right
		return self.insertion(key,val,prev,track)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		tallertree=self
		shortertree=tree2
		if(self.root.height<tree2.root.height):
			tallertree=tree2
			shortertree=self
		traveler=tallertree.root
		if(key<tallertree.root.key):
			while(traveler.height>shortertree.root.height):
				traveler=traveler.left
			xnode= AVLNode(key,val)
			xnode.right=traveler
			xnode.left=shortertree.root
			xnode.parent=traveler.parent
			traveler.parent.left=xnode
			xnode.UpdateHeight()
			xnode.parent.fix(0)
		else:
			while(traveler.height>shortertree.root.height):
				traveler=traveler.right
			xnode= AVLNode(key,val)
			xnode.left=traveler
			xnode.right=shortertree.root
			xnode.parent=traveler.parent
			if(traveler.parent!=None):
				traveler.parent.right=xnode
				self.root=tallertree.root
			else:
				self.root=xnode
				return
			xnode.UpdateHeight()
			xnode.parent.fix(0)


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):																			
		arr = []
		self.avl_to_array_rec(self.root, arr)
		return arr

	def avl_to_array_rec(self, node, arr):
		if (node.is_not_real()):
			return
		self.avl_to_array_rec(node.left, arr)
		arr.append(node.key) 
		self.avl_to_array_rec(node.right, arr)

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		traveler=self.root
		while(traveler.right.is_real_node()):
			traveler=traveler.right
		return traveler
	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None
	
def main():
	newtree=AVLTree()
	print(newtree.insert(3,"hello"))
	print(newtree.insert(2,"world"))
	print(newtree.insert(1,"!"))
	print(newtree.insert(10,"!"))
	print(newtree.insert(9,"!"))
	print(newtree.root.right.key)#9
	print(newtree.insert(6,"!"))
	print(newtree.root.key)
	print(newtree.root.right.key)
	print(newtree.root.left.key)
	print(newtree.insert(4,"!"))
	print(newtree.root.key)
	print("HELLO")
	newtree1=AVLTree()
	print(newtree1.insert(12,"hello"))
	print(newtree1.insert(15,"!"))
	print(newtree1.insert(13,"world"))
	newtree1.join(newtree,11,"join!")
	print(newtree1.root.key)
	print(newtree1.root.right.key)


if __name__ == "__main__":
    main()
