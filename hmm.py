from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
Midi = MyMidi('/Users/liuxinhong/Documents/毕业论文/数据集/Beethoven/beethoven_opus10_3_format0.midi')
data = np.array(Midi.read_midi(ins = 'Piano', show_hist = False, threshold = 4)).reshape(-1,1)
model = MultinomialHMM(n_components = 4)
model.fit(data)
print(model.emissionprob_)
sample = model.sample(60)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, '/Users/liuxinhong/Documents/毕业论文/数据集/Beethoven/hmm_v2_beethoven_opus10_3_format0.midi')