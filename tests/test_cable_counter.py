import os
from backend.CableCounter import get_cable_number, get_lines, get_distance_to_hang, get_anchors_from_file

from backend.parsedbaudioxml import ParserDBAudioSpeakerXML

hang_origin = [33.0, 6.0, 9.5]
anchors = [[10, 0, 0], [0,3,0], [0,0,10]]
speaker_type: dict[str,int] = {'Q-SUB': 0, 'Q1': 5, 'Q7': 0}
num_of_speakers = 5
all_linked = False
links = 3
flown = True

DEFAULT_HANG = {
        'Hang': hang_origin,
        'Speaker': speaker_type,
        'Num_speakers': num_of_speakers,
        'Links': links,
        'All_linked': all_linked,
        'Anchors': anchors,
        'Flown': flown
        }


class TestCableCounter():
    def test_get_lines(self):
        biamp, oneamp = get_lines(DEFAULT_HANG)
        assert(biamp == 0)
        assert(oneamp == 2)
    
    def test_get_lines_j_sub(self):
        hang = [4.2, 11.5, 10.0]  # x y z coordinates of hang
        speaker = {'J-SUB': 4}  # type of speaker
        num_speakers = 4  # num of cabinets
        anchors = [[1, 6, 0],[0, 8, 0], [0, 8, 13], [4, 12, 13]]
        test_4_j_subs = {
            'Hang': hang, 
            'Speaker': speaker, 
            'Num_speakers': num_speakers, 
            'Links': False, 
            'Anchors': anchors}  # all data in one dict
        biamp, oneamp = get_lines(test_4_j_subs)
        assert biamp == 4

    def test_get_cable_number(self):
        hang = [4.2, 11.5, 10.0]  # x y z coordinates of hang
        speaker = {'J-SUB': 4}  # type of speaker
        num_speakers = 4  # num of cabinets
        anchors = [[1, 6, 0],[0, 8, 0], [0, 8, 13], [4, 12, 13]]
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': False, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)
        
        hang = [8, 40, 10.0]  # x y z coordinates of hang
        speaker = {'J-TOP': 8}  # type of speaker
        num_speakers = 8  # num of cabinets
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': True, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)
        
        hang = [0., 0., 13.5]  # x y z coordinates of hang
        speaker = {'Y10': 7}  # type of speaker
        num_speakers = 7  # num of cabinets
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': False, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)
    
    def test_print_delay_8y(self):
        test_folder = os.path.join("tests", "speaker_data_xml")

        parser = ParserDBAudioSpeakerXML (os.path.join(test_folder, 'delay8y.dbea'))
        print(parser.populate_hang_data())

    
class TestGetDistanceToHang():
    def test_zero_anchors_x(self):
        assert get_distance_to_hang([10, 0, 0], [[0,0,0]]) == 10.0
    
    def test_zero_anchors_xyz(self):
        assert get_distance_to_hang([10, 10, 10], [[0,0,0]]) == 30.0
    
    def test_basic_case(self):
        assert get_distance_to_hang([10, 20, 5], [[0,0,0], [10, 0, 0], [10, 20, 0]]) == 35
    
    def test_zero(self):
        assert get_distance_to_hang([0, 0, 0], [[0,0,0]]) == 0.0
    
    def test_negative_first_anchor(self):
        assert get_distance_to_hang([10, 20, 5], [[0, -5,0], [10, 0, 0], [10, 20, 0]]) == 40
    
    def test_negative_anchors(self):
        assert get_distance_to_hang([10, -20, 5], [[0, -5,0], [10, -5, 0], [10, -20, 0]]) == 30

    def test_from_ceiling(self):
        hang = [2.0, 14.3, 5.0]
        anchors = [[0.0, 0.0, 0.0], [0.0, 11.0, 0.0], [0.0, 11.0, 14.0], [2.0, 14.0, 14.0]]
        assert get_distance_to_hang(hang, anchors) == 39.3
    

    
