import requests
import config
import xml.etree.ElementTree as ET


def _getAuthToken():
	print "getting auth token"
	authRequest = requests.get('https://www.pivotaltracker.com/services/v3/tokens/active', auth=(config.trackername, config.trackerpassword))
	etAuth = ET.fromstring(authRequest.text)
	return etAuth.find('guid').text

token = _getAuthToken()
header={'X-TrackerToken': token}

def getProjects():
	global token, header

	projectRequest = requests.get('https://www.pivotaltracker.com/services/v3/projects',headers=header)
	print projectRequest.text
	return ET.fromstring(projectRequest.text)

def getStories(tracker_id):
	pass
