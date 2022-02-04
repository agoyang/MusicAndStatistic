import importlib
import numpy as np
from hmmlearn import hmm
from read_midi import *
import mido

data_ary = file2arry('/Users/liuxinhong/Documents/毕业论文/数据集/bach_846_format0.midi')

arry2file(data_ary, fname='/Users/liuxinhong/Documents/毕业论文/数据集/new_midi.mid')