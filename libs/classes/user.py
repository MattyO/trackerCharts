import json
from datetime import datetime

def _days_since_last_updated(first_date, second_date):
	return (second_date - first_date).days

def _tracker_string_to_time(tracker_time):
	return datetime.strptime(tracker_time, "%Y/%m/%d %H:%M:%S UTC")

class User:
	def __init__(self, name):
		self.name = name
		self.wip = 0
		self.current_stories = []

	def updateWip(self, story):
		filtered_states = ["accepted", "delivered", "finished"]
		if story.owned_by != None and story.owned_by == self.name and story.current_state not in filtered_states:
			self.wip += 1
			self.current_stories.append(story)
	

def UserList(story_list):
	users = {}
	for story in story_list:
		if story.owned_by is not None :
			if users.has_key(story.owned_by) is False:
				users.update({story.owned_by:User(story.owned_by)})
			users[story.owned_by].updateWip(story)
	return users.values()

def userlist_tojson(user_list):
	dumpable = []
	for user in user_list:
		current_stories = [] 
		for story in user.current_stories:
			current_stories.append({
				"name":story.name,
				"updated_at": story.updated_at,
				"days_since_updated":story.days_since_last_updated,
				"id":story.id
			})
		dumpable.append({"name":user.name, "wip":user.wip, "current_stories":current_stories})
	return json.dumps(dumpable, sort_keys=True)


