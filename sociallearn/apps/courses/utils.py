def get_tree(node, tree = None):
	"""
	Follows children of a root node recursively to get all of the nodes in the tree hierarchically.
	Returns an ordered list.
	"""
	if tree is None:
		tree = []
	tree.append(node)
	if not hasattr(node, 'child'):
		return tree
	else:
		return get_tree(node.child, tree)

def get_level(points):
	"""
	Converts points to a level, using the formula level = sqrt(points/220)
	"""
	return int((points/220.0) ** .5)