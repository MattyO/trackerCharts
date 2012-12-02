import json

secret_key = 'your-secret-key-for-sessions'
trackername = 'your-pivotal-username'
trackerpassword = 'your-pivotal-password'
ignore = []
_states = {"tracker": ["unscheduled", "unstarted", "started", "finished", "delivered", "accepted"]}

def states(source):
	if _states.has_key(source):
		return _states[source]
	else:
		return None

def get_state_keys():
	return _states.keys()

def states_tojson(states):
	return json.dumps(states)
