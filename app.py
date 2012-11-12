import sys
from os import getcwd 
sys.path.append(getcwd() + "/libs")

from flask import Flask, render_template
from api import tracker
from classes.Project import Project
from classes.ProjectList import ProjectList

app = Flask(__name__)
app.debug = True

@app.route("/")
def overview():
	projects = ProjectList(tracker.getProjects())
	return render_template('index.html', projects=projects)

@app.route("/<int:tracker_id>")
def project(project_id):
	pass


@app.route("/wip.json")
def wip(type=None):
	pass

@app.route("/burndown/<int:tracker_id>.json")
def burndown(tracker_id, type=None):
	pass

@app.route("/config/")
def config():
	pass

@app.route("/update")
def updat():
	pass


if __name__ == "__main__":
	print "running flask"
	app.run(port=4567, host='0.0.0.0') 
