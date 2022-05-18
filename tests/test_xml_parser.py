from web_interface.backend.parsedbaudioxml import ParserDBAudioSpeakerXML

class TestXMLParser():
    def test_print_delay_8y(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/delay8y.dbea')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_ff4y(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/Frontfill4y.dbep')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_main16v(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/Main16V.dbea')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_maingsl(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/MainGSL.dbea')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")

    def test_print_out8v(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/Outfill8V.dbea')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n") 
        
    def test_print_24subs_arr(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/SUB array24subsV.dbesa')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")
    
    def test_print_ksl9(self):
        parser = ParserDBAudioSpeakerXML('web_interface/backend/test_data/speaker_data_xml/KSL9.dbea')
        parser.populate_hang_data()
        for obj in parser.hang_data:
            print(obj, parser.hang_data[obj])
        print("___________________________________\n")