from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
Midi = MyMidi('/Users/liuxinhong/Documents/毕业论文/数据集/beat/Fit_The_Description_C#_162_dripchord.mid')
data = np.array(Midi.read_midi(ins = '', show_hist = False, threshold = 3)).reshape(-1, 1)
model = MultinomialHMM(n_components = 4)
model.fit(data)
sample = model.sample(60)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, '/Users/liuxinhong/Documents/毕业论文/数据集/beat/hmm_Fit_The_Description_C#_162_dripchord.mid')
print(model.emissionprob_)