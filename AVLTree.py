#id1:
#name1:
#username1:
#id2:
#name2:
#username2:

import random

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
	
	"""Updates height of node
	"""
	def UpdateHeight(self): # O(1) complexity
		self.height=max(self.right.height,self.left.height)+1

	"""returns Height distance between this node and his right child

	@rtype: int
	@returns: Height distance between this node and his right child
	"""
	def getHeightDistanceRight(self): # O(1) complexity
		return self.height-self.right.height

	"""returns Height distance between this node and his left child

	@rtype: int
	@returns: Height distance between this node and his left child
	"""
	def getHeightDistanceLeft(self): # O(1) complexity
		return self.height-self.left.height
	
	"""fix tree after node/tree insertion 

	@type promotions: int
	@param promotions: counter for number of promotions fix func has done
	@pre: newnode father after initial insertion, function check in recursion whether to execute promotion/rotation so that the tree remains a proper AVL tree
	@rtype: int
	@returns: promotions (int), which is the number of promotions that the function made
	"""
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
	
	"""fix tree after node delete 

	@pre: parent node of the node we have deleted , function check in recursion whether to execute demotion/rotation so that the tree remains a proper AVL tree
	"""
	def fixdelete(self):#O(logn)(worst case is when demotion goes all the way to tree root)
		if((self.getHeightDistanceLeft()==2) and (self.getHeightDistanceRight()==2 )): #if demote is needed
			self.UpdateHeight() #demote !
			if(self.parent!=None):
				return self.parent.fixdelete()
			return # we made it to the root, finish !
		if((self.getHeightDistanceLeft()==2) or (self.getHeightDistanceRight()==2)):#if demote isnt needed because the balance factor is 1
			return #finish!
		if(self.getHeightDistanceLeft()==3):
			self.rotateLeft()
		if(self.getHeightDistanceRight()==3):
			self.rotateRight()
		if(self.parent!=None):#because after rotation we might not be done
			self.parent.fixdelete()
		return

	"""given node, execute rotation to the right, but before checks if double rotation is needed

	@pre: a node which his distance from his right child is 3 or 2 (depeding on the case), this function preform rotation right in order to balence the tree
	"""
	def rotateRight(self): # O(1) complexity
		newfather=self.left
		if(newfather.getHeightDistanceLeft()==2):#in case of double-rotation
			newfather.rotateLeft()
			newfather=newfather.parent
		self.left=newfather.right
		self.left.parent=self
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

	""" execute rotation to the left, but before checks if double rotation is needed

	@pre: a node which his distance from his left child is 3 or 2 (depeding on the case), this function preform rotation left in order to balence the tree
	"""
	def rotateLeft(self): # O(1) complexity
		newfather=self.right
		if(newfather.getHeightDistanceRight()==2):#in case of double-rotation
			newfather.rotateRight()
			newfather=newfather.parent
		self.right=newfather.left
		self.right.parent=self
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

	""" finds and returns this node's predecessor

	@rtype: AVLNode
	@returns: predecessor node
	"""
	def Predecessor(self):#O(logn)
		if(self.left.is_real_node()):
			return self.left.findMaxChild()
		traveler=self
		while(traveler.parent.left==traveler):
			traveler=traveler.parent
		traveler=traveler.parent
		return traveler
	
	""" finds and returns this node's successor

	@rtype: AVLNode
	@returns: successor node
	"""
	def Successor(self):#O(logn)
		if(self.right.is_real_node()):
			return self.right.findMinChild()
		traveler=self
		while(traveler.parent.right==traveler):#while im the right child of my father
			traveler=traveler.parent
		traveler=traveler.parent
		return traveler
	
	""" finds and returns the min node in self subtree

	@rtype: AVLNode
	@returns:  min node in sub tree
	"""
	def findMinChild(self):#O(logn)
		traveler=self
		while(traveler.left.is_real_node()):
			traveler=traveler.left
		return traveler
	
	""" finds and returns the max node in self subtree

	@rtype: AVLNode
	@returns:  min node in sub tree
	"""
	def findMaxChild(self):#O(logn)
		traveler=self
		while(traveler.right.is_real_node()):
			traveler=traveler.right
		return traveler
	
	"""
	replace this node and putting in his place another node

	@type other: AVLNode
	@param other: the node that shuold replace this node
	"""
	def replaceMe(self,other): #O(1)
		other.right=self.right 
		other.left=self.left
		other.right.parent=other
		other.left.parent=other
		other.parent=self.parent
		if(self.parent==None):
			return
		if(self.parent.right==self):
			self.parent.right=other
		else:
			self.parent.left=other
		

	def specific_search(self,key,track):
		traveler=self
		while((traveler.is_real_node())and (traveler.key!=key)):
			if(traveler.key>key):
				traveler=traveler.left
			else:
				traveler=traveler.right
			track+=1
		if(traveler.is_real_node()):
			return traveler, track
		return None -1
	

		
		

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.max=None
		self.size=0



	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):# search for key (O(logn) complexity)
		traveler=self.root
		track=1
		while(traveler.is_real_node()):
			if(traveler.key==key):
				return traveler, track
			if(traveler.key<key):
				traveler=traveler.right
			else:
				traveler=traveler.left
			track+=1 
		return None, -1 #if Node isnt found


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key): #O(logn)
		track=1
		node=self.max_node()
		while((node.parent!=None) and (node.key>key)):#go up on the right track of the tree until we find smaller parent or we get to the root O(logn)
			node=node.parent
			track+=1
		return node.specific_search(key,track) #when we made it to that root we are searching the node in its subtree
		
	"""execute initial insertion to the tree and then sends the tree to fix function
        
	@type key: int, val: Any, newnodeplace: AVLNode, track: int
	@param key,val: the key and val of new node, newnodeplace: the initial father of new node,track: the track from insert func
	@rtype: (AVLNode,int,int)
	@returns: (x,e,p) where x is the new node,
	and e is the number of edges on the path between the starting node and ending node+1.
	and p is number of promotions fix func made
	"""
	def insertion(self,key,val,newnodeplace,track):
		if(newnodeplace.key<key):
				newnodeplace.right=AVLNode(key,val)
				newnode=newnodeplace.right
		else:
				newnodeplace.left=AVLNode(key,val)
				newnode=newnodeplace.left
		if(key>self.max.key):
			self.max=newnode
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
			self.max=newnode
			self.size+=1
			return newnode, track, 0
		while(traveler.is_real_node()):# search for key (O(logn) complexity)
			prev=traveler
			if(traveler.key<key):
				traveler=traveler.right
			else:
				traveler=traveler.left
			track+=1 
		self.size+=1
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
		traveler=self.max
		if(traveler==None):# if tree is empty
			newnode=AVLNode(key,val)
			newnode.left=AVLNode(None,None)
			newnode.right=AVLNode(None,None)
			newnode.UpdateHeight()
			self.root=newnode
			self.size+=1
			self.max=newnode
			return newnode, 1, 0
		track=1
		while((traveler!=None)and(traveler.key>key)):
			traveler=traveler.parent
			track+=1
		if(traveler==None):
			traveler=self.root
		prev=traveler
		while((traveler.is_real_node())):
			prev=traveler
			if(traveler.key>key):
				traveler=traveler.left
			else:
				traveler=traveler.right
		self.size+=1
		return self.insertion(key,val,prev,track)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		nodefather=node.parent
		if(node.right.is_real_node()!=True or node.left.is_real_node()!=True): #if node doesnt have two childrens we replace node with his right\left child
			if(node.right.is_real_node()!=True): # if node doesnt have right child
				newchild=node.left
			elif(node.left.is_real_node()!=True): # if node doesnt have left child
				newchild=node.right
			if(nodefather==None):#if node is root with one child
				self.root=newchild
				self.size=1
				self.max=self.root
				return 
			if(nodefather.right==node):
				nodefather.right=newchild
			else:
				nodefather.left=newchild
			newchild.parent=nodefather
			nodefather.fixdelete() #O(logn)
			self.size-=1
		else: #if node has two children
			newchild=node.Successor() #we find his successor and keep pointer to him O(logn)
			self.delete(newchild) #we delete Successor O(logn)
			node.replaceMe(newchild) #replace node with Successor
			if(node==self.root):#if node is root now root is new child
				self.root=newchild
			newchild.UpdateHeight() #update its height to old node's height
		if(self.root.parent!=None): #in case of rotation with root
			self.root=self.root.parent



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
		if(self.root.height<tree2.root.height):#check whos the taller tree
			tallertree=tree2
			shortertree=self
		traveler=tallertree.root #walk on the taller tree
		if(key<tallertree.root.key):# checks whether to walk on the right track or the left track of tallertree
			while(traveler.height>shortertree.root.height):# left track
				traveler=traveler.left
			xnode= AVLNode(key,val)# creating xnode and updating his childrens 
			xnode.right=traveler
			xnode.left=shortertree.root
			xnode.parent=traveler.parent
			if(traveler.parent!=None): #if xnode isnt the tallertree root
				traveler.parent.left=xnode
			else:#if xnode is the tallertree root
				tallertree.root=xnode
			self.max=tallertree.max_node
		else:
			while(traveler.height>shortertree.root.height):# right track
				traveler=traveler.right
			xnode= AVLNode(key,val)
			xnode.left=traveler
			xnode.right=shortertree.root
			xnode.parent=traveler.parent
			if(traveler.parent!=None):#if xnode isnt the tallertree root
				traveler.parent.right=xnode
			else:#if xnode is the tallertree root
				tallertree.root=xnode
			self.max=shortertree.max_node
		traveler.parent=xnode
		xnode.UpdateHeight()
		if(xnode.parent!=None):# if Xnode isnt taller tree root we need to check and/or fix the top of the tallertree
			xnode.parent.fix(0)
		if(self!=tallertree):#we want the root to be the tallertree root
			if(tallertree.root.parent!=None):#if fix func made rotation with tallertree root
				tallertree.root=tallertree.root.parent
			self.root=tallertree.root
		self.size+=shortertree.size+1


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
		t1=AVLTree()
		t1.root=node.left
		t2=AVLTree()
		t2.root=node.right
		uptraveler=node
		while(uptraveler.parent!=None):
			if(uptraveler.parent.right==uptraveler):
				tmptree=AVLTree()
				tmptree.root=uptraveler.parent.left
				t1.join(tmptree,uptraveler.key,uptraveler.val)
			else:
				tmptree=AVLTree()
				tmptree.root=uptraveler.parent.right
				t2.join(tmptree,uptraveler.key,uptraveler.val)
			uptraveler=uptraveler.parent
		return t1, t2

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):																			
		arr = []
		self.avl_to_array_rec(self.root, arr)
		return arr

	def avl_to_array_rec(self, node, arr):#O(n)
		if (node.is_real_node()!=True):
			return
		self.avl_to_array_rec(node.left, arr)
		arr.append((node.key,node.value)) 
		self.avl_to_array_rec(node.right, arr)

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max
	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self): #O(1)
		return self.size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

