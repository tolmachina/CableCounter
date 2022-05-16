import sys
from ..backend.CableCounter import get_cable_number, get_lines, get_distance_to_hang, get_anchors_from_file

print(sys.path)
hang = [33.0, 6.0, 9.5]
anchors = [[10, 0, 0], [0,3,0], [0,0,10]]
speaker_type = {'Q-SUB': 0, 'Q1': 5, 'Q7': 0}
num_of_speakers = 5
all_linked = False
links = 3
flown = True

data = {'Hang': hang,
        'Speaker': speaker_type,
        'Num_speakers': num_of_speakers,
        'Links': links,
        'All_linked': all_linked,
        'Anchors': anchors,
        'Flown': flown}

class TestCableCounter():
    def test_get_distance_to_hang(self):
        assert get_distance_to_hang([10, 0, 0], [[0,0,0]]) == 10.0
        assert get_distance_to_hang([0, 0, 0], [[0,0,0]]) == 0.0
        assert get_distance_to_hang([10, 20, 5], [[0,0,0], [10, 0, 0], [10, 20, 0]]) == 35
        assert get_distance_to_hang([10, 20, 5], [[0, -5,0], [10, 0, 0], [10, 20, 0]]) == 40
        # assert get_distance_to_hang([10, -20, 5], [[0, -5,0], [10, 0, 0], [10, 20, 0]]) == 30


    def test_get_cable_number(self):
        hang = [4.2, 11.5, 10.0]  # x y z coordinates of hang
        speaker = 'J-Sub'  # type of speaker
        num_speakers = 4  # num of cabinets
        anchors = [[1, 6, 0],[0, 8, 0], [0, 8, 13], [4, 12, 13]]
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': True, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)
        
        hang = [8, 40, 10.0]  # x y z coordinates of hang
        speaker = 'J-Top'  # type of speaker
        num_speakers = 8  # num of cabinets
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': True, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)
        
        hang = [0., 0., 13.5]  # x y z coordinates of hang
        speaker = 'One'  # type of speaker
        num_speakers = 7  # num of cabinets
        test_data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': False, 'Anchors': anchors}  # all data in one dict
        get_cable_number(test_data)

    def test_get_lines(self):

        biamp, oneamp = get_lines(data)
        assert(biamp == 0)
        assert(oneamp == 2)
        

# test = TestCableCounter()
# test.test_get_distance_to_hang()

# test.test_get_lines()