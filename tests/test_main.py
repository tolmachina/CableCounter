from unittest import TestCase
from main import get_cable_number

def get_data_test():

    return test_data


# class Test(TestCase):
#     def test_get_data(self):
#         self.fail()
#
#     def test_main(self):
#         self.fail()


class Test(TestCase):
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
