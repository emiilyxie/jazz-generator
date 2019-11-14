import os
import csv

# HELPER FUNCTIONS

with open('output.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    rows = list(readCSV)

def remove_spaces(arr):
    for row in range(len(arr)):
        for r in range(len(arr[row])):
            arr[row][r] = arr[row][r].strip()
    return arr


def strToInt(arr):
    for row in range(len(arr)):
        for r in range(len(arr[row])):
            try:
                arr[row][r] = int(arr[row][r])
            except(ValueError):
                pass
    return arr

def getNote(num):
    noteNum = num - 40
    return note_map[noteNum]

note_map = []
ascii_val = 48
for i in range(50):
    note_map.append(chr(ascii_val))
    ascii_val += 1

def round_to_nearest_6(num):
    n = num + (6//2)
    return n - (n % 6)

def check_for_rests(row, nextRow, nextNote):
    if nextNote[1] - nextRow[1] >= 40:
        return True
    else:
        return False

def add_data(row, nextRow, nextNote, endpt):
    time = (nextNote[1] - row[1]) / 40
    #print("time:" + str(time))
    #hyphens = "-" * int(time)
    note = getNote(row[4])
    #print("note:" + str(note))
    if check_for_rests(row, nextRow, nextNote) == True:
        #print("checking for rests")
        if nextNote[1] > endpt:
            #print("nah it's normal")
            return note * int(time) + "\n"
        else:
            #print('rest processing')
            rests = int((nextNote[1] - nextRow[1]) / 40) - 1
            rests = round_to_nearest_6(rests)
            new_note_length = int((nextRow[1] - row[1]) / 40) + 1
            new_note_length = round_to_nearest_6(new_note_length)
            #print('rest and new note length: ' + str(rests) + ',' + str(new_note_length))
            return note * new_note_length + "\n" + '-' * rests + "\n"
    return note * int(time) + "\n"

def add_rest(prev, row):
    time = int((row - prev) / 40)
    #print('rest time: ' + str(time))
    return "-" * time + "\n"

# MAIN FUNCTION

endpt = 0
measure = 0
HERE = os.getcwd()
FILE_PATH = HERE + "/cmaj-gan-measures/"
FILE_BASE = "cmaj-measure"
noSpaces = remove_spaces(rows)
formatted = strToInt(noSpaces)

#print("first endpt: " + str(endpt))
for row in range(len(formatted)):
    if formatted[row][2] != 'Note_on_c' or formatted[row][5] != 80:
        continue
    if formatted[row][1] == endpt: #endpt is actually startpt of a new measure
        try:
            measure += 1
            #print("measure:" + str(measure))
            endpt = endpt + 1920
            #print("endpt 1:" + str(endpt))
            f = open(FILE_PATH + FILE_BASE + str(measure), 'a')
            added_data = add_data(formatted[row], formatted[row+1], formatted[row+2], endpt)
            #print("added data: " + added_data)
            f.write(added_data)
            f.close()
            continue
        except(IndexError):
            #print(IndexError)
            pass
    if formatted[row][1] > endpt:
        try:
            measure += 1
            #print('measure: ' + str(measure))
            endpt = endpt + 1920 * 2
            prev_endpt = endpt - 1920
            f = open(FILE_PATH + FILE_BASE + str(measure), 'a')
            if formatted[row][1] == prev_endpt:
                #print('endpt: ' + str(endpt))
                added_data = add_data(formatted[row], formatted[row+1], formatted[row+2], endpt)
                f.write(added_data)
                f.close()
            else:
                rests = add_rest(prev_endpt, formatted[row][1])
                note = add_data(formatted[row], formatted[row+1], formatted[row+2], endpt)
                added_data = rests + note
                #print('added data:' + added_data)
                f.write(added_data)
                f.close()
            continue
        except(IndexError):
            pass
    if formatted[row][1] < endpt:
        try:
            #print("endpt 2:" + str(endpt))
            #print("measure:" + str(measure))
            f = open(FILE_PATH + FILE_BASE + str(measure), 'a')
            added_data = add_data(formatted[row], formatted[row+1], formatted[row+2], endpt)
            #print("added data: " + added_data)
            f.write(added_data)
            f.close()
            continue
        except(IndexError):
            #print(IndexError)
            pass