class AVLTester:
	def __init__(self, AVLTree, AVLNode):
		self.AVLTree = AVLTree  # שמירת המחלקה של העץ
		self.AVLNode = AVLNode

	def test_insert(self):
			print("Testing insert...")
			tree = self.AVLTree()
			tree.insert(10, "value10")
			tree.insert(20, "value20")
			tree.insert(5, "value5")
			assert tree.size == 3, "Insert failed: size mismatch"
			print("Insert test passed.")

	def test_delete(self):
			print("Testing delete...")
			tree = self.AVLTree()
			tree.insert(10, "value10")
			tree.insert(20, "value20")
			tree.insert(5, "value5")
			node_to_delete = tree.search(10)[0]  # Assuming search returns (key, node)
			tree.delete(node_to_delete)  # Pass the AVLNode 
			assert tree.size== 2, "Delete failed: size mismatch"
			assert tree.search(10)[0] is None, "Delete failed: key 10 still found"
			print("Delete test passed.")

	def test_join(self):
			print("Testing join...")
			tree1 = self.AVLTree()
			tree1.insert(5, "value5")
			tree1.insert(3, "value3")
			tree2 = self.AVLTree()
			tree2.insert(10, "value10")
			tree2.insert(15, "value15")
			tree1.join(tree2, 7, "value7")
			assert tree1.size == 5, "Join failed: size mismatch"
			assert tree1.search(7)[0] == tree1.root, "Join failed: key 7 not found"
			print("Join test passed.")

	def test_split(self):
			print("Testing split...")
			tree = self.AVLTree()
			tree.insert(10, "value10")
			tree.insert(20, "value20")
			tree.insert(5, "value5")
			node_to_split = tree.search(10)[0]  # Assuming search returns (key, node)
			left_tree, right_tree = tree.split(node_to_split)  # Pass the AVLNode directly
			# Validate by checking elements in each tree
			left_array = left_tree.avl_to_array()
			right_array = right_tree.avl_to_array()
			assert all(key < node_to_split.key for key, _ in left_array), "Split failed: left tree keys are incorrect"
			assert all(key > node_to_split.key for key, _ in right_array), "Split failed: right tree keys are incorrect"
			combined_array = left_array + [(node_to_split.key, node_to_split.value)] + right_array
			original_array = tree.avl_to_array()
			assert sorted(combined_array) == sorted(original_array), "Split failed: resulting trees do not match original tree"
			print("Split test passed.")

	def test_avl_to_array(self):
			print("Testing avl_to_array...")
			tree = self.AVLTree()
			tree.insert(10, "value10")
			tree.insert(20, "value20")
			tree.insert(5, "value5")
			array = tree.avl_to_array()
			assert array == [(5, "value5"), (10, "value10"), (20, "value20")], "avl_to_array failed: incorrect array representation"
			print("avl_to_array test passed.")

	def run_tests(self):
			self.test_insert()
			self.test_delete()
			self.test_join()
			self.test_split()
			self.test_avl_to_array()
			print("All tests passed!")
	
