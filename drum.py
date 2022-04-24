from read_midi import *
input_file = '/Users/liuxinhong/Documents/thesis/数据集/boombap/Midi/Part 1/JBB - Drums 1.mid'
Midi = MyMidi(input_file)
data, chord_data = Midi.read_notes(ins = 'Piano', show_hist = False)