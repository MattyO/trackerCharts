import json

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
		userobj = {"name":user.name, "wip":user.wip, "stories":[]}
		for story in user.current_stories:
			userobj["stories"].append(story.name)
		dumpable.append(userobj)

	return json.dumps(dumpable) 

def UserList_toJson(user_list):
	dumpable = []
	for user in user_list:
		current_stories = [] 
		for story in user.current_stories:
			current_stories.append({"name":story.name, "id":story.id})
			dumpable.append({"name":user.name, "wip":user.wip, "current_stories":current_stories})
	return json.dumps(dumpable)



