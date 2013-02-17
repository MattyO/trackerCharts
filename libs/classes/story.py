from datetime import datetime

DAYS_IN_A_MONTH = 30

def _days_since_last_updated(first_date, second_date):
    return (second_date - first_date).days

def _prettify_days(num_days):
    pretty_string = ""

    if int(num_days) > DAYS_IN_A_MONTH:
        months, days = divmod(int(num_days), DAYS_IN_A_MONTH) 
        pretty_string += str(months)
        if days > 15: 
            pretty_string += " and a half"
        pretty_string += " months"

    else:
        pretty_string = num_days + " days"

    return pretty_string

def _tracker_string_to_time(tracker_time):
    return datetime.strptime(tracker_time, "%Y/%m/%d %H:%M:%S UTC")

def prettify_stories(stories):
    for story in stories: 
        story_days = story.days_since_last_updated
        story.days_since_last_updated = _prettify_days(story_days)

    return stories

class Story: 
    def __init__(self, xml):
        attrs = dict()
        self.lables = []
        for child in xml:
            if len(child.findall('.//*')) == 0:
                if child.tag == "labels":
                    attrs[child.tag] = child.text.split(",")
                else:
                    attrs[child.tag] = child.text

        if attrs.has_key('owned_by') is False:
            attrs['owned_by'] = None
        if attrs.has_key('labels') is False:
            attrs['labels'] = []

        attrs['days_since_last_updated'] = _days_since_last_updated(_tracker_string_to_time(attrs['updated_at']),datetime.today())

        self.__dict__ = attrs

def is_in_progress(story):
    #filtered_states = ["accepted", "delivered", "finished"]
    return story.owned_by != None and story.current_state == 'started' 


def StoryList(story_xml_list):
    story_list = []

    for story_set in story_xml_list:
        for story_xml in story_set.findall('story'):
            story_list.append(Story(story_xml))

    return story_list

def keep_by_ids(storylist, id_list):
    return filter(lambda story: story.id in id_list, storylist)

def exclude_by_ids(storylist, id_list):
    return filter(lambda story: story.id not in id_list, storylist)

def ids_for_in_progress(storylist):
    return [ story.id for story in storylist if is_in_progress(story)]

def story_ids_for_project(storylist, project_id):
    return [ story.id for story in storylist if story.project_id == project_id ]