def buildsortedarray(i):
		newarr=list()
		for j in range(111*(2**i)):
			newarr.append(j)
		return newarr
def buildopossitearr(i):
		newarr=list()
		for j in range(111*(2**i),0,-1):
			newarr.append(j)
		return newarr
def buildrandarr(i):
		arr=buildsortedarray(i)
		random.shuffle(arr)
		return arr
def buildrandinversionsarray(i):
		arr=buildsortedarray(i)
		for i in range(0,len(arr)-2,2):
			p=random.random()
			if(p<=0.5):
				temp=arr[i]
				arr[i]=arr[i+1]
				arr[i+1]=temp
		return arr
def countsearchforinsertion(arr):
	tree=AVLTree()
	counter=0
	for i in range(len(arr)-1):
		counter+=tree.finger_insert(arr[i],"yalla")[1]
	return counter

def expirement():
	for i in range(1,11,1):
		print("i equals to: ")
		print (i)
		sortedarr=buildsortedarray(i)
		opossitearr=buildopossitearr(i)
		print("count in sorted arr:")
		print(countsearchforinsertion(sortedarr))
		print ("count in opposite arr:")
		print(countsearchforinsertion(opossitearr))
		count=0
		print("count in rand arr: (avg)")
		for j in range (20):
			randarr=buildrandarr(i)
			count+=countsearchforinsertion(randarr)
		print(count/20)
		inverarr=buildrandinversionsarray(i)
		print("count for inversion arr:")
		print(countsearchforinsertion(inverarr))


