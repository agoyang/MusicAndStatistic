from mido import MidiFile, MidiTrack, Message
import mido
import numpy as np
import time

data_midi = MidiFile("/Users/liuxinhong/Documents/毕业论文/数据集/Summer.midi")

print(mido.get_output_names())