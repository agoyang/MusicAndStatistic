from mido import MidiFile, MidiTrack, Message
import mido
import numpy as np
import time

data_midi = MidiFile("/Users/liuxinhong/Documents/毕业论文/数据集/Summer.midi")

print(mido.get_output_names())  #print all available output ports

port = mido.open_output('Virtual Test Bus 1')

for msg in data_midi.play():
    port.send(msg)