from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
Midi = MyMidi('/Users/liuxinhong/Documents/毕业论文/数据集/twinkle/35393.midi')
data = np.array(Midi.read_midi(ins = 'Piano', show_hist = True, threshold = 3)).reshape(-1,1)
model = MultinomialHMM(n_components = 5)
model.fit(data)
print(model.emissionprob_)
sample = model.sample(120)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, '/Users/liuxinhong/Documents/毕业论文/数据集/twinkle/hmmv3_35393.midi')