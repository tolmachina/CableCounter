import os
from backend.parsedbaudioxml import ParserDBAudioSpeakerXML


test_folder = os.path.join("tests", "speaker_data_xml")
class TestXMLParser():
    def test_print_delay_8y(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'delay8y.dbea'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_ff4y(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'Frontfill4y.dbep'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_main16v(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'Main16V.dbea'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_maingsl(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'MainGSL.dbea'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_out8v(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'Outfill8V.dbea'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n") 
        
    def test_print_24subs_arr(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'SUB array24subsV.dbesa'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")
    
    def test_print_ksl9(self):
        parser = ParserDBAudioSpeakerXML(os.path.join(test_folder, 'KSL9.dbea'))
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")