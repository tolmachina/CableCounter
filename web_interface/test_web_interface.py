from helpers.helper_functions import allowed_file

def test_allowed_file():
    good_file = 'speaker.pdf'
    bad_file = 'sdfg.txt'
    print(allowed_file(good_file))

test_allowed_file()