def print_tree(node,dict=dict(), indent="", last=True):
	if node is None:
		return
	dict[node.key] = True
	print(indent, end="")
	if last:
		print("R----", end="")
		indent += "   "
	else:
		print("L----", end="")
		indent += "|  "
	print(node.key)
	print_tree(node.left,dict, indent, last=False)
	print_tree(node.right, dict,indent, last=True)






def main():
	newtree=AVLTree()
	print(newtree.insert(3,"hello"))
	print(newtree.insert(2,"world"))
	print(newtree.insert(1,"!"))
	print(newtree.insert(10,"!"))
	print(newtree.insert(9,"!"))
	print("search")
	print(newtree.search(9)[0])
	print(newtree.root.right.key)#9
	print(newtree.insert(6,"!"))
	print(newtree.root.key)
	print(newtree.root.right.key)
	print(newtree.root.left.key)
	print(newtree.insert(4,"!"))
	print(newtree.root.key)
	print("HELLO")
	print(newtree.size)
	newtree1=AVLTree()
	print(newtree1.insert(12,"hello"))
	print(newtree1.insert(15,"!"))
	print(newtree1.insert(13,"world"))
	newtree1.join(newtree,11,"join!")
	print(newtree1.root.key)
	print("passed my test")
	newtt=AVLTree()
	expirement()




if __name__ == "__main__":
    main()