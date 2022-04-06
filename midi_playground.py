from music21 import *
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

input_file = '/Users/liuxinhong/Documents/毕业论文/数据集/rap beat/scrub_A#_144bpm_dripchord.midi'
midi = converter.parse(input_file)
output = []
for part in midi.parts:
    
    notes_to_parse = part.recurse()

    for element in notes_to_parse:
        if isinstance(element, note.Rest):
            print(element)


midi_stream = stream.Stream(output)
midi_stream.write('midi', fp=input_file.rsplit('/', 1)[0] + '/test.midi')