# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# import pandas as pd
import csv
# import pandas as pd
from tabula import read_pdf_with_template

C = 13.5 #celining meters high
SOCA_LEN = 25 #soca cable meters
EP5_LEN = 10 #ep5 cable meters
FAN_OUT_3_LEGS = 3 #cable breakout for 3 biamp legs
FAN_OUT_6_LEGS = 6 #cable breakout for 6 oneamp legs

def get_data_pdf():
    filepath = input("Input path to pdf file to scan? \n")
    # filepath = 'SetupData/Main_Setup.pdf'
    template_path = 'Main_Setup.tabula-template.json'
    df = read_pdf_with_template (filepath,
    template_path, 
    pandas_options={'header':None})

    for t in df:
        print(t)

    isFlown = df[0][1][0].split(" ")[-1]
    print(isFlown)
    if isFlown == 'flown':
        flown = True
    else:
        flown = False

    hang =[float(df[1][1][0][0:-2]),
           float(df[1][3][0][0:-2]),
           float(df[1][1][1][0:-2])] #dataframe indexing df[table][column][row][string in row]

    num_speakers_total = int(df[1][3][1]) + int(df[1][3][2]) + int(df[1][3][3])

    speaker_total = []
    for i in range(1,4):
        if int(df[1][3][i]) > 0:
            speaker_total.append(df[1][2][i].split(" ")[-1][0:-1] + " ")

    speakers = {}
    for i in range(1,4):
        speakers[(df[1][2][i].split(" ")[-1][0:-1])] = int(df[1][3][i])

    try:
        speakers['J-Top'] = speakers['J8'] + speakers['J12']
        speakers.pop('J8')
        speakers.pop('J12')
    except:
        print('no J in speakers')

    links = df[3][7].isna().sum()
    all_linked = False
    if num_speakers_total / links == 2:
        all_linked = True

    anchors = []
    with open('anchors.csv', newline='') as csvfile:
        anchor_reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in anchor_reader:
            anchors.append(list(row))

    data = {'Hang': hang,
            'Speaker': speakers,
            'Num_speakers': num_speakers_total,
            'Links': links,
            'All_linked': all_linked,
            'Anchors': anchors,
            'Flown': flown}

    print("num speakers total", num_speakers_total)
    return data

def get_data_manual():
    data = {}
    hang = list(map(float, input("Enter hang position with spaces between x y z\n").split()))
    num_anchors = input("Enter num of anchor points in cable trace.")
    anchors = []
    amp_position = [0., 0., 0.]
    for i in range(num_anchors):
        anchor = list(map(float, input("Enter anchor point for cable trace in x y z\n").split()))
        anchors.append(anchor)
    speaker = input("Speaker J-Sub, J-Top or one channel? Enter 'J-Sub', 'J-Top', 'One'\n")
    assert (speaker == 'J-Sub' or speaker == 'J-Top' or speaker == 'One')
    links = False
    if speaker == 'J-Top' or speaker == 'One':
        links = input("Are they linked? y/n")
        if links == 'y':
            links = True
        else: links = False
    num_speakers = int(input("Num of speakers in hang?\n"))
    data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': links, 'Anchors': anchors}
    return data


