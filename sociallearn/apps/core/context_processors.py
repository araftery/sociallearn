import profiles.utils

def level_progress(request):
	try:
		points = request.user.student.points
		level = request.user.student.level
		level_progress = int(((float(points) - profiles.utils.get_points(level)) / profiles.utils.get_points(level + 1)) * 100)
	except:
		level_progress = None

	return {'level_progress':level_progress,}