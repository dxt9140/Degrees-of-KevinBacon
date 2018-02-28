"""
pq.py
Author: Dominick Taylor (dxt9140@g.rit.edu)
Created: 2/5/2018
Python module for mainting a priority queue to use in conjunction with
kb.py (Degrees of Kevin Bacon with Twitter API). The queue maintains a
max-heap using a standard array as its backend.

NOTE: I suppose the name 'PQ' is erroneous. This is simply an array heap
data structure. I just don't really feel like changing every reference tbh.
"""

"""
Class declaration for the heap.
"""
class PQ:

	queue = []
	
	def __str__( self ):
		string = "[ "
		for i in range(0, len(self.queue)):
			string += str(self.queue[i]) + " "
		string += "]"
		return string

	"""
	Add a node into the heap
	"""
	def insert( self, node ):
		self.queue.append( node ) 
		self.heapify()

	"""
	Remove the top node of the heap.
	"""
	def pop( self ):
		target = self.queue[0]
		self.queue = list( self.queue[1:] )
		self.heapify()
		return target


	"""
	Ensure that every child node is less than its parent
	"""
	def heapify( self ):
		q = self.queue
		length = len(q)
		for i in range( len(q)-1, -1, -1 ):
			parent_index = None

			if i % 2 == 0:		# Even index
				parent_index = ( i // 2 ) - 1
			elif i % 2 == 1:	# Odd index
				parent_index = ( i // 2 )

			if parent_index >= 0 and q[i].value > q[parent_index].value:
				temp = q[i]
				q[i] = q[parent_index]
				q[parent_index] = temp
				i += 1

"""
False node data structure, used for unit tests.
"""
class TestClass:
	value = None

	def __init__( self, value ):
		self.value = value

	def __str__( self ):
		return str( self.value )

"""
Main function to provide unit testability
"""
def main():
	
	q = PQ()

	for i in range(1, 25):
		node = TestClass( i )
		q.insert( node )

	print( str( q ) )

	test = q.pop()

	print( str( q ) )
	

if __name__ == '__main__':
	main()

# End of File
#-------------------------------------------------------------------------------

