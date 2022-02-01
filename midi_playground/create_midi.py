from fileinput import filename
from mido import Message, MidiFile, MidiTrack

fname = "/Users/liuxinhong/Documents/毕业论文/数据集/Summer.midi"
mid = MidiFile(fname)

for i, track in enumerate(mid.tracks):
    for msg in track:
        print(msg)