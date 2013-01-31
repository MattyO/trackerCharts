import requests
import config
import xml.etree.ElementTree as ET


def get_auth_token(username, password):
	print "authenticating..."
	authRequest = requests.get('https://www.pivotaltracker.com/services/v3/tokens/active', auth=(username, password))
	etAuth = ET.fromstring(authRequest.text)
	return etAuth.find('guid').text

def create_auth_header(auth_token):
	return {'X-TrackerToken': auth_token}

token = None
header = None

#token = get_auth_token(config.trackername, config.trackerpassword)
#header= create_auth_header(token)

def get_token():
		return get_auth_token(config.trackername, config.trackerpassword)

def get_header():
	global header
	if header != None:
		header= create_auth_header(get_token())



def getProjects(different_token=None):
	request_header = get_header()
	if different_token != None:
		request_header = create_auth_header(different_token)

	projectRequest = requests.get('https://www.pivotaltracker.com/services/v3/projects',headers=request_header)
	return ET.fromstring(projectRequest.text)

def getStories(tracker_id):

	story_request = requests.get("https://www.pivotaltracker.com/services/v3/projects/" + tracker_id + "/stories",headers=get_header())

	return ET.fromstring(story_request.text)

