from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.db.models import Sum
import profiles

# Create your models here.

class FriendRequest(models.Model):
	requester = models.ForeignKey(profiles.models.Student, related_name='friendrequests_out')
	target = models.ForeignKey(profiles.models.Student, related_name='friendrequests_in')
	time_requested = models.DateTimeField()
	time_responded = models.DateTimeField(null=True, blank=True)
	accepted = models.NullBooleanField(null=True, blank=True)


	def save(self, *args, **kwargs):
		super(FriendRequest, self).save(*args, **kwargs) # Call the "real" save() method.
		if self.accepted is True:
			if not self.requester.friends.filter(id=self.target.id):
				self.requester.friends.add(self.target)
			if not self.target.friends.filter(id=self.requester.id):
				self.target.friends.add(self.requester)
		elif self.accepted is False:
			self.requester.friends.remove(self.target)
			self.target.friends.remove(self.requester)

	def __unicode__(self):
		if self.accepted is None:
			answer = 'None'
		elif self.accepted is True:
			answer = 'accepted'
		else:
			answer = 'denied'


		return '{} requesting {} at {}, answer: {}'.format(self.requester.name, self.target.name, self.time_requested.strftime('%m/%d/%y %I:%M %p'), answer)