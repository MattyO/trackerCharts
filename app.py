import sys, os
from os.path import abspath, dirname, join
sys.path.append(abspath(join(dirname(__file__),'libs')))

from flask import Flask, render_template, redirect, url_for, make_response, session, request

from api import tracker
from api import flask_helper
from api import localdata
from api.localdata import listify

from classes.project import Project, ProjectList, Burndown, addState, burndown_tojson, projectlist_tojson, find_project, filter_on_ids,  burndown_labels, labels_tojson, list_private_ids, reduce_list, list_ids
from classes.story import Story, StoryList 
from classes.user import  User, UserList, userlist_tojson
import config

app = Flask(__name__)
app.debug = True
app.secret_key = '\xfdzKV\xfa\xb3\x8fU\x9e\xa7v\xcd\x11\xc3J \xec\x97\x06\xf3d\xe6f2'

@app.route("/")
def overview():
	projects = ProjectList(localdata.getProjectsXML())

	visible_user_projects = listify(localdata.get_cached_data(flask_helper.safe_session('user_id')))
	private_ids = list_private_ids(projects)
	
	private_ids = reduce_list(private_ids, visible_user_projects)

	projects = filter_on_ids(projects, private_ids)
	projects = filter_on_ids(projects, config.ignore)

	return render_template('index.html', projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
	if request.method == 'GET' :
		return render_template("login.html")

	username = request.form['username']
	user_token = tracker.get_auth_token(request.form['username'], request.form['password'])

	project_list = ProjectList(tracker.getProjects(user_token))
	project_ids = list_ids(project_list)
	localdata.cache_data(username, project_ids)

	session['user_id'] = username

	return redirect(url_for('overview'))

@app.route('/logout')
def logout():
	if 'user_id' in session:
		del session['user_id']
	return redirect(url_for('overview'))


@app.route("/<int:project_id>")
def project(project_id):
	project_list = ProjectList(localdata.getProjectsXML())
	project_found = find_project(project_list, str(project_id))

	if project_found == None:
		return redirect(url_for('overview'))
	
	project_id = str(project_id)
	burndown = Burndown(project_id,localdata.getBurndownStates(project_id))
	labels = burndown_labels(burndown)

	return render_template("project.html", project=project_found, labels=labels )

@app.route("/<int:project_id>/burndown.json")
def project_json(project_id):
	project_id = str(project_id)
	return burndown_tojson(Burndown(project_id,localdata.getBurndownStates(project_id)))

@app.route("/<int:project_id>/labels.json")
def labels(project_id):
	project_id = str(project_id)
	burndown = Burndown(project_id,localdata.getBurndownStates(project_id))
	labels = burndown_labels(burndown)
	return labels_tojson(labels)
	
@app.route("/projects.json")
def projects_json():
	project_list = ProjectList(localdata.getProjectsXML())
	project_list = filter_on_ids(project_list, config.ignore)
	response = make_response(projectlist_tojson(project_list))
	response.mimetype="application/json"
	return response

@app.route("/possible_states/<project_type>.json")
def get_states(project_type):
	response = make_response(config.states_tojson(config.states(project_type)))
	response.mimetype = "application/json"
	return response

@app.route("/wip.json")
def wip_json():
	project_list = ProjectList(localdata.getProjectsXML())
	project_ids = map(lambda project: project.id, project_list)
	stories_xml_list = []
	for id in project_ids :
		stories_xml_list.append(localdata.getStoriesXML(id))

	stories = StoryList(stories_xml_list)
	users = UserList(stories)

	return userlist_tojson(users)


@app.route("/wip")
def wip(type=None):

	project_list = ProjectList(localdata.getProjectsXML())
	project_ids = map(lambda project: project.id, project_list)
	stories_xml_list = []
	app.logger.debug(project_ids)
	for id in project_ids :
		stories_xml_list.append(localdata.getStoriesXML(id))

	stories = StoryList(stories_xml_list)
	users = UserList(stories)

	return render_template('wip.html', projects=project_list , users=users)

@app.route("/config/")
def config_page():
	pass

if __name__ == "__main__":
	print "running flask"
	app.run(port=4567, host='0.0.0.0') 
