import os
import sys
from __init__ import *
"""
Run the app as CLI
"""
def main():
    # path = input("Input path to pdf file to scan? \n")
    """
    Its a CLI tool 'python3 main.py setupfile1.pdf setupfile2.pdf result.csv' with anchor.csv hardcoded.
    To change anchors, change anchors.csv.
    It will write result as .csv file
    :return:
    """

    if len(sys.argv) < 2:
        print("Check arguments, example: 'python3 main.py setupfile1.pdf setupfile2.pdf result.csv' ")
        sys.exit()
    if sys.argv[-1][-3:] != "csv":
        print(sys.argv[-1])
        print(sys.argv[-1][-3:])
        print(sys.argv[-1][-3:] == "csv")
        print("Last argument must be a file with .csv")
        sys.exit()

    if os.path.exists(sys.argv[-1]):
        os.remove(sys.argv[-1])
    else:
        print("The file does not exist")

    for i in range(1, len(sys.argv) - 1):
        data = get_data_pdf(sys.argv[i])
        results = get_cable_number(data)
        print(results)
        with open(sys.argv[-1], 'a') as f:
            w = csv.writer(f)
            w.writerows(results.items())

    # path = 'Groundstacked.pdf'
    # data = get_data_pdf(path)  # getting the data from user
    # get_cable_number(data)
    # path = '22NotLinked.pdf'
    # data = get_data_pdf(path)  # getting the data from user
    # get_cable_number(data)
    # path = 'Main+Sub.pdf'
    # data = get_data_pdf(path)  # getting the data from user
    # get_cable_number(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()