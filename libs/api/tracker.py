import requests
import config
import xml.etree.ElementTree as ET


def _getAuthToken():
	print "authenticating..."
	authRequest = requests.get('https://www.pivotaltracker.com/services/v3/tokens/active', auth=(config.trackername, config.trackerpassword))
	etAuth = ET.fromstring(authRequest.text)
	return etAuth.find('guid').text

token = _getAuthToken()
header={'X-TrackerToken': token}

def getProjects():
	global token, header

	projectRequest = requests.get('https://www.pivotaltracker.com/services/v3/projects',headers=header)
	return ET.fromstring(projectRequest.text)

def getStories(tracker_id):
	global header

	story_request = requests.get("https://www.pivotaltracker.com/services/v3/projects/" + tracker_id + "/stories",headers=header)

	return ET.fromstring(story_request.text)

