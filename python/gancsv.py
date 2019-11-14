import os
import csv

beginningPart = '0, 0, Header, 1, 1, 480\n1, 0, Start_track\n1, 0, Time_signature, 4, 2, 24, 8\n1, 0, Key_signature, 0, "major"\n1, 0, Tempo, 500000\n1, 0, Control_c, 0, 121, 0\n1, 0, Program_c, 0, 0\n1, 0, Control_c, 0, 7, 100\n1, 0, Control_c, 0, 10, 64\n1, 0, Control_c, 0, 91, 0\n1, 0, Control_c, 0, 93, 0\n1, 0, MIDI_port, 0\n'

note_map = []
ascii_val = 48
for i in range(50):
    note_map.append(chr(ascii_val))
    ascii_val += 1

def getNoteNum(val):
    num = note_map.index(val)
    return num + 40

HERE = os.getcwd()
TARGET_FILE = "/cmaj-csv-measures/"
FILE_PATH = HERE + "/cmaj-gan-measures/"
TARGET_PATH = HERE + TARGET_FILE

for root, dirs, files in os.walk("cmaj-gan-measures"):
    measure = 1
    for filename in files:
        #print(filename + "********************")
        f = open(FILE_PATH + filename, 'r')
        g = open(TARGET_PATH + "cmaj-measure" + str(measure), 'a')
        g.write(beginningPart)
        relTime = 0
        for line in f:
            #print(line)
            #print("first letter: " + line[0])
            first_letter = line[0]
            if first_letter == '-':
                time = line.count(first_letter) * 40
                relTime += time
            try:
                noteNum = getNoteNum(first_letter)
            except(ValueError):
                continue
            #print(noteNum)
            noteCount = line.count(first_letter)
            #print("hyphens: " + hyphens)
            time = noteCount * 40
            #print("time: " + str(time))
            line1 = f"1, {relTime}, Note_on_c, 0, {noteNum}, 80\n"
            g.write(line1)
            line2 = f"1, {relTime + time - 13}, Note_on_c, 0, {noteNum}, 0\n"
            g.write(line2)
            relTime += time
        line_final = f"1, {relTime - 12}, End_track\n"
        file_end = "0, 0, End_of_file"
        g.write(line_final)
        g.write(file_end)
        measure += 1
        #print(line_final)
        f.close()
        g.close()
