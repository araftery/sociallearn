import profiles.utils, profiles.models

def level_progress(request):
	try:
		points = request.user.student.points
		level = request.user.student.level
		level_progress = int(((float(points) - profiles.utils.get_points(level)) / profiles.utils.get_points(level + 1)) * 100)
	except:
		level_progress = None

	return {'level_progress':level_progress,}

def notifications(request):
	# look for active friend requests
	if request.user.is_authenticated():
		friend_requests = request.user.student.friendrequests_in.filter(accepted=None)
		notifs = {
			'num': 0,
			'objects': [],
		}

		for req in friend_requests:
			notifs['num'] += 1
			notif = {
				'sender': req.requester,
				'type': 'friend request',
				'object': req,
			}
			notifs['objects'].append(notif)

		if notifs['num']:
			return {'notifications': notifs}
		else:
			return {'notifications': None}
	else:
		return {}