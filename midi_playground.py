from music21 import *
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

input_file = '/Users/liuxinhong/Documents/thesis/数据集/boombap/Midi/Part 1/JBB - Drums 1.mid'
midi = converter.parse(input_file)
output = []
for part in midi.parts:
    
    notes_to_parse = part.recurse()

    for element in notes_to_parse:
        output.append(element)

print(clef.Treble8vbClef().octaveChange)
midi_stream = stream.Stream([clef.Treble8vbClef()] + output[3:])
midi_stream.write('midi', fp='/Users/liuxinhong/Documents/thesis/数据集/boombap/Midi/Part 1/test.mid')