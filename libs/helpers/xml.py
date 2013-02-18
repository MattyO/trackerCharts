def xml_to_dictonary(xml):
    dictonary = {}
    for child in xml:
        if len(child.findall('.//*')) == 0:
            dictonary[child.tag] = child.text

    return dictonary

def xml_to_list(xml, element_name):
    return [xml_entry for xml_entry in xml.findall(element_name)]

def convert_elements(converter, xml, element_name):
    return [converter(xml_entry) for xml_entry in xml.findall(element_name)]
