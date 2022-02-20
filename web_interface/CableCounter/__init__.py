import csv
from tabula import read_pdf_with_template

C = 13.5  # ceiling meters high
SOCA_LEN = 25  # soca cable meters
EP5_LEN = 10  # ep5 cable meters
FAN_OUT_3_LEGS = 3  # cable breakout for 3 biamp legs
FAN_OUT_6_LEGS = 6  # cable breakout for 6 oneamp legs


def get_data_pdf(filepath):
    template_path = 'Main_Setup.tabula-template.json'
    df = read_pdf_with_template(filepath,
                                template_path,
                                pandas_options={'header': None})

    for t in df:
        print(t)

    is_flown = df[0][1][0].split(" ")[-1]
    print(is_flown)
    if is_flown == 'flown':
        flown = True
    else:
        flown = False

    hang = [float(df[1][1][0][0:-2]),
            float(df[1][3][0][0:-2]),
            float(df[1][1][1][0:-2])]  # dataframe indexing df[table][column][row][string in row]

    num_speakers_total = int(df[1][3][1]) + int(df[1][3][2]) + int(df[1][3][3])

    speakers = {}
    for i in range(1, 4):
        speakers[(df[1][2][i].split(" ")[-1][0:-1])] = int(df[1][3][i])

    try:
        speakers['J-Top'] = speakers['J8'] + speakers['J12']
        speakers.pop('J8')
        speakers.pop('J12')
    except:
        print('no J in speakers')

    links = df[3][7].isna().sum()

    all_linked = False
    if links != 0:
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


def get_lines(data):
    biamp_lines, one_amp_lines = 0, 0
    for speaker in data['Speaker']:
        if speaker == 'J-SUB':
            biamp_lines += data['Speaker']['J-SUB']
        if speaker == 'J-Top':
            biamp_lines += data['Speaker']["J-Top"] - data['Links']
        else:
            one_amp_lines += data['Speaker'][speaker] - data['Links']
    return biamp_lines, one_amp_lines


def calculate_soca(biamp_lines, one_amp_lines):
    assert (biamp_lines != one_amp_lines)

    if biamp_lines > one_amp_lines:
        soca_lines = int(biamp_lines / FAN_OUT_3_LEGS)
        biamp_lines -= soca_lines * FAN_OUT_3_LEGS
        num_lines = {'Soca': soca_lines, 'EP5': biamp_lines, 'Calamary': soca_lines, 'Octopus': 0}
    else:
        soca_lines = int(one_amp_lines / FAN_OUT_6_LEGS)
        one_amp_lines -= soca_lines * FAN_OUT_6_LEGS
        num_lines = {'Soca': soca_lines, 'EP5': one_amp_lines, 'Calamary': 0, 'Octopus': soca_lines}
    return num_lines


def get_data_manual():
    hang = list(map(float, input("Enter hang position with spaces between x y z\n").split()))
    num_anchors = input("Enter num of anchor points in cable trace.")
    anchors = []
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
        else:
            links = False
    num_speakers = int(input("Num of speakers in hang?\n"))
    data = {'Hang': hang, 'Speaker': speaker, 'Num_speakers': num_speakers, 'Links': links, 'Anchors': anchors}
    return data


def get_distance_to_hang(hang, anchors) -> float:
    delta = 0.  # diff between two anchor points
    for i in range(len(anchors) - 1):
        for j in range(len(anchors[i])):
            delta += abs(anchors[i][j] - anchors[i + 1][j])
    for d in range(len(anchors[-1])):
        delta += abs(anchors[-1][d] - hang[d])
    return delta


def get_cable_number(data):
    # parsing data to variables

    distance_to_hang = get_distance_to_hang(data['Hang'], data['Anchors'])
    num_soca_cables_total, num_ep5_cables_total = 0, 0

    biamp_lines, one_amp_lines = get_lines(data)
    num_lines = calculate_soca(biamp_lines, one_amp_lines)

    if num_lines['Soca'] > 0:
        num_soca_cables_inline = 1
        while distance_to_hang > SOCA_LEN * num_soca_cables_inline:
            num_soca_cables_inline += 1
        num_soca_cables_total = num_soca_cables_inline * num_lines['Soca']

    if num_lines['EP5'] > 0:
        num_ep5_cables_inline = 1
        while distance_to_hang > EP5_LEN * num_ep5_cables_inline:
            num_ep5_cables_inline += 1
        num_ep5_cables_total = num_ep5_cables_inline * num_lines['EP5']

    print("\nType of speaker", data['Speaker'],
          "\nDistance to speaker", distance_to_hang,
          "\nNumber of speakers", data['Num_speakers'],
          "\nAmp position", data['Anchors'][0])
    print("Hang", data['Hang'])
    print('Anchors')
    for anchor in data['Anchors']:
        if anchor != data['Anchors'][0]:
            print(anchor)
    print("Soca", num_soca_cables_total,
          "\nEP5", num_ep5_cables_total,
          "\n3 legged fanouts", num_lines['Calamary'],
          "\n6 legged fanouts", num_lines['Octopus'])
    print("Soca lines", num_lines['Soca'])
    print("EP5 lines", num_lines['EP5'])

    cable_numbers = {"TypeSpeakers": data['Speaker'],
                     "EP5": num_ep5_cables_total,
                     "Soca": num_soca_cables_total,
                     "ThreeLegFanOut": num_lines['Calamary'],
                     "SixLegFanOut": num_lines['Octopus'],
                     "Distance": distance_to_hang,
                     "NumSpeakers": data['Num_speakers']
                     }


    return cable_numbers