def get_cable_number(data):
    # default amp position under center stage
    # 4 back to wall + 13.5 up the ceiling

    hang = data['Hang']  # parsing data to variables
    speakers = data['Speaker']
    num_speakers = data['Num_speakers']
    anchors = data['Anchors']
    distance_to_hang = get_distance_to_hang(hang, anchors)
    num_6legged_fanouts, num_3legged_fanouts = 0, 0
    num_soca_cables_total, num_ep5_cables_total = 0, 0

    for speaker in speakers.keys():
        if speaker == "J-SUB":
            num_3legged_fanouts, num_ep5_lines, num_soca_lines = get_subs_lines(speakers[speaker])
        elif speaker == "J-Top":
            num_3legged_fanouts, num_ep5_lines, num_soca_lines = get_Jtop_lines(data, speakers[speaker])
        else:
            print("presuming one channel speakers")
            num_6legged_fanouts, num_ep5_lines, num_soca_lines = get_oneamp_lines(data, num_speakers)

    if num_soca_lines > 0:
        num_soca_cables_inline = 1
        while distance_to_hang > SOCA_LEN * num_soca_cables_inline:
            num_soca_cables_inline += 1
        num_soca_cables_total = num_soca_cables_inline * num_soca_lines

    if num_ep5_lines > 0:
        num_ep5_cables_inline = 1
        while distance_to_hang > EP5_LEN * num_ep5_cables_inline:
            num_ep5_cables_inline += 1
        num_ep5_cables_total = num_ep5_cables_inline * num_ep5_lines

    print("\nType of speaker", speaker, "\nDistance to speaker", distance_to_hang, "\nNumber of speakers", num_speakers,
          "\nAmp position", anchors[0])
    print("Hang", data['Hang'])
    print('Anchors')

    for anchor in anchors:
        if anchor != anchors[0]:
            print(anchor)
    print("Soca", num_soca_cables_total, "\nEP5", num_ep5_cables_total,
          "\n3 legged fanouts", num_3legged_fanouts, "\n6 legged fanouts", num_6legged_fanouts)
    print("Soca lines", num_soca_lines)
    print("EP5 lines", num_ep5_lines)
    num_cables_total = {"EP5": num_ep5_cables_total,"Soca": num_soca_cables_total, "ThreeLegFanOut":num_3legged_fanouts,
                        "SixLegFanOut": num_6legged_fanouts, "Distance": distance_to_hang, "NumSpeakers": num_speakers,
                        "TypeSpeakers": speaker}
    return num_cables_total


def get_oneamp_lines(data, num_speakers):
    if data['All_linked'] == True:
        num_soca_lines = int(num_speakers / 2 / FAN_OUT_6_LEGS)
        num_ep5_lines = num_speakers / 2 - (num_soca_lines * FAN_OUT_3_LEGS)
    elif data['All_linked'] == False:
        num_soca_lines = int(num_speakers / FAN_OUT_6_LEGS)
        num_ep5_lines = num_speakers - (num_soca_lines * FAN_OUT_3_LEGS)
    num_6legged_fanouts = num_soca_lines
    return num_6legged_fanouts, num_ep5_lines, num_soca_lines


def get_Jtop_lines(data, num_speakers):
    if data['All_linked'] == True:
        num_soca_lines = int(num_speakers / 2 / FAN_OUT_3_LEGS)
        num_ep5_lines = num_speakers / 2 - (num_soca_lines * FAN_OUT_3_LEGS)
    elif data['All_linked'] == False:
        num_soca_lines = int(num_speakers / FAN_OUT_3_LEGS)
        num_ep5_lines = num_speakers - (num_soca_lines * FAN_OUT_3_LEGS)
    num_3legged_fanouts = num_soca_lines
    return num_3legged_fanouts, num_ep5_lines, num_soca_lines


def get_subs_lines(num_speakers):
    """

    :param num_speakers:
    :return:
    """
    num_soca_lines = int(num_speakers / FAN_OUT_3_LEGS)
    num_ep5_lines = num_speakers - (num_soca_lines * FAN_OUT_3_LEGS)
    num_3legged_fanouts = num_soca_lines
    return num_3legged_fanouts, num_ep5_lines, num_soca_lines


def get_distance_to_hang(hang, anchors) -> float:
    delta = 0. #diff between two anchor points
    for i in range(len(anchors) - 1):
        for j in range(len(anchors[i])):
           delta += abs(anchors[i][j] - anchors[i+1][j])
    print("Distance inside func", delta)

    for d in range(len(anchors[-1])):
        delta += abs(anchors[-1][d] - hang[d])


    print("Distance inside func", delta)
    return delta


def main():
    data = get_data_pdf()  # getting the data from user
    get_cable_number(data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


