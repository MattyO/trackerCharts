class Story: 
	def __init__(self, xml):
		attrs = dict()
		for child in xml:
			if len(child.findall('.//*')) == 0:
				attrs[child.tag] = child.text

		if attrs.has_key('owned_by') is False:
			attrs['owned_by'] = None

		self.__dict__ = attrs
	
def StoryList(story_xml_list):
	story_list = []

	for story_set in story_xml_list:
		for story_xml in story_set.findall('story'):
			story_list.append(Story(story_xml))

	return story_list
		



