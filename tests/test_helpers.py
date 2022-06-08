from helpers.helper_functions import allowed_file

def test_allowed_file():
    good_file = 'speaker.pdf'
    bad_file = 'speaker.txt'
    assert allowed_file(good_file) == True
    assert allowed_file(bad_file) == False


