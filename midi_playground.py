from music21 import *
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

midi = converter.parse('/Users/liuxinhong/Documents/毕业论文/数据集/rap beat/scrub_A#_144bpm_dripchord.midi')
for part in midi.parts:
    
    notes_to_parse = part.recurse() 

    for element in notes_to_parse:
        print(element)