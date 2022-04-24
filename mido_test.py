from mido import MidiFile
mid = MidiFile('/Users/liuxinhong/Documents/thesis/数据集/boombap/Midi/Part 1/JBB - Drums 1.mid', clip=True)
for msg in mid.tracks[1]:
    print(msg)