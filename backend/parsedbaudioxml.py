from dataclasses import dataclass
import xml.etree.ElementTree as ET

class ParserDBAudioSpeakerXML():

    def __init__(self, filename) -> None:
        tree = ET.parse(filename)
        self.root = tree.getroot()
        self.hang_data = {
        'Name': None,
        'Hang': [],
        'Speaker': {},
        'Num_speakers': int(0),
        'Links': int(0),
        'LinksArray': [],
        'All_linked': None,
        'Anchors': None,
        'Flown': False}
    
    def print_test(self):
        for array in self.root:
            print(array)
            for array_part in array:
                if array_part.tag == 'Box':
                    print(array_part.attrib["Name"])
                    print(array_part.attrib["Linked"])
                if array_part.tag == 'Origin':
                    print(array_part.attrib)
            break
    
    def populate_hang_data(self):
        for array in self.root:
            self.hang_data['Name'] = array.tag
            for array_part in array:
                if array_part.tag == 'Box':
                    if array_part.attrib["Name"] in self.hang_data["Speaker"]:
                        self.hang_data["Speaker"][array_part.attrib["Name"]] += 1
                    else:
                        self.hang_data["Speaker"][array_part.attrib["Name"]] = 1
                    if array_part.attrib["Linked"] == '1':
                        self.hang_data['Links'] += 1
                    self.hang_data['LinksArray'].append(int(array_part.attrib["Linked"]))
                    
                if array_part.tag == 'Origin':
                    x = float(array_part.attrib['x'])
                    y = float(array_part.attrib['y'])
                    z = float(array_part.attrib['z'])
                    self.hang_data['Hang'] = [x,y,z]
            break
        
        for name in self.hang_data['Speaker']:
            self.hang_data['Num_speakers'] += self.hang_data['Speaker'][name]
        
        if self.hang_data['Name'] == 'SubArray':
            self.hang_data['Num_speakers'] *= 2
            for sub_name in self.hang_data['Speaker']:
                self.hang_data['Speaker'][sub_name] *= 2
        
        try:
            if self.root[0].attrib['Mounting'] == 'flown':
                self.hang_data['Flown'] = True
        except KeyError:
            self.hang_data['Flown'] = False

        if self.hang_data['Links']  != 0:
            if self.hang_data['Num_speakers'] // self.hang_data['Links'] == 2:
                self.hang_data['All_linked'] = True
        
        return self.hang_data
    
@dataclass
class Plane:
    pass

class ParseDBAudioVenueXML():
    def __init__(self, filename) -> None:
        tree = ET.parse(filename)
        self.root = tree.getroot()
        self.venue_data = {
        'Name': None,
        'Hang': [],
        'Speaker': {},
        'Num_speakers': 0,
        'Links': 0,
        'LinksArray': [],
        'All_linked': None,
        'Anchors': None,
        'Flown': False}
    
    def print_test(self):
        for child in self.root[1]:
            if child.tag == 'RoomObject':
                print(child.attrib['Name'])


            # for grandchild in child:
            #     print(grandchild.tag)
            #     for grgrchildren in grandchild:
            #         print(grgrchildren.tag)
            #     print("*****")
            # print("-----")
                
def dist(x1, y1, x2, y2, x3, y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = (dx*dx + dy*dy)**.5

    return dist
