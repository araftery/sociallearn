import courses
from django.db.models import Sum

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


def total_points_in_course(course):
	total_points_result = courses.models.Assignment.objects.filter(course=course).aggregate(Sum('points'))

	# note: this could break if there were more than one element in this dict
	total_points = total_points_result.itervalues().next()
	if total_points is None:
		total_points = 0

	return int(total_points)

def percentage_completed(course, student):
	"""
	Calculates the percentage of a course completed by a given student. Based on the number of points
	earned in that class divided by the total number of points in the class.
	"""
	points_earned_result = courses.models.AssignmentCompletion.objects.filter(student=student, assignment__course=course).aggregate(Sum('assignment__points'))

	# note: this could break if there were more than one element in this dict
	points_earned = points_earned_result.itervalues().next()
	if points_earned is None:
		points_earned = 0

	total_points = course.total_points

	return int(((float(points_earned)/float(total_points)) * 100))