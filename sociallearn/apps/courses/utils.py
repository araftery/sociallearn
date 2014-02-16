def assignment_tree(node, tree = None):
	"""
	Follows children of a root assignment node recursively to get all of the assignments in a given week hierarchically.
	Returns an ordered list.
	"""
	if tree is None:
		tree = []
	tree.append(node)
	if not hasattr(node, 'child'):
		return tree
	else:
		return assignment_tree(node.child, tree)