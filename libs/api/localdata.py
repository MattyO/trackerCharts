import yaml
import xml.etree.ElementTree as ET
import os

required_dirs = ["data","data/cache"]

for dir in required_dirs: 
    if os.path.isdir(dir) == False:
        os.mkdir(dir)

def xml_to_dictonary(xml):
    dictonary = {}
    for child in xml:
        if len(child.findall('.//*')) == 0:
            dictonary[child.tag] = child.text

    return dictonary

def get_cached_data(id):
    cached_data = None
    if id != None and os.path.exists("data/cache/" + id):
        with open("data/cache/" + id, 'r') as f:
            cached_data = yaml.load(f)

    return cached_data 

def cache_data(id,data):
    with open("data/cache/" + id, 'w') as f:
        yaml.dump(data, f)

def listify(maybe_a_list):
    if maybe_a_list == None:
        maybe_a_list = []
    return maybe_a_list

def saveBurndownStates(burndown, project_id):
    _save_yaml_thing(burndown, "burndown", project_id)

def getBurndownStates(project_id):
    return _get_yaml_thing("burndown", project_id)

def getStoriesXML(project_id):
    return _get_xml_thing("stories", project_id)


def saveStoriesXML(stories, project_id):
    _save_xml_thing(stories, "stories", project_id)

def getProjectsXML():
    return _get_xml_thing("all_projects",None)

def saveProjectsXML(xml):
    _save_xml_thing(xml, "all_projects")

def _get_yaml_thing(filename, folder=''):
    file_path = _data_path(folder, filename, 'yml')
    yaml_data = None

    if os.path.exists(file_path) == False:
        return None

    with open(_data_path(folder, filename, 'yml'), 'r') as f:
        yaml_data = yaml.load(f) 
    return yaml_data

def _save_yaml_thing(thing, filename, folder=''):
    with open(_data_path(folder, filename, 'yml'), 'w') as f:
        yaml.dump(thing, f) 

def _get_xml_thing(filename, folder):
    return ET.parse(_data_path(folder, filename, 'xml')).getroot()

def _save_xml_thing(thing, filename, folder=''):
    ET.ElementTree(element=thing).write(_data_path(folder, filename, 'xml'))

def _data_path(folder, filename, extension):
    path_head = "data"
    if folder is not None:
        path_head += "/" + folder
        if os.path.isdir(path_head) == False:
            os.mkdir(path_head)
    return path_head + "/" + filename + "." + extension
